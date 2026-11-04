import type { Metadata, Viewport } from "next";
import "./globals.css";
export const metadata:Metadata={
 metadataBase:new URL(process.env.NEXT_PUBLIC_SITE_URL||"https://trtt-voyage.vercel.app"),
 title:{default:"TRTT Voyage — Open Travel & Tech Intelligence",template:"%s | TRTT Voyage"},
 description:"Independent travel tools and a source-first technology update desk. Read official updates from OpenAI, Google, GitHub and Meta.",
 applicationName:"TRTT Voyage",
 verification:{google:"zDp4ABgRW_Bh7vhZ49sBzHpMu9WNZdHA3rXvHHd7VIA"},
 openGraph:{type:"website",title:"TRTT Voyage — Open Travel & Tech Intelligence",description:"Travel with clarity. Stay curious with official technology updates."},
 robots:{index:true,follow:true}
};
export const viewport:Viewport={width:"device-width",initialScale:1,themeColor:"#241b2f"};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>;}
