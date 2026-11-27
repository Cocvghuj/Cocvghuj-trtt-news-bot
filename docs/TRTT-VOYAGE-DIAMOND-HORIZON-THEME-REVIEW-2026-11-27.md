# TRTT Voyage — Diamond Horizon Blogger Theme Review

**Candidate:** `TRTT-Voyage-Generation-2-ULTIMATE.xml`  
**Project:** DR-TRTT-OPS-001  
**Brand:** TRTT Voyage — From Vision to Global Brand! Explore Beyond. Discover Everything.  
**Status:** Candidate only; not installed on Blogger.

## Design direction

- Diamond Horizon identity using Pink `#E98BAF`, Piyaji `#B77991`, Kathali `#D6A542`, Royal Midnight `#11152D`, White `#FFFFFF`, and restrained Cyan `#67E8F9` / Diamond Gold `#FFD700` accents.
- Mobile-first editorial layout with a dark brand header, simple navigation, a TRTT Voyage hero, clean article cards, and a dark footer.
- Homepage navigation is limited to Home, News, Travel, AI, Tools, and About. News, Travel, AI, and Tools destinations were checked against live Blogger routes; the menu uses existing non-empty routes.
- Footer includes About, Privacy, Disclaimer, and known public TRTT channels. The Contact page route currently returns 404, so it is not linked until the Owner creates the live Blogger page.
- Existing Blog1, Header1, LinkList74, Label1, ContactForm1, and other source widgets are retained; Blog1 share buttons remain disabled. The legacy PageList1 and Profile1 widgets are hidden from public rendering to avoid an old Blogger home URL and personal location/profile panel.

## Safety changes

- Started from the current repository theme source and created a separate new candidate file. The old theme file remains untouched.
- Removed the obfuscated `eval()` theme function block and the malformed legacy auto-link mutation script.
- Removed the `deleted='true'` section attribute while keeping the hidden contact widget container hidden.
- Removed the old `trttnews24bd.blogspot.com` navigation destination. The legacy Blogger PageList/Profile widgets are hidden; personal diary cards are filtered from public feeds and old TRTT News24BD label chips are hidden. Diary content remains available on its own label route. The old Telegram channel handle remains only in the actual Telegram URL because the public channel handle has not been changed.
- Replaced the branch-specific raw JavaScript loader with the reviewed main-branch `trtt-loader.js` reference.
- Removed the generic Lorem Ipsum footer caption.
- No posts, Blogger settings, existing live theme, or production deployment were changed.

## Navigation destinations

- Home and category paths are relative to the active Blogger host, so the menu follows whichever Blogger host is actually configured.
- Tools points to the current Vercel project domain at `/super-app`. Vercel reports a READY production deployment, but the project-level live flag is false; public route resolution remains NOT VERIFIED.
- The brand/header link points to `https://trttvoyage.com/`. The custom domain was not found as a domain in the connected Vercel team, and Blogger custom-domain status is NOT VERIFIED.

## Validation

The PR adds `scripts/validate_blogger_theme.py` and a PR workflow step to check:
- XML well-formedness with Python's standard-library XML parser.
- Forbidden patterns: `eval(`, `location.href`, `deleted='true'`, and `auto-publish`.
- Required existing widget IDs and uniqueness.
- Six navigation labels and non-empty destinations.
- Blog1 share buttons disabled.
- Footer page links and approved palette tokens; verified category routes; personal diary isolation and legacy widget hiding.
- Reviewed control-loader reference.

## Not tested

- Blogger Theme preview/import and Layout editor behavior.
- Live Contact page route (currently 404), and the final live About/Privacy/Disclaimer content update.
- Mobile/desktop browser rendering and accessibility.
- Public resolution of `trttvoyage.com` and the Vercel Tools route.
- Live Blogger pages, existing post count, or production deployment.

**Owner approval is required before importing or replacing any live Blogger theme.**
