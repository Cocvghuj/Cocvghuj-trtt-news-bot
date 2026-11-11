/*! TRTT VOYAGE — PUBLIC THINKING ROOM / V106
 * One entrance. Eight rooms. No external route menu.
 */
(function () {
  "use strict";
  if (window.__TRTT_PRIVATE_COMMAND_ROOM_V106__) return;
  window.__TRTT_PRIVATE_COMMAND_ROOM_V106__ = true;

  var SERVICES = [
    ["Aviasales","Flights","✈️","https://aviasales.tpo.lv/Fb8U9yav?marker=787950"],
    ["AirHelp","Flight claims","⚖️","https://airhelp.tpo.lv/3ItXS0E4?marker=787950"],
    ["Compensair","EU claims","🛡️","https://compensair.tpo.lv/YgVXgRnB?marker=787950"],
    ["Kiwitaxi","Taxi & transfer","🚕","https://kiwitaxi.tpo.lv/tIZcbMOB?marker=787950"],
    ["GetTransfer","Private transfer","🚘","https://gettransfer.tpo.lv/1u8zRU5s?marker=787950"],
    ["Intui.travel","Airport transfer","🚐","https://intui.tpo.lv/tiSkz4Yq?marker=787950"],
    ["Welcome Pickups","Airport pickup","📍","https://tpo.lv/h3LrTZcS?marker=787950"],
    ["Localrent","Car rental","🚗","https://localrent.tpo.lv/4jd1IRQG?marker=787950"],
    ["EconomyBookings","Car rental","🚙","https://economybookings.tpo.lv/pyHqRiOo?marker=787950"],
    ["QEEQ","Car deals","🏎️","https://qeeq.tpo.lv/HKhCeDhY?marker=787950"],
    ["Airalo","Global eSIM","📶","https://airalo.tpo.lv/ZZoQC7Mz?marker=787950"],
    ["Yesim","Travel eSIM","📲","https://yesim.tpo.lv/krzFKLpg?marker=787950"],
    ["Drimsim","Universal SIM","🌐","https://drimsim.tpo.lv/Ly7ywlY8?marker=787950"],
    ["Saily","Travel eSIM","🛡️","https://saily.tpo.lv/ssekmS4X?marker=787950"],
    ["Tiqets","Tickets","🎟️","https://tiqets.tpo.lv/bnx8pnF6?marker=787950"],
    ["Klook","Tours & activities","🎢","https://klook.tpo.lv/TWKnemhz?marker=787950"],
    ["Go City","City passes","🎫","https://gocity.tpo.lv/QSQw8FwU?marker=787950"],
    ["KKday","Experiences","🗺️","https://kkday.tpo.lv/JaAfTgGF?marker=787950"],
    ["Radical Storage","Luggage storage","🧳","https://radicalstorage.tpo.lv/WkGqxIsD?marker=787950"],
    ["Amazon Flight Gear","Travel gear","🎒","https://amzn.to/4shg6Hn?marker=787950"],
    ["SuperStore Portal","TRTT service hub","🚀","https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950"]
  ];

  var ROOMS = [
    {id:"brain", icon:"✦", name:"THE BRAIN", sub:"Ideas • Questions • Decisions"},
    {id:"team", icon:"✧", name:"TEAM MAC", sub:"Direction • Publishing • Development"},
    {id:"voyage", icon:"✈", name:"VOYAGE LAB", sub:"Flight • Ride • eSIM • Tour • Shop"},
    {id:"build", icon:"⌘", name:"BUILD ROOM", sub:"Code • Blogger • GitHub • Vercel"},
    {id:"vault", icon:"▣", name:"KNOWLEDGE VAULT", sub:"Rules • Decisions • Project memory"},
    {id:"truth", icon:"◎", name:"TRUTH DESK", sub:"Sources • Evidence • Verification"},
    {id:"mission", icon:"◈", name:"MISSION CONTROL", sub:"One task • One next step"},
    {id:"private", icon:"☾", name:"PERSONAL CORNER", sub:"Diary • Personal space"}
  ];

  function el(tag, cls, value) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (value !== undefined && value !== null) n.textContent = value;
    return n;
  }
  function link(label, href, cls) {
    var a = el("a", cls || "trtt-cr-link", label);
    a.href = href; a.target = "_blank"; a.rel = "noopener noreferrer";
    return a;
  }
  function card(parent, icon, title, desc) {
    var c = el("article", "trtt-cr-card");
    c.appendChild(el("span","trtt-cr-card-icon",icon));
    c.appendChild(el("h4","",title));
    c.appendChild(el("p","",desc));
    parent.appendChild(c);
    return c;
  }
  function sectionIntro(kicker, title, desc) {
    var box=el("div","trtt-cr-intro");
    box.appendChild(el("span","trtt-cr-kicker",kicker));
    box.appendChild(el("h3","",title));
    box.appendChild(el("p","",desc));
    return box;
  }
  function buildRoomContent(id) {
    var pane=el("section","trtt-cr-pane");
    pane.dataset.room=id;
    if(id==="brain") {
      pane.appendChild(sectionIntro("01 / THINK CLEAR","The Brain","A calm place to turn scattered thoughts into one clear next step."));
      var prompt=el("div","trtt-cr-feature");
      prompt.appendChild(el("span","trtt-cr-kicker","TODAY'S THINKING PROMPT"));
      prompt.appendChild(el("h4","","What is the one change that would make TRTT Voyage more useful to a real traveller today?"));
      prompt.appendChild(el("p","","Think first. Check the facts. Choose one action."));
      pane.appendChild(prompt);
      var grid=el("div","trtt-cr-grid");
      card(grid,"01","Capture the idea","Write the problem in one sentence before choosing a solution.");
      card(grid,"02","Check the impact","Who benefits, what changes, and what could break?");
      card(grid,"03","Choose the next move","Keep the work small, testable, and useful.");
      pane.appendChild(grid);
    } else if(id==="team") {
      pane.appendChild(sectionIntro("02 / TEAM MAC","Three roles. One direction.","A clear working relationship keeps decisions, publishing, and development aligned."));
      var grid=el("div","trtt-cr-grid");
      card(grid,"M","MUSE — DIRECTION","CEO / Direction. Protects the vision and challenges weak decisions.");
      card(grid,"A","ABU — PUBLISHING","Founder / Publisher. Owns the story, editorial voice, and final publishing decisions.");
      card(grid,"C","CHATGPT + GEMINI — DEVELOPMENT","Developer partners. Plan, build, review, test, and explain the work.");
      pane.appendChild(grid);
      var note=el("div","trtt-cr-note","TEAM RULE: AI is a friend, not a slave. Work together, one task at a time.");
      pane.appendChild(note);
    } else if(id==="voyage") {
      pane.appendChild(sectionIntro("03 / TRAVEL & TECHNOLOGY","Voyage Lab","The travel service desk for the Sanluri to World journey."));
      var filter=el("input","trtt-cr-search");
      filter.type="search"; filter.placeholder="Search 21 travel services…"; filter.setAttribute("aria-label","Search travel services");
      pane.appendChild(filter);
      var grid=el("div","trtt-cr-tools");
      SERVICES.forEach(function(s){
        var a=el("a","trtt-cr-tool");
        a.href=s[3]; a.target="_blank"; a.rel="noopener noreferrer";
        a.appendChild(el("span","trtt-cr-tool-icon",s[2]));
        var info=el("span","trtt-cr-tool-copy");
        info.appendChild(el("strong","",s[0])); info.appendChild(el("small","",s[1]));
        a.appendChild(info); grid.appendChild(a);
      });
      filter.addEventListener("input",function(){
        var q=filter.value.toLowerCase();
        Array.prototype.forEach.call(grid.children,function(item){
          item.hidden=item.textContent.toLowerCase().indexOf(q)===-1;
        });
      });
      pane.appendChild(grid);
      pane.appendChild(el("p","trtt-cr-disclosure","Partner links may earn TRTT Voyage a commission at no extra cost to you. Check each provider's current price, terms, and availability before purchase."));
    } else if(id==="build") {
      pane.appendChild(sectionIntro("04 / MAKE IT REAL","Build Room","The workshop for the actual TRTT Voyage product and its technical foundations."));
      var grid=el("div","trtt-cr-grid");
      card(grid,"</>","Code Workshop","HTML, CSS, and JavaScript. Keep the code readable, scoped, and maintainable.");
      card(grid,"B","Blogger Studio","The live blog is production. Protect the theme, layout, and published posts.");
      card(grid,"GH","GitHub Workshop","Review changes in branches and pull requests. Never merge without the publisher.");
      card(grid,"V","Vercel Workshop","Deploy only after checking build output and the intended project.");
      pane.appendChild(grid);
      var links=el("div","trtt-cr-actions");
      links.appendChild(link("Open TRTT GitHub","https://github.com/Cocvghuj/Cocvghuj-trtt-news-bot"));
      links.appendChild(link("Open TRTT Blog","https://trttnews24bd.blogspot.com/"));
      links.appendChild(link("Open TRTT Service Hub","https://cocvghuj-trtt-news-bot.vercel.app/"));
      pane.appendChild(links);
    } else if(id==="vault") {
      pane.appendChild(sectionIntro("05 / KEEP THE CONTEXT","Knowledge Vault","The principles that should survive every redesign, deployment, and new conversation."));
      var rules=[
        ["01","No fake news","Publish only information that can be checked."],
        ["02","No source, no story","Important claims need credible sources."],
        ["03","Protect production","The 98 published posts and unrelated theme features stay untouched."],
        ["04","One task at a time","Finish, test, and then move to the next task."],
        ["05","Own the work","Explain changes clearly; do not hide complexity or invent success."]
      ];
      var list=el("div","trtt-cr-rules");
      rules.forEach(function(r){var row=el("article","trtt-cr-rule");row.appendChild(el("b","",r[0]));var copy=el("div","");copy.appendChild(el("strong","",r[1]));copy.appendChild(el("p","",r[2]));row.appendChild(copy);list.appendChild(row);});
      pane.appendChild(list);
    } else if(id==="truth") {
      pane.appendChild(sectionIntro("06 / EVIDENCE FIRST","Truth Desk","A claim is not a fact just because it sounds convincing."));
      var steps=el("div","trtt-cr-checklist");
      ["Find the original source, not only a repost.","Check the publication date and the event date.","Compare with a second independent, credible source.","Separate confirmed facts from claims and opinion.","If evidence is missing, say so or do not publish."].forEach(function(t,i){var row=el("div","trtt-cr-check");var n=el("span","",String(i+1).padStart(2,"0"));row.appendChild(n);row.appendChild(el("p","",t));steps.appendChild(row);});
      pane.appendChild(steps);
      pane.appendChild(el("div","trtt-cr-note","TRTT STANDARD: Verify first. Publish second. Correct transparently."));
    } else if(id==="mission") {
      pane.appendChild(sectionIntro("07 / FOCUS & DELIVERY","Mission Control","A simple operating board. One active task, one clear next step."));
      var feature=el("div","trtt-cr-feature");
      feature.appendChild(el("span","trtt-cr-kicker","CURRENT MISSION"));
      feature.appendChild(el("h4","","Restore the complete V106 Thinking Room"));
      feature.appendChild(el("p","","Keep one entrance on the blog and place all eight rooms behind it. Protect the rest of production."));
      pane.appendChild(feature);
      var stages=el("div","trtt-cr-grid");
      card(stages,"01","Understand","Read the existing files and confirm the actual loading path.");
      card(stages,"02","Build","Change only the approved Thinking Room assets.");
      card(stages,"03","Review","Check the diff, accessibility, responsive layout, and asset version.");
      card(stages,"04","Release","Publisher reviews and merges. Then verify the live blog.");
      pane.appendChild(stages);
    } else if(id==="private") {
      pane.appendChild(sectionIntro("08 / YOUR QUIET SPACE","Private Corner","A quieter place for personal writing, memories, and the journey behind the project."));
      var grid=el("div","trtt-cr-grid");
      card(grid,"⌂","My Diary","Open the My Diary posts on TRTT Voyage.");
      grid.lastChild.appendChild(link("Open My Diary","/search/label/My%20Diary"));
      card(grid,"♡","For Roksana","A personal corner for the people and reasons behind the journey.");
      card(grid,"⌖","Sanluri to World","A life journey told with honesty, dignity, and hope.");
      pane.appendChild(grid);
      pane.appendChild(el("p","trtt-cr-disclosure","Private notes are not collected or sent anywhere by this room."));
    }
    return pane;
  }

  function build() {
    if(!document.body || document.getElementById("trtt-thinking-room-trigger")) return;
    var door=el("button","trtt-cr-door");
    door.id="trtt-thinking-room-trigger"; door.type="button";
    door.setAttribute("aria-label","Enter the TRTT Thinking Room");
    door.setAttribute("aria-controls","trtt-room-overlay"); door.setAttribute("aria-expanded","false");
    door.appendChild(el("span","trtt-cr-door-mark","✦"));
    var label=el("span","trtt-cr-door-label");
    label.appendChild(el("strong","","THINKING ROOM")); label.appendChild(el("small","","ENTER THE ROOM"));
    door.appendChild(label); door.appendChild(el("span","trtt-cr-door-arrow","↗"));

    var overlay=el("div","trtt-cr-overlay"); overlay.id="trtt-room-overlay";
    overlay.setAttribute("role","dialog"); overlay.setAttribute("aria-modal","true");
    overlay.setAttribute("aria-hidden","true"); overlay.setAttribute("aria-labelledby","trtt-cr-title");
    var shell=el("div","trtt-cr-shell");
    var header=el("header","trtt-cr-header");
    var heading=el("div","trtt-cr-heading");
    heading.appendChild(el("span","trtt-cr-kicker","TRTT VOYAGE • SANLURI TO WORLD"));
    var h2=el("h2","","THINKING ROOM"); h2.id="trtt-cr-title"; heading.appendChild(h2);
    heading.appendChild(el("p","","An open public space for ideas, travel, truth, and building."));
    var close=el("button","trtt-cr-close","×"); close.type="button"; close.setAttribute("aria-label","Close Thinking Room");
    header.appendChild(heading); header.appendChild(close); shell.appendChild(header);
    shell.appendChild(el("div","trtt-cr-public","PUBLIC VIEW • ALL 8 ROOMS OPEN • NO PIN / PASSWORD"));
    var layout=el("div","trtt-cr-layout");
    var nav=el("nav","trtt-cr-nav"); nav.setAttribute("aria-label","Thinking Room sections");
    var content=el("div","trtt-cr-content");
    ROOMS.forEach(function(room,index){
      var b=el("button","trtt-cr-nav-item"); b.type="button"; b.dataset.room=room.id;
      b.setAttribute("aria-controls","trtt-cr-pane-"+room.id);
      b.appendChild(el("span","trtt-cr-nav-icon",room.icon));
      var copy=el("span","trtt-cr-nav-copy"); copy.appendChild(el("strong","",room.name)); copy.appendChild(el("small","",room.sub));
      b.appendChild(copy); nav.appendChild(b);
      var pane=buildRoomContent(room.id); pane.id="trtt-cr-pane-"+room.id;
      pane.setAttribute("aria-label",room.name); content.appendChild(pane);
    });
    layout.appendChild(nav); layout.appendChild(content); shell.appendChild(layout);
    shell.appendChild(el("footer","trtt-cr-footer","TRTT MAC-787950 • Made by MAC — Muse, Abu, ChatGPT"));
    overlay.appendChild(shell);

    function activate(id,focusNav){
      Array.prototype.forEach.call(nav.children,function(b){
        var active=b.dataset.room===id;
        b.classList.toggle("is-active",active);
        b.setAttribute("aria-current",active?"page":"false");
        if(active && focusNav) b.focus();
      });
      Array.prototype.forEach.call(content.children,function(p){p.classList.toggle("is-active",p.dataset.room===id);});
    }
    function open(){
      overlay.classList.add("is-open"); overlay.setAttribute("aria-hidden","false");
      document.documentElement.classList.add("trtt-cr-open");
      door.setAttribute("aria-expanded","true"); activate("brain",false); close.focus();
    }
    function shut(){
      overlay.classList.remove("is-open"); overlay.setAttribute("aria-hidden","true");
      document.documentElement.classList.remove("trtt-cr-open");
      door.setAttribute("aria-expanded","false"); door.focus();
    }
    nav.addEventListener("click",function(e){
      var b=e.target.closest("button[data-room]"); if(b) activate(b.dataset.room,false);
    });
    close.addEventListener("click",shut); door.addEventListener("click",open);
    overlay.addEventListener("click",function(e){if(e.target===overlay) shut();});
    document.addEventListener("keydown",function(e){
      if(!overlay.classList.contains("is-open")) return;
      if(e.key==="Escape"){e.preventDefault();shut();return;}
      if(e.key==="Tab"){
        var focusable=overlay.querySelectorAll('button:not([disabled]),a[href],input:not([disabled]),[tabindex]:not([tabindex="-1"])');
        if(!focusable.length)return;
        var first=focusable[0],last=focusable[focusable.length-1];
        if(e.shiftKey && document.activeElement===first){e.preventDefault();last.focus();}
        else if(!e.shiftKey && document.activeElement===last){e.preventDefault();first.focus();}
      }
    });
    document.body.appendChild(overlay); document.body.appendChild(door);
    activate("brain",false);
  }
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",build,{once:true});
  else build();
})();