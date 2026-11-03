// TRTT PRO LOCK - GitHub Version - Marker 787950
const MARKER="787950";
const PROGRAMS={
 Aviasales:`https://aviasales.tp.st/Fb8U9yav?marker=${MARKER}`,
 Klook:`https://klook.tp.st/TWKnemhz?marker=${MARKER}`,
 Airalo:`https://airalo.tp.st/ZZoQC7Mz?marker=${MARKER}`,
 Saily:`https://saily.tp.st/ssekmS4X?marker=${MARKER}`,
 Yesim:`https://yesim.tp.st/krzFKLpg?marker=${MARKER}`,
 Drimsim:`https://drimsim.tp.st/Ly7ywIY8?marker=${MARKER}`,
 Kiwitaxi:`https://kiwitaxi.tp.st/tIZcbMOB?marker=${MARKER}`, // FIXED tl->tI
 Trip:`https://trip.tp.st/h3LrTZcS?marker=${MARKER}`,
 Tiqets:`https://tiqets.tp.st/bnx8pnF6?marker=${MARKER}`,
 AirHelp:`https://airhelp.tp.st/3ItXS0E4?marker=${MARKER}`
};

async function init(){
  let res=await fetch("https://ipapi.co/json/").catch(()=>({country_code:"IT"}));
  let d=res.json?await res.json():res;
  const c = (d.country_code||"IT").toLowerCase();
  let html="";
  for(let k in PROGRAMS){
    let url=new URL(PROGRAMS[k]);
    url.searchParams.set('subid','trtt_lock_'+c);
    url.searchParams.set('utm_source','gh_'+c);
    html+=`<p><a href="${url}" target="_blank" style="color:#FFC300">${k} - ${url}</a></p>`;
  }
  document.getElementById('links').innerHTML=html;
  console.log("PRO LOCK ACTIVE -",c);
}
init();
