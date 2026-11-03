// IP Auto + SubID Lock - Expert Tracking
async function trttLock(baseUrl, type="plane"){
  try{
    const res = await fetch("https://ipapi.co/json/");
    const d = await res.json();
    const c = d.country_code.toLowerCase(); // it, es, de, fr, bd...
    
    let url = new URL(baseUrl);
    url.searchParams.set('subid','trtt_lock_'+c);
    url.searchParams.set('utm_source', type + '_' + c);
    url.searchParams.set('utm_medium','trtt_autonomous');
    url.searchParams.set('utm_campaign','marker_787950');
    
    return url.toString();
  }catch(e){
    let url = new URL(baseUrl);
    url.searchParams.set('subid','trtt_lock_it');
    return url.toString();
  }
}

// USE:
trttLock("https://aviasales.tp.st/Fb8U9yav?marker=787950", "plane_it").then(link => {
  console.log(link); // https://aviasales.tp.st/Fb8U9yav?marker=787950&subid=trtt_lock_it&utm_source=plane_it_it...
  window.open(link, "_blank");
});
