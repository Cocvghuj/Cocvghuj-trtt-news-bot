// IDEA 04 - FREE TOOL = MICROSOFT STRATEGY
(function(){
  if(document.getElementById('free-tool')) return;
  var b=document.createElement('div');
  b.id='free-tool';
  b.innerHTML="<div style='padding:12px;background:#fff;border:2px solid #ff2e63;border-radius:12px;text-align:center;max-width:900px;margin:10px auto;font-family:Arial'><b>✈️ FREE Flight Price Checker — Sanluri to Anywhere</b><br><small>Powered by GitHub - Your Brain</small><br><input id='fromCity' placeholder='From: Cagliari' style='padding:8px;margin:6px;border-radius:6px;border:1px solid #ccc'><input id='toCity' placeholder='To: Dhaka' style='padding:8px;margin:6px;border-radius:6px;border:1px solid #ccc'><button onclick='window.open(\"https://www.aviasales.com/?marker=TRTT\",\"_blank\")' style='background:#ff2e63;color:#fff;padding:8px 14px;border:none;border-radius:6px;font-weight:bold'>Check Price FREE</button></div>";
  var v=document.getElementById('RoksanaFinalVault'); if(v) v.after(b);
})();
