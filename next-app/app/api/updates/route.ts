import {NextResponse} from "next/server";
import {getLatestUpdates} from "@/lib/feeds";
export const revalidate=900;
export async function GET(){
 try{const data=await getLatestUpdates();return NextResponse.json(data,{headers:{"Cache-Control":"public, s-maxage=900, stale-while-revalidate=3600"}});}
 catch{return NextResponse.json({items:[],checkedAt:new Date().toISOString(),sources:[],error:"Official feeds are temporarily unavailable."},{status:503,headers:{"Cache-Control":"public, s-maxage=60, stale-while-revalidate=300"}});}
}