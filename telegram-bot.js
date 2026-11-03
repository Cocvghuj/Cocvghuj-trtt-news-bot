// TELEGRAM BOT - ROKSANA NILLA - AUTONOMOUS PUSH
const BOT_TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"; // BotFather থেকে নিবা
const CHANNEL = "@trttnews24bd"; // তোমার Channel

async function sendToTelegram(msg){
  const url = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
  await fetch(url,{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({chat_id:CHANNEL, text:msg, parse_mode:"HTML"})
  });
}

// Auto send when new idea
(function(){
  var idea = "🚀 <b>ROKSANA NILLA'S VAULT UPDATE</b>\n\n✈️ Sanluri Italy LIVE\n📍 New Idea Added: "+ (document.title||"Autonomous Machine") +"\n🔗 https://trttnews24bd.blogspot.com\n\n#TRTT #Sanluri #RoksanaNilla";
  // Only send once per version
  if(!sessionStorage.getItem('tg-sent')){ 
    console.log("TELEGRAM READY - Call sendToTelegram(idea)");
    // sendToTelegram(idea); // Token বসালে uncomment করবা
    sessionStorage.setItem('tg-sent','1');
  }
})();
