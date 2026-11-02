(function(){
 window.__ROKSANA_DONE__=false;
 document.querySelectorAll('#ROKSANA-VAULT,#ROKSANA-VAULT-LOADER').forEach(e=>e.remove());
 var s=document.createElement('script');
 s.src='https://cocvghuj-trtt-news-bot.vercel.app/roksana-vault.js?t='+Date.now()+'&v=final2';
 s.async=true;
 s.onerror=function(){console.log('Vercel fail - trying backup');};
 document.head.appendChild(s);
 console.log('TRTT Loader Final - Loading Vault');
})();
