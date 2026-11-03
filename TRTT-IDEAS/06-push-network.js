// IDEA 06 - AUTONOMOUS PUSH NETWORK
(function(){
  if(document.getElementById('push-net')) return;
  var p=document.createElement('div');
  p.id='push-net';
  p.innerHTML="<div style='max-width:900px;margin:10px auto;padding:10px;background:linear-gradient(90deg,#AF7AC5,#ff2e63);color:#fff;border-radius:10px;text-align:center;font-family:Arial;font-size:12px'>🔔 <b>AUTONOMOUS PUSH NETWORK</b> — Roksana Nilla LIVE — <button id='push-btn' style='background:#fff;color:#ff2e63;border:none;padding:6px 12px;border-radius:20px;font-weight:bold;margin-left:8px'>Enable Push</button></div>";
  var v=document.getElementById('RoksanaFinalVault'); if(v) v.after(p);
  document.getElementById('push-btn').onclick=()=>{
    if("Notification" in window){
      Notification.requestPermission().then(perm=>{
        if(perm==="granted"){ new Notification("TRTT News 24 BD — Roksana Nilla LIVE from Sanluri Italy ✈️"); document.getElementById('push-btn').textContent="PUSH ACTIVE ✓"; }
      });
    }
  };
  // Auto push when new idea added
  if(!localStorage.getItem('trtt-push')){ localStorage.setItem('trtt-push','active'); }
})();
