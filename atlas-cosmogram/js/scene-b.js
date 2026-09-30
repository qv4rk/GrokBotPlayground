import { CosmogramScene } from './scene-a.js';
import * as THREE from 'three';
import {
  getGeoCoordinates,
  altitudeAboveHorizon
} from './ephemeris.js';
import { latLonToVector3 } from './globeNodes.js';

const EARTH_R = 1;

Object.assign(CosmogramScene.prototype, {
setCameraMode(mode) {
this.mode = mode;
if (mode === 'planetary') {
this.camera = this.planetaryCam;
this.controls.enabled = true;
this.observerFrame.visible = false;
this.earth.visible = true;
this.eclipticGroup.visible = true;
this.nodes.group.visible = true;
this.planetGroup.visible = true;
} else {
this.camera = this.observerCam;
this.controls.enabled = false;
this.observerFrame.visible = true;
this.earth.visible = false;
this.eclipticGroup.visible = false;
this.nodes.group.visible = false;
this._placeObserverCamera();
this._updateObserverSkyBodies();
}
},
_placeObserverCamera() {
this.observerCam.position.set(-0.2, 0.35, 0);
this.observerCam.up.set(0, 1, 0);
this.observerCam.lookAt(2, 0.2, 0);
},
_updateObserverSkyBodies() {
const bodies = ['sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn'];
for (const name of bodies) {
const alt = altitudeAboveHorizon(name, this.jd, this.observer.lat, this.observer.lon);
const mesh = this.planetMeshes[name];
if (!mesh) continue;
const g = getGeoCoordinates(name, this.jd);
const az = Math.atan2(g.y, g.x);
const altRad = alt * (Math.PI / 180);
const R = 2.2;
const cosAlt = Math.cos(altRad);
mesh.position.set(
R * cosAlt * Math.cos(az),
R * Math.sin(altRad),
R * cosAlt * Math.sin(az)
);
mesh.visible = true;
}
this.planetGroup.visible = true;
},
setNatalFreeze(jd, lat, lon) {
while (this._natalGroup.children.length) {
const c = this._natalGroup.children[0];
this._natalGroup.remove(c);
if (c.geometry) c.geometry.dispose();
if (c.material) c.material.dispose();
}
this.natal = { jd, lat, lon };
const pos = latLonToVector3(lat, lon, EARTH_R * 1.03);
const beacon = new THREE.Mesh(
new THREE.SphereGeometry(0.04, 16, 16),
new THREE.MeshBasicMaterial({ color: 0xff66aa, transparent: true, opacity: 1 })
);
beacon.position.copy(pos);
beacon.userData = { type: 'natal-beacon' };
this._natalGroup.add(beacon);
const pillar = new THREE.Mesh(
new THREE.CylinderGeometry(0.008, 0.008, 0.35, 8),
new THREE.MeshBasicMaterial({ color: 0xff66aa, transparent: true, opacity: 0.7 })
);
pillar.position.copy(pos).multiplyScalar(1.0);
pillar.position.normalize().multiplyScalar(EARTH_R * 1.18);
pillar.lookAt(0, 0, 0);
pillar.rotateX(Math.PI / 2);
this._natalGroup.add(pillar);
const horizon = {};
const bodies = ['sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn'];
const prevJd = this.jd;
this.jd = jd;
this._updatePlanetPositions();
for (const name of bodies) {
const alt = altitudeAboveHorizon(name, jd, lat, lon);
horizon[name] = { altitude: alt, above: alt > 0 };
const mesh = this.planetMeshes[name];
if (!mesh) continue;
const points = [pos.clone(), mesh.position.clone()];
const geo = new THREE.BufferGeometry().setFromPoints(points);
const color = horizon[name].above ? 0x66ffaa : 0x556677;
const line = new THREE.Line(
geo,
new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0.75 })
);
line.userData = { type: 'natal-ray', planet: name };
this._natalGroup.add(line);
}
this.jd = prevJd;
this._updatePlanetPositions();
this.natal.horizon = horizon;
return horizon;
},
clearNatal() {
while (this._natalGroup.children.length) {
this._natalGroup.remove(this._natalGroup.children[0]);
}
this.natal = null;
},
updateTemporalHorizon(year) {
this.nodes.updateTemporalHorizon(year);
},
_onClick(event) {
if (this.mode !== 'planetary') return;
const rect = this.canvas.getBoundingClientRect();
this.pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
this.pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
this.raycaster.setFromCamera(this.pointer, this.camera);
const hits = this.raycaster.intersectObjects(this.nodes.getClickables(), false);
if (hits.length && this.onNodeClick) {
this.onNodeClick(hits[0].object.userData);
}
},
_onResize() {
const w = window.innerWidth;
const h = window.innerHeight;
this.planetaryCam.aspect = w / h;
this.planetaryCam.updateProjectionMatrix();
this.observerCam.aspect = w / h;
this.observerCam.updateProjectionMatrix();
this.renderer.setSize(w, h);
},
animate() {
requestAnimationFrame(() => this.animate());
if (this.mode === 'planetary') {
this.controls.update();
} else {
this._updateObserverSkyBodies();
}
if (this.mode === 'planetary' && this.earth) {
this.earth.rotation.y += 0.0004;
}
this.renderer.render(this.scene, this.camera);
}
});

export { CosmogramScene };
export default CosmogramScene;
