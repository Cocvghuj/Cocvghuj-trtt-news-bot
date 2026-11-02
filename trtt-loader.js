// TRTT MASTER LOADER - Blog Control to GitHub - One Time Install
(async function(){
  const script = document.getElementById('trtt-master-key');
  const configUrl = script.dataset.config + '?t=' + Date.now(); // Cache bypass
  try{
    const res = await fetch(configUrl);
    const config = await res.json();
    
    // 1. Theme Control - গোলাপি, কাঁঠালি, পেঁয়াজি
    if(config.theme){
      const style = document.createElement('style');
      style.innerHTML = `
        :root{--golapi:${config.theme.golapi};--kathali:${config.theme.kathali};--piaji:${config.theme.piaji}}
        .LinkList,.PageList,#main-menu{display:none !important}
        body{background:${config.theme.bodyBg} !important}
        #trtt-dynamic-menu{background:linear-gradient(90deg, ${config.theme.golapi}, ${config.theme.piaji}, ${config.theme.kathali}) !important}
      `;
      document.head.appendChild(style);
    }
    // 2. Menu Control - 1-Click Yahoo Menu
    if(config.menu){
      let root = document.getElementById('trtt-dynamic-menu');
      if(!root){
        root = document.createElement('div'); root.id='trtt-dynamic-menu';
        const h=document.querySelector('header,.header,#header');
        if(h) h.parentNode.insertBefore(root, h.nextSibling);
        else document.body.prepend(root);
      }
      // Get user interest from localStorage
      const scores = JSON.parse(localStorage.getItem('trtt_scores')||'{}');
      const sorted = [...config.menu].sort((a,b)=>(scores[b.id]||0)-(scores[a.id]||0));
      
      root.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;padding:0 15px;height:54px;max-width:1300px;margin:0 auto">
          <div style="color:#fff;font-weight:900">${config.logo||'TRTT VOYAGE'}</div>
          <div style="display:flex;gap:5px">${sorted.map(m=>`
            <a href="${m.href}" data-id="${m.id}" style="color:#fff;padding:10px 14px;text-decoration:none;font-weight:600;background:${scores[m.id]>0?m.color:'transparent'};border-radius:20px">
              ${m.icon||''} ${m.label} ${scores[m.id]>0?'<small style="background:#000;color:#fff;padding:2px 6px;border-radius:10px">Your Interest</small>':''}
            </a>`).join('')}
          </div>
        </div>
      `;
      root.querySelectorAll('a').forEach(a=>{
        a.addEventListener('click', ()=>{
          const s=JSON.parse(localStorage.getItem('trtt_scores')||'{}');
          s[a.dataset.id]=(s[a.dataset.id]||0)+1;
          localStorage.setItem('trtt_scores', JSON.stringify(s));
        });
      });
    }
    console.log('TRTT Blog Control: GitHub Active -', config.version);
  }catch(e){ console.error('TRTT Control Failed', e); }
})();
