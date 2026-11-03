# TRTT Voyage — Next.js edition
This is a self-contained Next.js App Router implementation for a Vercel project whose **Root Directory is set to `next-app`**.

## Features
- Responsive, mobile-first TRTT Voyage landing page.
- Golapi `#ff2e63`, Kathali `#FFC300`, and Piaji `#AF7AC5` brand palette.
- Server-rendered official-source update desk for OpenAI, Google AI, Google DeepMind, GitHub, Meta Newsroom, and Meta Engineering.
- RSS fetched server-side and cached for 15 minutes; each feed has a 9-second timeout and 2 MB response limit.
- Only publisher headline, publication date, source name, and original article URL are displayed. No article body, image, or publisher description is republished.
- Preview copy is written from the headline only. It is not represented as an AI-verified article summary.
- Publisher links are restricted to HTTPS and each feed's expected official domain.
- No API keys or paid AI calls are required for this news desk.

## Local development
```bash
npm install
npm run dev
```

## Build and checks
```bash
npm run lint
npm run build
```

## Vercel setup
Create a separate Vercel project for this Next.js edition (or a dedicated preview project) and select this repository branch:
- Root Directory: `next-app`
- Framework Preset: Next.js
- Build Command: `npm run build`
- Install Command: `npm install`
- Output Directory: leave blank (Next.js default)

Optional: `NEXT_PUBLIC_SITE_URL` for canonical metadata.

**Migration boundary:** the repository root still contains the existing static TRTT hub, Blogger assets, and Roksana serverless endpoint. Do not change the existing Vercel project's Root Directory to `next-app` until all legacy routes and the Answer Engine have been migrated and tested. This edition is prepared for a separate Vercel preview/project and has not been deployed.

## Copyright and source policy
Feeds are used as discovery metadata, not as permission to reproduce article content. Publisher titles are attributed and linked to their original pages; dates come from feed metadata. Preview text is a short original note based only on headline and publisher identity. If a feed is unavailable, the page degrades gracefully and offers direct publisher links. Publisher names and marks remain their owners' property. This approach reduces copying and attribution risk; it is not a legal guarantee. Respect publisher terms, applicable copyright/database rights, robots rules, and feed-specific conditions.