// IDEA 07 - TELEGRAM BUTTON
(function(){
  if(document.getElementById('tg-btn')) return;
  var d=document.createElement('div');
  d.id='tg-btn';
  d.innerHTML="<div style='max-width:900px;margin:10px auto;text-align:center'><a href='https://t.me/trttnews24bd' target='_blank' style='background:#0088cc;color:#fff;padding:10px 18px;border-radius:25px;text-decoration:none;font-family:Arial;font-weight:bold;font-size:13px'>📲 Join Telegram — Roksana Nilla Flight LIVE</a></div>";
  var v=document.getElementById('RoksanaFinalVault'); if(v) v.after(d);
})();
