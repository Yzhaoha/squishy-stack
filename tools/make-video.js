// Record the CrazyGames preview videos from bot play, frame by frame (crisp, 30 fps, no sound).
// usage: node tools/make-video.js [out dir = submission]      (needs playwright + ffmpeg)
// writes preview-1920x1080.mp4 and preview-1080x1620.mp4. If art/final/squishy-stack-cg-1920x1080.png
// and ...-800x1200.png exist, 0.8 s of the cover is put in front (CrazyGames wants the cover as first frame).
const {chromium}=require('playwright'),fs=require('fs'),path=require('path'),{execFileSync}=require('child_process'),os=require('os');
const root=path.join(__dirname,'..'),out=path.resolve(process.argv[2]||path.join(root,'submission'));fs.mkdirSync(out,{recursive:true});
const FPS=30;
// [level index, what to wait for before recording (floor count or 'fever'), seconds to record]
const CLIPS=[[3,5,3],[5,'fever',3],[12,7,3],[16,6,3],[22,6,3],[21,'dark',3]]; // pals+birds, fever, sliding base, cafe coins, bouncy cloud, flickering light
(async()=>{const b=await chromium.launch({args:['--no-sandbox']});
 for(const [w,h] of [[1920,1080],[1080,1620]]){
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'sqvid-'));let n=0;
  const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
  await p.addInitScript(()=>{localStorage.setItem('sqs_lang','"en"');localStorage.setItem('sqs_mute','true');window.__sqManual=true});
  await p.goto('file://'+path.join(root,'index.html'));await p.waitForTimeout(800);
  await p.addStyleTag({content:'#tip,#pauseB,#mute,#lang{display:none!important}'});
  const tick=()=>p.evaluate(()=>{const G=__sq.G;for(let i=0;i<2;i++){if(G.state==='pick')__sq.choose(0);__sq.step(1/60)}__sq.render();return{floor:G.floor,fever:G.fever>0,dark:Math.sin(G.time*1.15-1.2)>0.35,over:G.state!=='play'&&G.state!=='pick'}});
  for(const [lv,until,len] of CLIPS){
   for(let tries=0;tries<8;tries++){
    await p.evaluate(i=>{__sq.setTut(true);__sq.startRun({mode:'level',idx:i});__sq.G.auto=true;__sq.G.botSkill=0.012},lv);
    let ok=false;for(let k=0;k<FPS*60;k++){const s=await tick();if(s.over)break;if(until==='fever'?s.fever:until==='dark'?s.dark&&s.floor>=4:s.floor>=until){ok=true;break}}
    if(ok)break}
   for(let k=0;k<Math.round(len*FPS);k++){await tick();await p.screenshot({path:path.join(dir,'f'+String(n++).padStart(5,'0')+'.png')})}
   console.log(w+'x'+h,'level',lv+1,'frames so far',n)}
  await p.close();
  const f=path.join(out,`preview-${w}x${h}.mp4`);
  execFileSync('ffmpeg',['-y','-loglevel','error','-framerate',String(FPS),'-i',path.join(dir,'f%05d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','slow','-movflags','+faststart','-an',f]);
  fs.rmSync(dir,{recursive:true,force:true});
  const cover=path.join(root,'art','final',w>h?'squishy-stack-cg-1920x1080.png':'squishy-stack-cg-800x1200.png');
  if(fs.existsSync(cover)){const tmp=f.replace('.mp4','.tmp.mp4');fs.renameSync(f,tmp);
   execFileSync('ffmpeg',['-y','-loglevel','error','-loop','1','-framerate',String(FPS),'-t','0.8','-i',cover,'-i',tmp,'-filter_complex',`[0:v]scale=${w}:${h}:flags=lanczos,setsar=1,format=yuv420p[a];[1:v]setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]`,'-map','[v]','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','slow','-movflags','+faststart','-an',f]);
   fs.rmSync(tmp)}
  console.log('wrote',f,(fs.statSync(f).size/1e6).toFixed(1)+' MB')}
 await b.close()})();
