import re,html,sys,subprocess
p=sys.argv[1]; out=sys.argv[2]
t=subprocess.run(['curl','-sL','-m','60','https://api.parliament.uk/historic-hansard/'+p],capture_output=True,text=True).stdout
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
t=re.sub(r"<cite[^>]*>(.*?)</cite>",lambda m:'\n\n### '+re.sub('<[^>]+>','',m.group(1))+'\n',t,flags=re.S)
t=re.sub(r"<a class='permalink column-permalink' id='column_(\w+)'[^>]*>",r' [col \1] ',t)
t=re.sub(r'<p[ >]',lambda m:'\n'+m.group(0),t)
s=html.unescape(re.sub(r'<[^>]+>',' ',t)); s=re.sub(r'[ \t]+',' ',s); s=re.sub(r'\n\s*\n+','\n',s)
open(out,'w').write(s); print(out,len(s.split()))
