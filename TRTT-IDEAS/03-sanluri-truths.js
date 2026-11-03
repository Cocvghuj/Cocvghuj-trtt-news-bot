// IDEA 03 - SANLURI TRUTH - Google 1st Rank
(function(){
  const TRUTHS = [
    "Sanluri to Cagliari cheapest bus €5 - ARST Line 124 - 1hr",
    "Cagliari Airport to Sanluri - Bus + Train €6.50 - 90min",
    "Best eSIM Italy cheap - Iliad €9.99 - Sanluri Vodafone store",
    "Ryanair luggage FREE trick - Under seat bag 40x20x25",
    "Sanluri Italy LIVE - No Booking.com knows this"
  ];
  if(document.getElementById('sanluri-truth')) return;
  var box = document.createElement('div');
  box.id = 'sanluri-truth';
  box.innerHTML = "📍 <b>SANLURI TRUTH:</b> " + TRUTHS[Math.floor(Math.random()*TRUTHS.length)] + " — Verified by Roksana Nilla, Sanluri Italy LIVE";
  box.style.cssText = "max-width:900px;margin:10px auto;padding:10px;background:#0d001a;color:#FFC300;border:1px solid gold;border-radius:10px;text-align:center;font-size:12px;font-family:Arial";
  var v=document.getElementById('RoksanaFinalVault'); if(v) v.after(box);
})();
