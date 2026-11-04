import Link from "next/link";
import {getLatestUpdates} from "@/lib/feeds";
import PartnerMarketplace from "@/app/components/partner-marketplace";
export const dynamic="force-dynamic";
function dateLabel(value:string){return new Intl.DateTimeFormat("en",{dateStyle:"medium",timeZone:"UTC"}).format(new Date(value));}
export default async function HomePage(){
 const data=await getLatestUpdates();const counts=new Set(data.items.map(item=>item.sourceId)).size;
 return <main>
 <header className="topbar">
  <Link className="brand" href="/" aria-label="TRTT Voyage home"><span className="brand-symbol">T</span><span><strong>TRTT <b>VOYAGE</b></strong><small>OPEN TRAVEL INTELLIGENCE</small></span></Link>
  <nav aria-label="Main navigation"><a href="#marketplace">Marketplace</a><a href="/flight-scout-pro">Flight Scout Pro</a><a href="#tech-desk">Tech desk</a><a href="https://trttnews24bd.blogspot.com/" target="_blank" rel="noreferrer">Roksana Vault ↗</a></nav>
  <a className="top-cta" href="#tech-desk">Explore updates <span>↗</span></a>
 </header>
 <section className="hero"><div className="hero-copy">
  <p className="eyebrow"><span className="pulse"/> INDEPENDENT · SOURCE-FIRST · PEOPLE FIRST</p>
  <h1>Travel with clarity.<br/><em>Stay curious.</em></h1>
  <p className="hero-lede">A thoughtful home for practical travel tools and technology updates—linked to the people who publish them, never copied from their articles.</p>
  <div className="hero-actions"><a className="button button-pink" href="#tech-desk">Explore the tech desk <span>→</span></a><a className="button button-outline" href="#travel-tools">Discover travel tools</a></div>
  <div className="hero-proof"><span>✳</span> Official sources. Clear dates. Original editorial notes.</div>
 </div><div className="hero-art" aria-hidden="true"><div className="planet"><span>✦</span></div><div className="ring ring-one"/><div className="ring ring-two"/><div className="orbit-card card-top"><small>OPEN KNOWLEDGE</small><b>Curiosity, connected.</b></div><div className="orbit-card card-bottom"><small>TRTT TOOLKIT</small><b>Made for real journeys.</b></div><span className="star star-a">✳</span><span className="star star-b">✦</span></div></section>
 <section className="statbar" aria-label="Technology desk status"><div><strong>{data.items.length}</strong><span>recent updates</span></div><div><strong>{counts}</strong><span>official sources responding</span></div><div><strong>15 min</strong><span>feed cache window</span></div><p>Last checked {new Intl.DateTimeFormat("en",{hour:"2-digit",minute:"2-digit",timeZone:"UTC",timeZoneName:"short"}).format(new Date(data.checkedAt))}</p></section>
 <PartnerMarketplace />
 <section className="section tech-section" id="tech-desk"><div className="section-heading"><div><p className="eyebrow dark">THE OPEN INTELLIGENCE DESK</p><h2>Big ideas, from<br/><em>the original sources.</em></h2></div><p>Follow announcements from the teams building tomorrow. Each card links directly to its publisher. Preview text is written from the headline only—not copied from article bodies.</p></div>
 <div className="source-chips" aria-label="Tracked publishers">{data.sources.map(source=><span key={source.id} className={source.group.toLowerCase()}>{source.name}</span>)}</div>
 {data.items.length?<div className="news-grid">{data.items.map(item=><article className="news-card" key={item.id}><div className="news-meta"><span className={"source-dot "+item.group.toLowerCase()}/>{item.source}<time dateTime={item.publishedAt}>{dateLabel(item.publishedAt)}</time></div><h3>{item.title}</h3><p>{item.summary}</p><a href={item.url} target="_blank" rel="noopener noreferrer" className="read-link">Read the original <span>↗</span></a></article>)}</div>:<div className="empty-state"><strong>Official feeds are taking a short break.</strong><p>No feed entries could be loaded right now. Please try again later or visit the publishers directly.</p><a href="https://openai.com/news/" target="_blank" rel="noreferrer">OpenAI</a> · <a href="https://blog.google/technology/ai/" target="_blank" rel="noreferrer">Google AI</a> · <a href="https://github.blog/" target="_blank" rel="noreferrer">GitHub</a> · <a href="https://about.fb.com/news/" target="_blank" rel="noreferrer">Meta</a></div>}
 <p className="desk-note">Editorial note: previews are generated from feed headlines and source metadata only. Publisher headlines remain attributed to their owners. No article body, image, or full description is republished.</p></section>
 <section className="tools-section" id="travel-tools"><div className="tools-inner"><div className="section-heading"><div><p className="eyebrow dark">THE TRAVEL TOOLKIT</p><h2>Make every journey<br/><em>a little easier.</em></h2></div><p>Useful starting points for planning, packing and understanding your options.</p></div>
 <div className="tool-grid">
 <a className="tool-card" href="/flight-scout-pro"><span className="tool-icon pink">✈</span><small>FLIGHT INTELLIGENCE</small><h3>Flight Scout Pro</h3><p>Explore flight search, passenger rights and travel connections.</p><b>Open Flight Scout Pro ↗</b></a>
 <a className="tool-card" href="https://cocvghuj-trtt-news-bot.vercel.app/tools/baggage-size-checker.html"><span className="tool-icon gold">▣</span><small>PACK SMARTER</small><h3>Baggage checker</h3><p>Review cabin-bag dimensions before you travel.</p><b>Check baggage ↗</b></a>
 <a className="tool-card" href="https://cocvghuj-trtt-news-bot.vercel.app/tools/delay-calculator.html"><span className="tool-icon violet">◷</span><small>KNOW YOUR RIGHTS</small><h3>Delay guide</h3><p>Explore possible passenger-rights scenarios.</p><b>Check a delay ↗</b></a>
 </div></div></section>
 <section className="closing"><p className="eyebrow">OPEN KNOWLEDGE. OPEN DOORS.</p><h2>Better journeys begin<br/><em>with a simple question.</em></h2><a className="button button-light" href="https://trttnews24bd.blogspot.com/" target="_blank" rel="noreferrer">Visit TRTT Journal ↗</a></section>
 <footer className="footer"><Link className="footer-brand" href="/">TRTT <b>VOYAGE</b></Link><p>Independent travel tools and source-first technology updates.</p><div><a href="https://github.com/Cocvghuj/Cocvghuj-trtt-news-bot" target="_blank" rel="noreferrer">GitHub</a><a href="https://trttnews24bd.blogspot.com/" target="_blank" rel="noreferrer">Blogger</a><a href="https://openai.com/news/" target="_blank" rel="noreferrer">OpenAI</a></div><small>© {new Date().getFullYear()} TRTT Voyage. Publisher names and headlines belong to their respective owners.</small></footer>
 </main>;
}