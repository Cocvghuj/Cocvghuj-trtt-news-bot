import Parser from "rss-parser";
export type NewsSource = { id:string; name:string; group:"AI"|"Developer"|"Company"; feedUrl:string; siteUrl:string };
export type NewsItem = { id:string; title:string; url:string; source:string; sourceId:string; group:NewsSource["group"]; publishedAt:string; summary:string };
export const SOURCES:NewsSource[]=[
{id:"openai",name:"OpenAI",group:"AI",feedUrl:"https://openai.com/news/rss.xml",siteUrl:"https://openai.com/news/"},
{id:"google-ai",name:"Google AI",group:"AI",feedUrl:"https://blog.google/technology/ai/rss/",siteUrl:"https://blog.google/technology/ai/"},
{id:"deepmind",name:"Google DeepMind",group:"AI",feedUrl:"https://deepmind.google/blog/rss.xml",siteUrl:"https://deepmind.google/"},
{id:"github",name:"GitHub",group:"Developer",feedUrl:"https://github.blog/feed/",siteUrl:"https://github.blog/"},
{id:"meta-news",name:"Meta Newsroom",group:"Company",feedUrl:"https://about.fb.com/news/feed/",siteUrl:"https://about.fb.com/news/"},
{id:"meta-engineering",name:"Meta Engineering",group:"Developer",feedUrl:"https://engineering.fb.com/feed/",siteUrl:"https://engineering.fb.com/"}
];
const parser=new Parser({timeout:8000,headers:{"User-Agent":"TRTT-Voyage-NewsReader/1.0"}});
function cleanTitle(value:unknown){return String(value??"").replace(/<[^>]*>/g," ").replace(/\s+/g," ").trim().slice(0,220);}
function makeSummary(title:string,source:string){return "A title-based preview of "+source+"'s official update: “"+title.replace(/[.!?]+$/,"")+"”. Open the original source for the full announcement and context.";}
function safeArticleUrl(value:unknown,source:NewsSource):string|null{
 try{const url=new URL(String(value??""));const allowed=new URL(source.siteUrl).hostname;
 if(url.protocol!=="https:"||(url.hostname!==allowed&&!url.hostname.endsWith("."+allowed)))return null;
 return url.toString();}catch{return null;}
}
export async function getLatestUpdates(){
 const settled=await Promise.allSettled(SOURCES.map(async source=>{
  const response=await fetch(source.feedUrl,{headers:{"User-Agent":"TRTT-Voyage-NewsReader/1.0",Accept:"application/rss+xml, application/atom+xml, application/xml, text/xml"},signal:AbortSignal.timeout(9000),next:{revalidate:900}});
  if(!response.ok)throw new Error(source.name+" feed returned HTTP "+response.status);
  const xml=await response.text();if(xml.length>2_000_000)throw new Error("Feed exceeded the 2 MB safety limit");
  const feed=await parser.parseString(xml);
  return (feed.items??[]).slice(0,12).flatMap(entry=>{
   const title=cleanTitle(entry.title);const url=safeArticleUrl(entry.link,source);const rawDate=entry.isoDate||entry.pubDate;const date=rawDate?new Date(rawDate):null;
   if(!title||!url||!date||Number.isNaN(date.getTime()))return [];
   return [{id:source.id+":"+String(entry.guid||url).slice(0,180),title,url,source:source.name,sourceId:source.id,group:source.group,publishedAt:date.toISOString(),summary:makeSummary(title,source.name)}];
  });
 }));
 const items=settled.flatMap(result=>result.status==="fulfilled"?result.value:[]);
 const unique=Array.from(new Map(items.map(item=>[item.url,item])).values()).sort((a,b)=>Date.parse(b.publishedAt)-Date.parse(a.publishedAt)).slice(0,36);
 return {items:unique,checkedAt:new Date().toISOString(),sources:SOURCES};
}