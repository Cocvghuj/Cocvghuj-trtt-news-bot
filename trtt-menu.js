// TRTT BRAND MENU - GITHUB VERSION - STRICT LOCK - ROKSANA NILLA
(function(){
  var ALLOWED = ["trttnews24bd.blogspot.com","trttnews24bd.com","www.trttnews24bd.com"];
  var h = location.hostname;
  var ok = ALLOWED.some(d => h===d || h.endsWith("."+d));
  if(!ok){ 
    var b=document.createElement("div");
    b.innerHTML="⛔ TRTT MENU - TRTT Only";
    b.style.cssText="background:red;color:#fff;padding:10px;text-align:center;font-weight:bold";
    document.body.prepend(b);
    return;
  }

  var css = `
  #trtt-menu{ background:#fff; border-bottom:3px solid #ff2e63; box-shadow:0 2px 10px rgba(0,0,0,0.1); position:sticky; top:0; z-index:99999; font-family:Arial }
  #trtt-menu .menu-wrap{ display:flex; align-items:center; justify-content:space-between; padding:10px 15px; max-width:1200px; margin:auto }
  #trtt-menu .logo{ font-weight:bold; font-size:20px; color:#ff2e63 }
  #trtt-menu .links{ display:flex; gap:12px }
  #trtt-menu .links a{ text-decoration:none; color:#333; font-weight:bold; padding:6px 12px; border-radius:20px; transition:0.3s; font-size:14px }
  #trtt-menu .links a:hover{ transform:scale(1.05) }
  #trtt-menu .links a:nth-child(1):hover{ background:#ff2e63; color:#fff }
  #trtt-menu .links a:nth-child(2):hover{ background:#ffc107; color:#000 }
  #trtt-menu .links a:nth-child(3):hover{ background:#9c88ff; color:#fff }
  #trtt-menu .links a:nth-child(4):hover{ background:#00d2a0; color:#fff }
  #trtt-menu .links a:nth-child(5):hover{ background:#ff6b6b; color:#fff }
  #trtt-menu .mobile{ display:none; font-size:24px; cursor:pointer }
  @media(max-width:768px){ #trtt-menu .links{ display:none; flex-direction:column; position:absolute; top:60px; left:0; width:100%; background:#fff; padding:15px; box-shadow:0 5px 10px rgba(0,0,0,0.1) } #trtt-menu .links.show{ display:flex } #trtt-menu .mobile{ display:block } }
  `;
  var style = document.createElement("style");
  style.innerHTML = css;
  document.head.appendChild(style);

  var menuHTML = `
  <div id='trtt-menu'>
    <div class='menu-wrap'>
      <div class='logo'>✨ TRTT VOYAGE</div>
      <div class='links' id='trttLinks'>
        <a href='/'>Home</a>
        <a href='/search/label/TRTT%20News'>TRTT News</a>
        <a href='/search/label/Travel'>Travel</a>
        <a href='/search/label/Voyage'>Voyage Hub</a>
        <a href='/p/about.html'>About</a>
      </div>
      <div class='mobile' onclick='document.getElementById("trttLinks").classList.toggle("show")'>☰</div>
    </div>
  </div>`;

  document.addEventListener("DOMContentLoaded", function(){
    document.body.insertAdjacentHTML("afterbegin", menuHTML);
  });
  if(document.readyState !== "loading"){
    document.body.insertAdjacentHTML("afterbegin", menuHTML);
  }
})();
