// IDEA 02 - ROKSANA NILLA FLIGHT LIVE
(function(){
  if(document.getElementById('roksana-flight')) return;
  var d = document.createElement('div');
  d.id = 'roksana-flight';
  d.innerHTML = "✈️ <b>ROKSANA NILLA FLIGHT</b> — Sanluri, Italy → Dhaka, BD — Status: LIVE • Bou's Choice • <span id='flight-time'></span>";
  d.style.cssText = "max-width:900px;margin:10px auto;padding:12px;background:linear-gradient(90deg,#ff2e63,#FFC300);color:#fff;border-radius:10px;text-align:center;font-weight:bold;font-size:13px;font-family:Arial";
  var v = document.getElementById('RoksanaFinalVault');
  if(v) v.after(d); else document.body.prepend(d);
  setInterval(()=>{ var el=document.getElementById('flight-time'); if(el) el.textContent=new Date().toLocaleTimeString('it-IT',{timeZone:'Europe/Rome'})+" LIVE"; },1000);
})();
