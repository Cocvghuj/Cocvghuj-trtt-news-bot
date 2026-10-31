// TRTT Direct Post - AI Safety Lock - PIN 7879 - Sanluri Confirm - Marker 787950 Locked
(function(){
  if(window.TRTT_DIRECT_POST_LOADED) return; window.TRTT_DIRECT_POST_LOADED = true;
  const CONFIG = { BLOG_SECRET_EMAIL: 'engrtaher2017.trttnews24bd@blogger.com', MARKER: '787950', PIN: '7879', BLOG_NAME: 'trttnews24bd', LOCATION: 'Sanluri' };
  window.trttDirectPost = function(topic, htmlContent) {
    const badWords = ['sex','porn','casino','crypto scam']; if(badWords.some(w => topic.toLowerCase().includes(w))){ alert('⛔ Blocked: খারাপ টপিক!'); return false; }
    const pin = prompt('🔒 TRTT Direct Post?\n\nTopic: ' + topic + '\n\nPIN দে (7879):'); if(pin !== CONFIG.PIN){ alert('❌ Wrong PIN!'); return false; }
    if(!confirm('✅ Sanluri থেকে Confirm করছিস?\n\n📌 ' + topic + '\n📧 Post to: ' + CONFIG.BLOG_NAME)){ return false; }
    const subject = topic.substring(0,100); const body = htmlContent || `<div>${subject} - Marker ${CONFIG.MARKER}</div>`;
    try{ const mailtoLink = `mailto:${CONFIG.BLOG_SECRET_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`; window.open(mailtoLink, '_blank'); alert('✅ Approved from Sanluri! Email: ' + CONFIG.BLOG_SECRET_EMAIL); return true; }catch(e){ alert('Error: '+e); return false; }
  };
})();
