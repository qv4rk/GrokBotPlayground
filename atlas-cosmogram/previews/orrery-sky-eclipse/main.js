import * as THREE from './vendor/three.module.js';
import {OrbitControls} from './vendor/OrbitControls.js';
import {ScaleOrrery} from './orrery/orrery.js';
import {moonOffsetUnits} from './orrery/scale.js';
import {makeCosmos,raDecToScene} from './cosmos.js';
import {EclipseScene} from './eclipse-scene.js';
import {Astronomy as A,EVENTS,AU,EARTH_A,ephemeris,observer,sceneVector,atPoint,shadowCenter,rayEllipsoid} from './physics.mjs';
const $=id=>document.getElementById(id),rad=Math.PI/180;
const title=s=>s[0].toUpperCase()+s.slice(1);
let renderer;
try {
  renderer=new THREE.WebGLRenderer({canvas:$('space'),antialias:true,alpha:true,logarithmicDepthBuffer:true,preserveDrawingBuffer:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setSize(innerWidth,innerHeight);
  renderer.outputColorSpace=THREE.SRGBColorSpace;
  const orbitScene=new THREE.Scene();orbitScene.background=new THREE.Color(0x020306);
  const orrery=new ScaleOrrery();orbitScene.add(orrery.group);
  const eclipse=new EclipseScene();
  orrery.bodies.earth.mesh.geometry.dispose();orrery.bodies.earth.mesh.geometry=eclipse.earth.geometry.clone();
  const orbitCamera=new THREE.PerspectiveCamera(45,innerWidth/innerHeight,1e-7,100000);
  const earthCamera=new THREE.PerspectiveCamera(45,innerWidth/innerHeight,1e-5,100000);
  const skyCamera=new THREE.PerspectiveCamera(70,innerWidth/innerHeight,1e-7,100000);
  const orbitControls=new OrbitControls(orbitCamera,$('space'));
  const earthControls=new OrbitControls(earthCamera,$('space'));
  orbitControls.enableDamping=earthControls.enableDamping=true;
  earthControls.minDistance=.015;earthControls.maxDistance=300;
  const cosmos=await makeCosmos(8000);cosmos.setCulture('both');
  const eclipticToEquatorial=new THREE.Matrix4();
  let view='earth',event=EVENTS[0],date=event.eclipse.peak.date,state=ephemeris(date),playing=false;
  let mode='visible',focus='',lat=event.eclipse.latitude,lon=event.eclipse.longitude,following=true;
  let lastEarth=new THREE.Vector3(),lastFocus=new THREE.Vector3(),sunLock=false;
  const bodyNames={sun:'Sun',mercury:'Mercury',venus:'Venus',earth:'Earth',mars:'Mars',jupiter:'Jupiter',saturn:'Saturn',uranus:'Uranus',neptune:'Neptune',moon:'Moon',io:'Io',europa:'Europa',ganymede:'Ganymede',callisto:'Callisto'};
  for(const e of EVENTS){const o=new Option(e.name,e.id);$('event').add(o);}
  for(const [name,label] of Object.entries(bodyNames)) $('focus').add(new Option(label,name));
  const nameNodes=cosmos.centres.map(c=>{
    const el=document.createElement('span');el.className='star-name';el.textContent=c.name;
    $('constellation-labels').appendChild(el);return {el,dir:c.dir};
  });
  $('catalog').textContent=`${cosmos.counts.stars.toLocaleString()} stars · ${cosmos.counts.western} Western figures · ${cosmos.counts.chinese} Chinese figures`;
  function eclScene(vector) {
    const v=A.RotateVector(A.Rotation_EQJ_ECL(),vector);
    return new THREE.Vector3(v.x,v.z,-v.y);
  }
  function fromEqDate(vector) {
    return eclScene(A.RotateVector(A.Rotation_EQD_EQJ(state.time),new A.Vector(vector[0],vector[1],vector[2],state.time)));
  }
  function updateOrrery() {
    orrery.setJulianDay(state.jd);
    const oldJupiter=orrery.bodyPosition('jupiter');
    for(const name of ['mercury','venus','earth','mars','jupiter','saturn','uranus','neptune']){
      const p=eclScene(A.HelioVector(bodyNames[name],state.time)).multiplyScalar(15);
      orrery.bodies[name].holder.position.copy(p);
    }
    const jupiterDelta=orrery.bodyPosition('jupiter').sub(oldJupiter);
    for(const name of ['io','europa','ganymede','callisto'])orrery.bodies[name].holder.position.add(jupiterDelta);
    const m=eclScene(A.GeoMoon(state.time));
    const off=moonOffsetUnits({x:m.x,y:m.y,z:m.z},'earth',mode);
    // moonOffsetUnits accepts a vector; its scale operation is frame independent.
    orrery.bodies.moon.holder.position.copy(orrery.bodyPosition('earth')).add(new THREE.Vector3(off.x,off.y,off.z));
    for(const [name,b] of Object.entries(orrery.bodies)){
      b.marker.visible=true;
      if(name==='earth') {
        const g=state.gast*rad;
        const x=fromEqDate([Math.cos(g),Math.sin(g),0]);
        const y=fromEqDate([0,0,1]);const z=fromEqDate([Math.sin(g),-Math.cos(g),0]);
        b.mesh.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x,y,z));
      } else if(bodyNames[name]&& !['io','europa','ganymede','callisto'].includes(name)) {
        const axis=A.RotationAxis(bodyNames[name],state.time);
        const pole=eclScene(axis.north).normalize();
        b.mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),pole);
        b.mesh.rotateY(axis.spin*rad);
      }
    }
    const saturnRing=orrery.bodies.saturn.mesh.children[0];
    if(saturnRing)saturnRing.quaternion.setFromAxisAngle(new THREE.Vector3(1,0,0),-Math.PI/2);
  }
  function cosmosTransform() {
    const r=A.Rotation_ECL_EQD(state.time);
    const basis=[[1,0,0],[0,0,1],[0,-1,0]].map(v=>{
      const p=A.RotateVector(r,new A.Vector(...v,state.time));return new THREE.Vector3(p.x,p.z,-p.y);
    });
    eclipticToEquatorial.makeBasis(...basis);
    cosmos.group.quaternion.setFromRotationMatrix(view==='orrery'?new THREE.Matrix4():eclipticToEquatorial);
  }
  function dateBox() {
    const iso=date.toISOString();$('clock').textContent=`${iso.slice(0,10)} ${iso.slice(11,19)} UTC · JD ${state.jd.toFixed(6)}`;
    if(document.activeElement!==$('date'))$('date').value=iso.slice(0,19);
    const offset=(date-event.eclipse.peak.date)/60000;
    $('scrub').value=Math.max(-120,Math.min(120,offset));$('offset').textContent=`${offset>=0?'+':''}${offset.toFixed(1)} min`;
  }
  function setDate(next) {
    date=new Date(next);if(!Number.isFinite(+date))return;
    const previousGast=state.gast;
    state=ephemeris(date);updateOrrery();eclipse.update(state,lat,lon);cosmosTransform();dateBox();
    if(view==='sky'){
      skyCamera.quaternion.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0,1,0),(state.gast-previousGast)*rad));
      anchorSky();if(sunLock)skyCamera.lookAt(eclipse.sun.position);
    }
    if(view==='earth'&&following){
      const center=eclipse.center?.position;
      if(center){const p=new THREE.Vector3(...sceneVector(center));const delta=p.clone().sub(lastEarth);
        if(lastEarth.lengthSq()){earthCamera.position.add(delta);earthControls.target.add(delta);}lastEarth.copy(p);}
    }
    if(view==='orrery'&&focus){const p=orrery.bodyPosition(focus),delta=p.clone().sub(lastFocus);orbitCamera.position.add(delta);orbitControls.target.add(delta);lastFocus.copy(p);}
    const center=eclipse.center;
    $('shadow').textContent=center?`Calculated shadow axis: ${center.lat.toFixed(4)}° N · ${center.lon.toFixed(4)}° E`:'Shadow axis does not intersect Earth at this time';
    const local=atPoint(state,observer(state,lat,lon));
    $('sky-status').textContent=`At observer: ${local.kind} · ${(local.obscuration*100).toFixed(2)}% Sun covered · altitude ${local.altitude.toFixed(1)}°`;
    eclipse.corona.visible=view==='sky'&&local.kind==='Total';
    eclipse.corona.position.copy(eclipse.sun.position).multiplyScalar(.9999);
    eclipse.corona.quaternion.copy(skyCamera.quaternion);
  }
  function anchorSky() {
    const p=new THREE.Vector3(...sceneVector(observer(state,lat,lon,10)));
    skyCamera.position.copy(p);skyCamera.up.copy(p).normalize();
  }
  function lookSun(close=true) {
    sunLock=true;
    skyCamera.fov=close?.85:70;skyCamera.updateProjectionMatrix();
    skyCamera.lookAt(eclipse.sun.position);$('fov').value=skyCamera.fov;
  }
  function wideSky() {
    sunLock=false;
    skyCamera.fov=70;skyCamera.updateProjectionMatrix();$('fov').value=70;
    const p=skyCamera.position.clone();skyCamera.lookAt(p.clone().add(p.clone().normalize()));
  }
  function frameEarth() {
    eclipse.frame($('vantage').value,earthCamera,earthControls);
    if(eclipse.center)lastEarth.set(...sceneVector(eclipse.center.position));
  }
  function frameOrbit() {
    orbitCamera.fov=45;orbitCamera.updateProjectionMatrix();
    if(!focus){orbitCamera.position.set(0,350,650);orbitControls.target.set(0,0,0);}
    else{const p=orrery.bodyPosition(focus),r=orrery.bodyRadius(focus);
      orbitControls.target.copy(p);orbitCamera.position.copy(p).add(new THREE.Vector3(0,.35,1).normalize().multiplyScalar(r*6));lastFocus.copy(p);}
    orbitControls.update();
  }
  function setView(next) {
    view=next;orbitControls.enabled=next==='orrery';earthControls.enabled=next==='earth';
    for(const b of document.querySelectorAll('[data-view]'))b.classList.toggle('active',b.dataset.view===view);
    $('earth-tools').hidden=next!=='earth';$('orrery-tools').hidden=next!=='orrery';$('sky-tools').hidden=next!=='sky';
    $('selection').hidden=true;
    eclipse.beacon.visible=next==='earth';
    (next==='orrery'?orbitScene:eclipse.scene).add(cosmos.group);cosmosTransform();
    if(next==='orrery')frameOrbit();else if(next==='earth')frameEarth();else {anchorSky();wideSky();}
    setDate(date);
  }
  function useEvent(id) {
    event=EVENTS.find(e=>e.id===id)||EVENTS[0];date=event.eclipse.peak.date;
    lat=event.eclipse.latitude;lon=event.eclipse.longitude;$('lat').value=lat.toFixed(4);$('lon').value=lon.toFixed(4);
    eclipse.setEvent(event);$('nasa-source').href=event.source;setDate(date);
    if(view==='earth')frameEarth();if(view==='sky')lookSun();
  }
  const camera=()=>view==='orrery'?orbitCamera:view==='earth'?earthCamera:skyCamera;
  const scene=()=>view==='orrery'?orbitScene:eclipse.scene;
  const tapPoints=()=>view==='orrery'?Object.values(orrery.bodies).map(b=>b.mesh):[eclipse.moon,eclipse.sun,eclipse.earth,...(eclipse.beacon.visible?[eclipse.beacon]:[]),...[...eclipse.planets.values()]];
  function tapAt(x,y) {
    const ray=new THREE.Raycaster();ray.setFromCamera(new THREE.Vector2(x/innerWidth*2-1,1-y/innerHeight*2),camera());
    const hit=ray.intersectObjects(tapPoints(),false)[0];let name=hit?.object.name;
    if(hit?.object===eclipse.earth){const p=[hit.point.x*EARTH_A,-hit.point.z*EARTH_A,hit.point.y*EARTH_A];
      const g=atPoint(state,p);name=`Earth · ${(g.obscuration*100).toFixed(1)}% Sun covered`;}
    if(!name){let nearest=Infinity;for(const body of tapPoints()){
      const p=body.getWorldPosition(new THREE.Vector3()).project(camera());if(p.z<-1||p.z>1)continue;
      const d=Math.hypot((p.x+1)*innerWidth/2-x,(1-p.y)*innerHeight/2-y);
      if(d<24&&d<nearest){nearest=d;name=body.name;}
    }}
    if(!name&&cosmos.group.visible){
      const points=cosmos.group.children[0].geometry.getAttribute('position');let nearest=12;
      for(let i=0;i<points.count;i++){const p=new THREE.Vector3().fromBufferAttribute(points,i).applyMatrix4(cosmos.group.matrixWorld).project(camera());
        if(p.z<-1||p.z>1)continue;const d=Math.hypot((p.x+1)*innerWidth/2-x,(1-p.y)*innerHeight/2-y);
        if(d<nearest){nearest=d;const star=cosmos.stars[i];name=star.properties.name||`Catalog star ${star.id} · mag ${star.properties.mag}`;}}
    }
    const label=$('selection');label.hidden=!name;
    if(name){label.textContent=title(name);label.style.left=`${Math.max(8,Math.min(x+12,innerWidth-245))}px`;label.style.top=`${Math.max(55,y-40)}px`;}
  }
  let gesture=null;const pointers=new Map();let pinch=null;
  $('space').addEventListener('pointerdown',e=>{
    gesture=e.isPrimary?{id:e.pointerId,x:e.clientX,y:e.clientY,moved:false}:null;
    if(view!=='sky')return;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});pinch=null;
    if(pointers.size===2){const [a,b]=[...pointers.values()];pinch=Math.hypot(a.x-b.x,a.y-b.y);}
    $('space').setPointerCapture(e.pointerId);
  });
  function fov(next){skyCamera.fov=Math.max(.65,Math.min(100,next));skyCamera.updateProjectionMatrix();$('fov').value=skyCamera.fov;}
  $('space').addEventListener('pointermove',e=>{
    if(gesture?.id===e.pointerId&&Math.hypot(e.clientX-gesture.x,e.clientY-gesture.y)>8)gesture.moved=true;
    if(view!=='sky'||!pointers.has(e.pointerId))return;
    const old=pointers.get(e.pointerId);pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});
    if(pointers.size===1){sunLock=false;const d=skyCamera.getWorldDirection(new THREE.Vector3()),k=skyCamera.fov*rad/innerHeight;
      d.applyAxisAngle(skyCamera.up,-(e.clientX-old.x)*k);
      const right=new THREE.Vector3().crossVectors(d,skyCamera.up).normalize();
      d.applyAxisAngle(right,-(e.clientY-old.y)*k);skyCamera.lookAt(skyCamera.position.clone().add(d));
    }else if(pointers.size===2){const [a,b]=[...pointers.values()],d=Math.hypot(a.x-b.x,a.y-b.y);if(pinch&&d>0)fov(skyCamera.fov*pinch/d);pinch=d;}
  });
  function end(e){if(gesture?.id===e.pointerId&&!gesture.moved&&e.type==='pointerup')tapAt(e.clientX,e.clientY);
    if(gesture?.id===e.pointerId)gesture=null;pointers.delete(e.pointerId);pinch=null;}
  for(const type of ['pointerup','pointercancel','lostpointercapture'])$('space').addEventListener(type,end);
  $('space').addEventListener('wheel',e=>{if(view==='sky'){e.preventDefault();fov(skyCamera.fov*Math.exp(e.deltaY*(e.ctrlKey?.00035:.001)));}}, {passive:false});
  for(const b of document.querySelectorAll('[data-view]'))b.onclick=()=>setView(b.dataset.view);
  $('event').onchange=()=>{playing=false;$('play').textContent='Play';useEvent($('event').value);};
  $('date').onchange=()=>{playing=false;$('play').textContent='Play';setDate(new Date($('date').value+'Z'));};
  $('peak').onclick=()=>{playing=false;$('play').textContent='Play';useEvent(event.id);};
  $('scrub').oninput=()=>{playing=false;$('play').textContent='Play';setDate(new Date(event.eclipse.peak.date.getTime()+Number($('scrub').value)*60000));};
  $('back').onclick=()=>setDate(new Date(+date-60000));$('forward').onclick=()=>setDate(new Date(+date+60000));
  $('play').onclick=()=>{playing=!playing;$('play').textContent=playing?'Pause':'Play';};
  $('vantage').onchange=frameEarth;
  $('track-center').onclick=()=>{following=!following;$('track-center').classList.toggle('active',following);if(following)frameEarth();};
  $('focus').onchange=()=>{focus=$('focus').value;frameOrbit();};
  $('scale').onclick=()=>{mode=mode==='visible'?'true':'visible';orrery.setScaleMode(mode);setDate(date);frameOrbit();$('scale').textContent=mode==='visible'?'Show true scale':'Show visible scale';};
  $('observer').onclick=()=>{const a=Number($('lat').value),b=Number($('lon').value);if(!Number.isFinite(a)||!Number.isFinite(b)||Math.abs(a)>90||Math.abs(b)>180)return;playing=false;$('play').textContent='Play';lat=a;lon=b;setView('sky');wideSky();};
  $('sun').onclick=()=>lookSun();$('zenith').onclick=wideSky;$('fov').oninput=()=>fov(Number($('fov').value));
  $('culture').onchange=()=>{cosmos.setCulture($('culture').value);cosmos.group.visible=$('culture').value!=='off';};
  $('cones').onchange=()=>{eclipse.cones.visible=$('cones').checked;eclipse.footprint.visible=$('cones').checked;};
  $('track').onchange=()=>eclipse.path.visible=$('track').checked;
  $('collapse').onclick=()=>{const hidden=$('dock').classList.toggle('collapsed');$('collapse').textContent=hidden?'+':'−';$('collapse').setAttribute('aria-expanded',String(!hidden));};
  $('sources').onclick=()=>$('about').showModal();$('close-about').onclick=()=>$('about').close();
  $('png').onclick=()=>{const current=scene(),background=current.background;current.background=null;
    renderer.setClearColor(0,0);renderer.render(current,camera());const a=document.createElement('a');
    const output=document.createElement('canvas');output.width=renderer.domElement.width;output.height=renderer.domElement.height;
    const ctx=output.getContext('2d');ctx.drawImage(renderer.domElement,0,0);ctx.scale(output.width/innerWidth,output.height/innerHeight);
    ctx.textAlign='center';ctx.textBaseline='middle';
    for(const {el}of nameNodes)if(!el.hidden){const style=getComputedStyle(el);ctx.font=style.font;ctx.fillStyle=style.color;
      ctx.fillText(el.textContent,parseFloat(el.style.left),parseFloat(el.style.top));}
    a.download=`atlas-${view}-${date.toISOString().replaceAll(':','-')}.png`;a.href=output.toDataURL('image/png');a.click();current.background=background;};
  window.addEventListener('resize',()=>{renderer.setSize(innerWidth,innerHeight);for(const c of [orbitCamera,earthCamera,skyCamera]){c.aspect=innerWidth/innerHeight;c.updateProjectionMatrix();}});
  useEvent('1999');setView('earth');if(innerWidth<700){$('dock').classList.add('collapsed');$('collapse').textContent='+';$('collapse').setAttribute('aria-expanded','false');}
  const query=new URLSearchParams(location.search);if(query.get('event'))useEvent(query.get('event'));if(query.get('view'))setView(query.get('view'));
  let previous=performance.now(),elapsed=0;
  renderer.setAnimationLoop(now=>{
    const dt=Math.min(.1,(now-previous)/1000);previous=now;elapsed+=dt;
    if(playing&&elapsed>.1){setDate(new Date(+date+elapsed*Number($('speed').value)*1000));elapsed=0;}
    if(view==='orrery')orbitControls.update();else if(view==='earth')earthControls.update();
    const c=camera();cosmos.group.position.copy(c.position);
    if(view!=='orrery')for(const p of eclipse.planets.values())p.position.copy(p.userData.realPosition).sub(c.position).normalize().multiplyScalar(7300).add(c.position);
    eclipse.corona.quaternion.copy(skyCamera.quaternion);
    for(const n of nameNodes){const visible=$('names').checked&&cosmos.group.visible&&$('culture').value!=='chinese'&&c.fov>6;
      if(!visible){n.el.hidden=true;continue;}
      const direction=n.dir.clone().applyQuaternion(cosmos.group.quaternion);
      if(view!=='orrery'&&rayEllipsoid([c.position.x*EARTH_A,-c.position.z*EARTH_A,c.position.y*EARTH_A],[direction.x,-direction.z,direction.y])){n.el.hidden=true;continue;}
      const p=direction.multiplyScalar(7900).add(c.position).project(c);
      n.el.hidden=p.z<-1||p.z>1||Math.abs(p.x)>.94||Math.abs(p.y)>.88;
      if(!n.el.hidden){n.el.style.left=`${(p.x+1)*innerWidth/2}px`;n.el.style.top=`${(1-p.y)*innerHeight/2}px`;}}
    renderer.render(scene(),c);
  });
  window.__atlas={renderer,orrery,eclipse,cosmos,setDate,setView,useEvent,get state(){return state;},get view(){return view;},camera,scene};
} catch(error) {$('error').hidden=false;$('error').textContent=`Could not start the Atlas: ${error.message}`;console.error(error);}
