// ROKSANA NILLA'S FINAL VAULT - 100% SEPARATE - NO MENU RELATION - BRAND PROTECTED
// Bou's Choice - Golapi #ff2e63 Kathali #FFC300 Piaji #AF7AC5 - Marker HIDDEN
// Based on Your 2 Photos + Video - Professional First News
window.RoksanaVault = {
  show: function() {
    // Secret Marker - Hidden - Never Display
    const _m = '787950';
    
    // Remove old vault if exists
    const old = document.getElementById('ROKSANA-VAULT-LOADER');
    if(old) old.remove();

    let container = document.createElement('div');
    container.id = 'ROKSANA-VAULT-LOADER';
    container.style.cssText = 'position:relative;z-index:1;width:100%;margin:16px 0 24px 0;';

    // Find First News Position - Below Logo/Menu, Above Posts - No Menu Relation
    const main = document.querySelector('.main, #main, .content, #content, .post-feed, .blog-posts, [class*="post"], main');
    const header = document.querySelector('header, #header, .header, .main-header');
    
    if(main){
      main.insertBefore(container, main.firstChild);
    } else if(header && header.nextSibling){
      header.parentNode.insertBefore(container, header.nextSibling);
    } else {
      document.body.insertBefore(container, document.body.firstChild);
    }

    // Scrolling Text - From Your 2nd Video - Engr. Abu Taher
    const ticker = "★ Engr. Abu Taher | Milan, Italy | Dedicated to Roksana, Taifa, Tasrif | Building for Bangladesh | Crafted with Love | Sanluri HQ LIVE | TRTT Family | ";

    container.innerHTML = `
    <article id="vault-separate" style="position:relative;cursor:pointer;border-radius:22px;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,0.08);border:1px solid rgba(0,0,0,0.06);font-family:system-ui;background:#fff;">
      <!-- Scrolling Ticker - Right to Left - Your 2nd Video Style -->
      <div style="background:linear-gradient(90deg,#ff2e63,#FFC300,#AF7AC5);color:#fff;padding:7px 0;overflow:hidden;white-space:nowrap;font-size:10px;font-weight:800;letter-spacing:1.2px;">
        <div style="display:inline-block;animation:scrollLeft 30s linear infinite;will-change:transform;">${ticker.repeat(5)}</div>
      </div>
      
      <!-- Vault Card - Based on Your 1st Photo - Glassmorphism -->
      <div style="position:relative;padding:28px 20px 20px 20px;text-align:center;background:radial-gradient(circle at 20% 20%,rgba(255,46,99,0.08),transparent 50%),radial-gradient(circle at 80% 70%,rgba(175,122,197,0.12),transparent 50%),linear-gradient(180deg,#ffffff 0%,#fffafc 100%);">
        
        <!-- Small Top - Bou's Choice -->
        <div style="font-size:10px;color:#ff2e63;letter-spacing:2.5px;font-weight:700;opacity:0.9;margin-bottom:10px;">♡ Roksana Nilla's Final Vault - তোমার জন্য ♡</div>
        
        <!-- Golden Lock - From 1st Photo -->
        <div style="width:80px;height:80px;margin:14px auto;background:linear-gradient(145deg,#FFD700 0%,#FFC300 50%,#FFB000 100%);border-radius:18px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 24px rgba(255,195,0,0.35), inset 0 2px 0 rgba(255,255,255,0.7);border:1.5px solid #FFC300;position:relative;">
          <div style="position:absolute;inset:-4px;border-radius:20px;background:linear-gradient(90deg,#ff2e63,#FFC300,#AF7AC5);filter:blur(10px);opacity:0.25;z-index:-1;"></div>
          <span style="font-size:38px;filter:drop-shadow(0 2px 4px rgba(0,0,0,0.2));">🔒</span>
        </div>
        
        <!-- Title - From 1st Photo -->
        <h2 style="margin:14px 0 6px 0;font-weight:900;font-size:24px;letter-spacing:0.5px;line-height:1.15;">
          <span style="color:#6b4a00;">ROKSANA NILLA'S</span><br>
          <span style="color:#6b4a00;">FINAL VAULT</span>
        </h2>
        
        <div style="font-size:13px;color:#777;font-style:italic;margin:8px 0 14px 0;letter-spacing:0.3px;">This Vault is for You...</div>
        
        <!-- Divider -->
        <div style="width:90px;height:1.5px;background:linear-gradient(90deg,transparent,#AF7AC5,transparent);margin:16px auto;"></div>
        
        <!-- Bottom - Secured Live Encrypted - From 1st Photo -->
        <div style="font-size:10.5px;color:#888;line-height:1.7;">
          Sanluri, Italy LIVE - Secured with Love - Abu Taher
          <div style="margin-top:12px;display:flex;justify-content:center;gap:8px;">
            <span style="background:#fff;color:#ff2e63;border:1px solid rgba(255,46,99,0.18);padding:4px 12px;border-radius:20px;font-size:8.5px;letter-spacing:1px;font-weight:700;">SECURED</span>
            <span style="background:#fff;color:#b78a00;border:1px solid rgba(255,195,0,0.2);padding:4px 12px;border-radius:20px;font-size:8.5px;letter-spacing:1px;font-weight:700;">LIVE</span>
            <span style="background:#fff;color:#7a4a8a;border:1px solid rgba(175,122,197,0.2);padding:4px 12px;border-radius:20px;font-size:8.5px;letter-spacing:1px;font-weight:700;">ENCRYPTED</span>
          </div>
        </div>
        
        <!-- Bou's Colors - Dots - Professional -->
        <div style="display:flex;justify-content:center;gap:7px;margin-top:18px;opacity:0.9;">
          <span title="Golapi" style="width:9px;height:9px;border-radius:50%;background:#ff2e63;box-shadow:0 0 10px rgba(255,46,99,0.5)"></span>
          <span title="Kathali" style="width:9px;height:9px;border-radius:50%;background:#FFC300;box-shadow:0 0 10px rgba(255,195,0,0.5)"></span>
          <span title="Piaji" style="width:9px;height:9px;border-radius:50%;background:#AF7AC5;box-shadow:0 0 10px rgba(175,122,197,0.5)"></span>
        </div>
      </div>
      
      <!-- Bottom Line - From 2nd Photo Watercolor Accent -->
      <div style="height:4px;background:linear-gradient(90deg,#ff2e63,#FFC300,#AF7AC5,#ff2e63);opacity:0.7;"></div>
    </article>
    <style>
      @keyframes scrollLeft{0%{transform:translateX(15%)}100%{transform:translateX(-85%)}}
      #vault-separate:hover{transform:translateY(-3px);box-shadow:0 18px 50px rgba(0,0,0,0.12);transition:all 0.35s cubic-bezier(0.2,0.8,0.2,1);}
      #ROKSANA-VAULT-LOADER{position:relative!important;top:auto!important;}
    </style>`;

    // Click Tracking - You Will Get - Separate from Menu
    const vaultEl = document.getElementById('vault-separate');
    if(vaultEl){
      vaultEl.onclick = function(){
        fetch('https://cocvghuj-trtt-news-bot.vercel.app/api/vault-click?t='+Date.now()+'&m='+_m)
          .then(()=>console.log('Vault Separate Clicked - Marker Hidden'))
          .catch(()=>{});
        window.open('https://cocvghuj-trtt-news-bot.vercel.app','_blank');
      };
    }
  }
};

// Auto Show - No Config Needed - 100% Separate
if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', ()=>{ window.RoksanaVault.show(); });
} else {
  window.RoksanaVault.show();
}
