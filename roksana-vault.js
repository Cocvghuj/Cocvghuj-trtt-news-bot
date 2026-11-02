window.RoksanaVault={
 show:function(){
  let c=document.createElement('div');
  c.id='ROKSANA-VAULT';
  c.style='margin:18px 0;';
  c.innerHTML=`
<div style="border-radius:22px;overflow:hidden;background:#fff;border:1px solid #ddd;">
<div style="background:#111;color:#FFD700;padding:6px;font-size:9px;white-space:nowrap;overflow:hidden;">
★ Engr Abu Taher | Milan Italy | Dedicated to Roksana Taifa Tasrif |
</div>
<div style="background:linear-gradient(90deg,#ff2e63,#FFC300,#AF7AC5);color:#fff;padding:5px;font-size:9px;font-weight:900;">
ROKSANA TAIFA TASRIF • ROKSANA TAIFA TASRIF •
</div>
<div style="padding:20px;text-align:center;">
<div style="display:flex;gap:8px;justify-content:center;margin-bottom:12px;">
<div style="flex:1;background:#ff2e63;border-radius:10px;padding:12px;color:#fff;font-weight:900;">Golapi<br><small>#ff2e63</small></div>
<div style="flex:1;background:#FFC300;border-radius:10px;padding:12px;color:#000;font-weight:900;">Kathali<br><small>#FFC300</small></div>
<div style="flex:1;background:#AF7AC5;border-radius:10px;padding:12px;color:#fff;font-weight:900;">Piaji<br><small>#AF7AC5</small></div>
</div>
<div style="color:#ff2e63;font-size:10px;">♡ Roksana Nilla's Final Vault - তোমার জন্য ♡</div>
<div style="width:70px;height:70px;margin:12px auto;background:linear-gradient(145deg,#FFD700,#FFC300);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:32px;">🔒</div>
<h2 style="font-weight:900;font-size:20px;color:#3a2a00;">ROKSANA NILLA'S<br>FINAL VAULT</h2>
<div id="rt" style="margin:12px auto;max-width:500px;background:#f5f5f5;border-radius:10px;padding:8px 12px;text-align:left;font-family:monospace;font-size:11px;color:#5a2a8a;">Loading...</div>
<div style="font-size:10px;color:#888;margin-top:10px;">Sanluri Italy LIVE - <span id="st">--:--:--</span></div>
</div>
<div style="height:4px;background:linear-gradient(90deg,#ff2e63,#FFC300,#AF7AC5);"></div>
</div>`;
  let t=document.querySelector('.blog-posts,main,#main');
  if(t) t.insertBefore(c,t.firstChild);
  else document.body.insertBefore(c,document.body.firstChild);
  function up(){
   let n=new Date();
   let s=n.toLocaleTimeString('en-GB',{timeZone:'Europe/Rome',hour12:false});
   let e=document.getElementById('st');
   if(e) e.textContent=s;
  }
  setInterval(up,1000);up();
  async function lt(){
   try{
    let r=await fetch('https://cocvghuj-trtt-news-bot.vercel.app/api/roksana-thinking?t='+Date.now());
    let j=await r.json();
    let e=document.getElementById('rt');
    if(e&&j.thinking) e.textContent=j.thinking;
   }catch(e){}
  }
  lt();setInterval(lt,6000);
 }
};
if(document.readyState==='loading'){
 document.addEventListener('DOMContentLoaded',()=>window.RoksanaVault.show());
}else{
 window.RoksanaVault.show();
}
