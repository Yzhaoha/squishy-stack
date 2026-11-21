#!/usr/bin/env python3
"""Build the CrazyGames version from the test build (index.html at the repo root).

- adds the CrazyGames SDK v3 and a small adapter that offers the PokiSDK-shaped
  interface the game already uses (init, gameLoadingFinished, gameplayStart/Stop,
  commercialBreak, rewardedBreak), plus platform mute and player locale via window.__sqHost
- BUILD='test' -> BUILD='cg' (no SDK = rewarded ads give no reward)
- strips the /*TEST*/ ... /*ENDTEST*/ hooks (?auto, window.__sq)

Writes dist/crazygames/index.html and dist/squishy-stack-crazygames.zip (index.html at the zip root).
"""
import os, re, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SDK_URL = 'https://sdk.crazygames.com/crazygames-sdk-v3.js'
CG = r'''<script src="https://sdk.crazygames.com/crazygames-sdk-v3.js"></script>
<script>
/* CrazyGames v3 adapter: exposes the PokiSDK-shaped interface the game uses */
(function(){
var sdk=null,ready=null;
function body(){return new Promise(function(r){if(document.body)r();else document.addEventListener('DOMContentLoaded',function(){r()},{once:true})})}
function host(){return window.__sqHost}
function ad(type,onStart){return new Promise(function(res){
  if(!sdk){res(false);return}
  try{sdk.ad.requestAd(type,{
    adStarted:function(){try{onStart&&onStart()}catch(e){}},
    adFinished:function(){res(true)},
    adError:function(){res(false)}})}catch(e){res(false)}})}
window.PokiSDK={
  init:function(){
    if(ready)return ready;
    ready=body().then(function(){
      if(!window.CrazyGames||!CrazyGames.SDK)throw new Error('no sdk');
      return CrazyGames.SDK.init().then(function(){sdk=CrazyGames.SDK})
    }).then(function(){
      try{sdk.game.loadingStart()}catch(e){}
      try{var h=host(),st=sdk.game.settings;if(h&&st)h.setPlatMute(!!st.muteAudio);
          sdk.game.addSettingsChangeListener(function(n){var h=host();if(h&&n)h.setPlatMute(!!n.muteAudio)})}catch(e){}
      try{var loc=sdk.user&&sdk.user.systemInfo&&sdk.user.systemInfo.locale;var h2=host();if(loc&&h2)h2.setLang(loc)}catch(e){}
    }).catch(function(){sdk=null});
    return ready},
  gameLoadingFinished:function(){try{sdk&&sdk.game.loadingStop()}catch(e){}},
  gameplayStart:function(){try{sdk&&sdk.game.gameplayStart()}catch(e){}},
  gameplayStop:function(){try{sdk&&sdk.game.gameplayStop()}catch(e){}},
  commercialBreak:function(before){return ad('midgame',before).then(function(){})},
  rewardedBreak:function(before){return ad('rewarded',before)}
};
})();
</script>'''

src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
out = src
assert out.count('<title>') == 1 and out.count("const BUILD='test';") == 1
out = out.replace('<title>', CG + '\n<title>', 1)
out = out.replace("const BUILD='test';", "const BUILD='cg';", 1)
out, n = re.subn(r'/\*TEST\*/.*?/\*ENDTEST\*/\n?', '', out, flags=re.S)
assert n == 1, 'test block not found'
assert '__sq=' not in out and 'G.auto=true' not in out and '__sqHost' in out
urls = set(re.findall(r'https?://[^"\'\s)<>]+', out))
assert urls == {SDK_URL}, urls

d = os.path.join(ROOT, 'dist', 'crazygames')
os.makedirs(d, exist_ok=True)
open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)
zp = os.path.join(ROOT, 'dist', 'squishy-stack-crazygames.zip')
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('index.html', out)
print('dist/crazygames/index.html', len(out.encode()) // 1024, 'KB;', os.path.relpath(zp, ROOT), os.path.getsize(zp) // 1024, 'KB')
