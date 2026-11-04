<div id="pro-vault" style="max-width:680px;margin:40px auto;padding:28px;border-radius:18px;background:#FFFBEB;border:2px solid #111;font-family:system-ui">
  <h2 style="text-align:center;margin:0">🔒 ROKSANA VAULT • PRO</h2>
  <p style="text-align:center;font-size:12px;color:#888">AES-256 Encrypted • Sanluri Vault</p>

  <div id="v-lock">
    <input id="v-pass" type="password" placeholder="Vault Password" style="width:100%;padding:14px;border-radius:10px;border:1px solid #ccc;font-size:16px;margin-top:18px">
    <button id="v-btn" style="width:100%;padding:14px;margin-top:12px;border-radius:10px;background:#111;color:#fff;border:none;font-size:16px;cursor:pointer">Unlock</button>
    <p id="v-err" style="display:none;color:#b00;text-align:center">ভুল পাসওয়ার্ড</p>
  </div>

  <div id="v-content" style="display:none;margin-top:22px;padding:20px;background:#fff;border-radius:12px;line-height:1.6"></div>
</div>

<script>
// এখানে তোমার Encrypted Data বসবে - নিচের Generator দিয়ে বানাবে
const VAULT_DATA = "PASTE_YOUR_ENCRYPTED_BLOB_HERE";

async function deriveKey(pass, salt){
  const enc = new TextEncoder();
  const keyMat = await crypto.subtle.importKey("raw", enc.encode(pass), "PBKDF2", false, ["deriveKey"]);
  return crypto.subtle.deriveKey(
    {name:"PBKDF2", salt, iterations:200000, hash:"SHA-256"},
    keyMat, {name:"AES-GCM", length:256}, false, ["decrypt"]
  );
}

document.getElementById('v-btn').onclick = async () => {
  try{
    const pass = document.getElementById('v-pass').value;
    const raw = Uint8Array.from(atob(VAULT_DATA), c=>c.charCodeAt(0));
    const salt = raw.slice(0,16), iv = raw.slice(16,28), data = raw.slice(28);
    const key = await deriveKey(pass, salt);
    const dec = await crypto.subtle.decrypt({name:"AES-GCM", iv}, key, data);
    document.getElementById('v-content').innerHTML = new TextDecoder().decode(dec);
    document.getElementById('v-lock').style.display='none';
    document.getElementById('v-content').style.display='block';
  }catch(e){ document.getElementById('v-err').style.display='block'; }
};
</script>
