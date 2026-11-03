// IDEA 01 - AI CONTENT POLICY - People First
(function(){
  if(document.getElementById('ai-policy-box')) return;
  var box = document.createElement('div');
  box.id = 'ai-policy-box';
  box.innerHTML = "✨ <b>AI Content Policy:</b> This content is helpful, original, and made for people, not for search engines — Bou's Choice Verified ✓";
  box.style.cssText = "max-width:900px;margin:10px auto;padding:10px 14px;background:#fffbe6;border-left:4px solid #FFC300;border-radius:8px;font-size:12px;color:#000;text-align:center;font-family:Arial";
  var vault = document.getElementById('RoksanaFinalVault');
  if(vault) vault.after(box); else document.body.prepend(box);
})();
