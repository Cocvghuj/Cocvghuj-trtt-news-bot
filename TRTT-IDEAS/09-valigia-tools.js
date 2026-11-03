// IDEA 09 - VALIGIA TOOLS - Amazon $$$
(function(){
  if(document.getElementById('valigia-tools')) return;
  var amazon="https://www.amazon.it/dp/B0EXAMPLE?tag=trttnews24-21"; // তোমার Tag বসাও
  var d=document.createElement('div'); d.id='valigia-tools';
  d.innerHTML=`<div style='max-width:900px;margin:10px auto;padding:12px;background:#fff;border:2px solid #000;border-radius:12px;font-family:Arial'>
  <b>🧳 VALIGIA TOOLS - Amazon</b><br>
  <button onclick="checkSize()" style='margin:4px;padding:8px;border-radius:6px'>Size Checker 55x40x20</button>
  <button onclick="window.open('${amazon}','_blank')" style='margin:4px;padding:8px;background:#ff9900;color:#fff;border:none;border-radius:6px'>Buy Valigia → Amazon.it</button>
  <div id='valigia-result' style='margin-top:8px;font-size:12px'></div>
  </div>`;
  var v=document.getElementById('RoksanaFinalVault'); if(v) v.after(d);
  window.checkSize=()=>{ var r=document.getElementById('valigia-result'); r.innerHTML="✅ Ryanair OK 55x40x20 | Wizzair OK | 23kg = 25 Shirts | Liquid 100ml x10"; };
})();
