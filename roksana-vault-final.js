// ROKSANA NILLA'S FINAL VAULT - FINAL LOCKED - STRICT 3 DOMAIN
(function(){
  var ALLOWED = ["trttnews24bd.blogspot.com","trttnews24bd.com","www.trttnews24bd.com"];
  var host = window.location.hostname.toLowerCase().trim();
  if(!ALLOWED.includes(host)){
    console.warn("⛔ Locked: "+host);
    var r=document.getElementById("RoksanaFinalVault");
    if(r) r.innerHTML="<div style='padding:20px;text-align:center;color:red;border:2px solid red'>⛔ TRTT Only</div>";
    return;
  }

  var ROOT_ID="RoksanaFinalVault";
  var root=document.getElementById(ROOT_ID);
  if(!root) return;
  root.innerHTML="";
  root.style.cssText="padding:20px;text-align:center;border:3px solid #ff2e63;border-radius:15px;margin:10px;background:linear-gradient(45deg,#fff,#fff0f5);box-shadow:0 4px 15px rgba(255,46,99,.2)";

  var h=document.createElement("h2");
  h.innerHTML="✨ ROKSANA NILLA'S FINAL VAULT ✨";
  h.style.color="#ff2e63";
  
  var s=document.createElement("p");
  s.innerHTML="Tomar Jonno - This Vault is for You...<br>TRTT VOYAGE - 369 Views";
  s.style.color="#333";

  var box=document.createElement("div");
  box.style.cssText="display:flex;gap:10px;justify-content:center;margin-top:15px";
  box.innerHTML="<div style='width:50px;height:50px;background:#ff2e63;border-radius:50%'></div><div style='width:50px;height:50px;background:#FFC300;border-radius:50%'></div><div style='width:50px;height:50px;background:#AF7AC5;border-radius:50%'></div>";

  var lock=document.createElement("p");
  lock.innerHTML="🔒 Strict Locked - Commit 97a73a7 - Anti Google Kick - TRTT Only";
  lock.style.fontSize="11px";lock.style.color="green";lock.style.marginTop="15px";

  root.appendChild(h);root.appendChild(s);root.appendChild(box);root.appendChild(lock);
  console.log("✅ VAULT LIVE - STRICT LOCKED FOR TRTT");
})();
