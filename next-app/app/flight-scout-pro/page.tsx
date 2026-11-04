import Link from "next/link";
import PartnerMarketplace from "@/app/components/partner-marketplace";

export const metadata={title:"Flight Scout Pro | TRTT Voyage",description:"Aviation planning, flight search, passenger rights and travel services from TRTT Voyage."};
export default function FlightScoutProPage(){return <main className="fsp-hub">
 <header className="fsp-top"><Link href="/" className="fsp-brand">✈ FLIGHTSCOUT<span>PRO</span></Link><nav><Link href="/">TRTT Voyage</Link><a href="/#tech-desk">Intelligence desk</a><a href="/#marketplace">Travel marketplace</a></nav></header>
 <section className="fsp-hero"><p>FLIGHT INTELLIGENCE · TRAVEL PLANNING · PASSENGER RIGHTS</p><h1>Every connection,<br/><em>planned with confidence.</em></h1><div>Flight search, airport transfers, connectivity and passenger-rights resources in one independent travel workspace.</div><a href="#fsp-services">Explore flight services ↓</a></section>
 <section className="fsp-feature-row"><article><b>01 / FLIGHT SEARCH</b><h2>Compare routes</h2><p>Open a flight-search partner to check current routes and fares.</p></article><article><b>02 / TRAVEL SUPPORT</b><h2>Stay connected</h2><p>Explore eSIM, transfers and car hire for the journey beyond the airport.</p></article><article><b>03 / PASSENGER RIGHTS</b><h2>Know your options</h2><p>Review disruption and compensation resources. Eligibility depends on the facts and applicable rules.</p></article></section>
 <div id="fsp-services"><PartnerMarketplace initialCategory="Flights"/></div>
 <footer className="fsp-footer"><Link href="/">TRTT VOYAGE</Link><span>Independent travel information. Partner services are provided by third parties.</span></footer>
 </main>}
