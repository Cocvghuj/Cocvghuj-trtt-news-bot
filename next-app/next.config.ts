import type { NextConfig } from "next";
const nextConfig: NextConfig = {
  poweredByHeader: false,
  reactStrictMode: true,
  compress: true,
  async headers() { return [
    { source: "/:path*", headers: [
      { key: "X-Content-Type-Options", value: "nosniff" },
      { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
      { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" }
    ]},
    { source: "/api/:path*", headers: [{ key: "Cache-Control", value: "public, s-maxage=900, stale-while-revalidate=3600" }] }
  ]; }
};
export default nextConfig;