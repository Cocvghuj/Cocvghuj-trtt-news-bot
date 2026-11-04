"use client";

import {useMemo, useState} from "react";

type Partner={id:string;name:string;category:string;description:string;url:string;icon:string;tag:string};
const partners:Partner[]=[
{id:"aviasales",name:"Aviasales",category:"Flights",description:"Compare flight options and routes with a flight metasearch partner.",url:"https://aviasales.tpo.lv/Fb8U9yav?marker=787950",icon:"✈️",tag:"Flight search"},
{id:"klook",name:"Klook",category:"Tours & tickets",description:"Explore tours, local activities, attractions and transit experiences.",url:"https://klook.tpo.lv/TWKnemhz?marker=787950",icon:"🎟️",tag:"Things to do"},
{id:"airalo",name:"Airalo",category:"eSIM & connectivity",description:"Browse international eSIM plans for connected travel.",url:"https://airalo.tpo.lv/ZZoQC7Mz?marker=787950",icon:"📶",tag:"eSIM"},
{id:"gettransfer",name:"GetTransfer",category:"Airport transfers",description:"Find private rides and transfer options for your journey.",url:"https://gettransfer.tpo.lv/1u8zRU5s?marker=787950",icon:"🚘",tag:"Transfers"},
{id:"drimsim",name:"Drimsim",category:"eSIM & connectivity",description:"Explore SIM connectivity options for international trips.",url:"https://drimsim.tpo.lv/Ly7ywlY8?marker=787950",icon:"🌐",tag:"SIM"},
{id:"getrentacar",name:"Getrentacar",category:"Car rental",description:"Compare car-rental options for independent travel.",url:"https://getrentacar.tpo.lv/VZe2HcGc?marker=787950",icon:"🚗",tag:"Car hire"},
{id:"airhelp",name:"AirHelp",category:"Passenger rights",description:"Check whether a disrupted flight may qualify for compensation support.",url:"https://airhelp.tpo.lv/3ItXS0E4?marker=787950",icon:"🛡️",tag:"Flight disruption"},
{id:"gocity",name:"Go City",category:"Tours & tickets",description:"Discover city passes and multi-attraction sightseeing options.",url:"https://gocity.tpo.lv/QSQw8FwU?marker=787950",icon:"🏙️",tag:"City passes"},
{id:"economybookings",name:"EconomyBookings",category:"Car rental",description:"Compare rental-car offers for destinations around the world.",url:"https://economybookings.tpo.lv/pyHqRiOo?marker=787950",icon:"🚙",tag:"Car hire"},
{id:"qeeq",name:"QEEQ",category:"Car rental",description:"Explore car-rental choices and booking options.",url:"https://qeeq.tpo.lv/HKhCeDhY?marker=787950",icon:"🛣️",tag:"Car hire"},
{id:"tiqets",name:"Tiqets",category:"Tours & tickets",description:"Find tickets for museums, attractions and cultural experiences.",url:"https://tiqets.tpo.lv/bnx8pnF6?marker=787950",icon:"🎫",tag:"Attraction tickets"},
{id:"trip-pickups",name:"Airport & hotel pickups",category:"Airport transfers",description:"Open the partner service for airport and hotel pickup options.",url:"https://tpo.lv/h3LrTZcS?marker=787950",icon:"🧭",tag:"Pickups"},
{id:"localrent",name:"Localrent",category:"Car rental",description:"Explore local car-hire providers and rental options.",url:"https://localrent.tpo.lv/4jd1lRQG?marker=787950",icon:"🚘",tag:"Local car hire"},
{id:"kiwitaxi",name:"Kiwitaxi",category:"Airport transfers",description:"Arrange airport transfers and pre-booked rides.",url:"https://kiwitaxi.tpo.lv/tlZcbMOB?marker=787950",icon:"🚖",tag:"Airport rides"},
{id:"yesim",name:"Yesim",category:"eSIM & connectivity",description:"Browse travel eSIM options for mobile data abroad.",url:"https://yesim.tpo.lv/krzFKLpg?marker=787950",icon:"📱",tag:"eSIM"},
{id:"compensair",name:"Compensair",category:"Passenger rights",description:"Explore flight compensation claim support and eligibility information.",url:"https://compensair.tpo.lv/YgVXgRnB?marker=787950",icon:"⚖️",tag:"Passenger rights"},
{id:"saily",name:"Saily",category:"eSIM & connectivity",description:"Compare digital SIM plans for travel connectivity.",url:"https://saily.tpo.lv/ssekmS4X?marker=787950",icon:"📡",tag:"eSIM"},
{id:"kkday",name:"KKday",category:"Tours & tickets",description:"Discover local tours, experiences and activity bookings.",url:"https://kkday.tpo.lv/JaAfTgGF?marker=787950",icon:"🌄",tag:"Experiences"},
{id:"intui",name:"Intui",category:"Airport transfers",description:"Find airport transfer services for holiday destinations.",url:"https://intui.tpo.lv/tiSkz4Yq?marker=787950",icon:"🚐",tag:"Transfers"},
{id:"radical-storage",name:"Radical Storage",category:"Luggage storage",description:"Find luggage-storage locations while exploring a city.",url:"https://radicalstorage.tpo.lv/WkGqxIsD?marker=787950",icon:"🧳",tag:"Bag storage"},
{id:"amazon",name:"Amazon Travel Essentials",category:"Travel essentials",description:"Browse the travel gear and accessories selected for the TRTT travel shop.",url:"https://amzn.to/4shg6Hn",icon:"🛍️",tag:"Amazon shop"}
];
const categories=["All services","Flights","Tours & tickets","eSIM & connectivity","Airport transfers","Car rental","Passenger rights","Luggage storage","Travel essentials"];

export default function PartnerMarketplace({initialCategory="All services"}:{initialCategory?:string}){
 const [category,setCategory]=useState(initialCategory);
 const [query,setQuery]=useState("");
 const [mapQuery,setMapQuery]=useState("Rome, Italy");
 const [mapOpen,setMapOpen]=useState(false);
 const visible=useMemo(()=>partners.filter(p=>(category==="All services"||p.category===category)&&(`${p.name} ${p.category} ${p.description}`.toLowerCase().includes(query.toLowerCase()))),[category,query]);
 return <section className="marketplace-section" id="marketplace">
  <div className="marketplace-head">
   <div><p className="market-eyebrow">TRTT VOYAGE PARTNER MARKETPLACE</p><h2>Plan the whole journey.<br/><em>From one travel hub.</em></h2></div>
   <p className="marketplace-intro">Explore partner services by travel need. Compare the provider's current options, terms and prices before booking.</p>
  </div>
  <div className="market-tools">
   <label className="market-search"><span aria-hidden="true">⌕</span><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search flights, eSIM, transfers, tickets…" aria-label="Search travel services"/></label>
   <a className="market-map-link" href="https://www.google.com/maps/search/?api=1&query=world+travel" target="_blank" rel="noopener noreferrer">Open Google Maps ↗</a>
  </div>
  <section className="market-map-explorer" aria-label="Destination map explorer">
   <div className="market-map-copy"><span>DESTINATION EXPLORER</span><h3>See where your journey takes you.</h3><p>Search a city, airport or landmark to preview it on the map.</p></div>
   <form className="market-map-form" onSubmit={e=>{e.preventDefault();if(mapQuery.trim())setMapOpen(true);}}>
    <input value={mapQuery} onChange={e=>setMapQuery(e.target.value)} aria-label="Destination or landmark" placeholder="e.g. Cagliari, Italy"/>
    <button type="submit">Show map ↗</button>
   </form>
   {mapOpen&&<div className="market-map-frame"><iframe title={"Map of "+mapQuery} src={"https://www.google.com/maps?q="+encodeURIComponent(mapQuery)+"&output=embed"} loading="lazy" referrerPolicy="no-referrer-when-downgrade" allowFullScreen/></div>}
  </section>
  <div className="market-filters" role="group" aria-label="Filter travel services">
   {categories.map(c=><button type="button" key={c} onClick={()=>setCategory(c)} className={category===c?"active":""} aria-pressed={category===c}>{c}</button>)}
  </div>
  <div className="market-results"><span>{visible.length} services</span><span>Partner links open in a new tab</span></div>
  <div className="partner-grid">
   {visible.map(p=><article className="partner-card" key={p.id}>
    <div className="partner-card-top"><span className="partner-icon" aria-hidden="true">{p.icon}</span><span className="partner-tag">{p.tag}</span></div>
    <h3>{p.name}</h3><p>{p.description}</p>
    <a href={p.url} target="_blank" rel="sponsored nofollow noopener noreferrer" className="partner-cta">Explore options <span>↗</span></a>
   </article>)}
  </div>
  {visible.length===0&&<div className="market-empty">No matching service. Try another search or category.</div>}
  <p className="affiliate-note">Affiliate disclosure: TRTT Voyage may earn a commission when you use eligible partner links, at no additional cost to you. Providers control availability, prices, booking conditions and support. TRTT Voyage does not guarantee a particular fare or offer.</p>
 </section>;
}
