# TRTT Blogger → Telegram automatic publishing bridge

**Record ID:** TRTT-TELEGRAM-AUTOPOST-001  
**Channel:** https://t.me/trttnews24bd  
**Schedule:** Every 15 minutes via GitHub Actions  
**Mode:** Published posts only; Blogger drafts are never forwarded.

## What it does
- Polls the public RSS feeds for TRTT Voyage and TRTT News 24 BD.
- Forwards new published posts with title, short excerpt, article link, and an available article image.
- Processes unseen posts oldest-first and stores delivery IDs in GitHub Actions cache.
- Confirms Telegram API success before marking each post delivered.
- Uses free GitHub Actions and Telegram Bot API; no paid service.

## Required GitHub Actions Secrets
- \`TELEGRAM_BOT_TOKEN\`: Telegram BotFather token. Never disclose its value.
- \`TELEGRAM_CHAT_ID\`: Channel username (e.g. \`@trttnews24bd\`) or numeric channel ID.

The bot must be an administrator of the channel with permission to post. Actual permission is not verified by this code.

## First-run safety
The first successful run creates a baseline from current feed entries and does not send the existing archive. Posts published after the baseline are forwarded automatically. Historical backfill is separate and must be explicitly approved.

## Feeds
- \`https://trttvoyage.blogspot.com/feeds/posts/default?alt=rss&max-results=100\`
- \`https://trttnews24bd.blogspot.com/feeds/posts/default?alt=rss&max-results=100\`

FlightScoutPro is excluded.

## Limitations
- Normal delay is up to 15 minutes plus GitHub Actions queue time.
- RSS exposes only the latest 100 entries per blog.
- Cache expiry/clear can reset deduplication state; the next first run re-baselines without flooding the archive.
- Delivery is NOT TESTED until merged, Secrets are configured, bot channel permissions are granted, and the workflow is run.

## Owner setup after merge
1. In repository Settings → Secrets and variables → Actions, ensure \`TELEGRAM_BOT_TOKEN\` and \`TELEGRAM_CHAT_ID\` exist. Do not paste values into chat or code.
2. Add the bot to \`@trttnews24bd\` as an administrator with post permission.
3. Actions → **TRTT Blogger to Telegram Auto-Forward** → Run workflow.
4. First run should report “Baseline created”; no archive posts should be sent.
5. Publish one test Blogger post and confirm it appears once in Telegram.

## Security
No Telegram credential values are stored in this repository. This workflow never publishes Blogger drafts or modifies Blogger.
