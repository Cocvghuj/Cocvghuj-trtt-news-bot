# TRTT Voyage — GitHub + JSDelivr Theme Bridge

This is a reversible external visual layer for Blogger. It is not a Blogger API controller and does not publish posts or replace the Blogger XML theme.

## Files
- `theme.css`: scoped visual overrides enabled only when the loader sets `data-trtt-theme="enabled"`.
- `loader.js`: sets that opt-in attribute; no Blogger data, credentials, or visitor data are collected.
- `blogger-loader.xml`: Blogger `<head>` snippet using JSDelivr URLs pinned to this feature branch.

## Safe installation
1. Back up the current Blogger theme XML.
2. Test only on a backup/test blog or copied theme first.
3. Insert the two tags from `blogger-loader.xml` inside `<head>`.
4. Preview desktop and mobile; remove both tags to roll back.
5. Do not use the `@main` CDN URL until this branch is reviewed and explicitly merged to main.

## Test branch CDN base
`https://cdn.jsdelivr.net/gh/Cocvghuj/Cocvghuj-trtt-news-bot@feature/trtt-voyage-jsdelivr-loader/public/trtt-theme-bridge/`

NOT TESTED: live JSDelivr cache delivery and Blogger theme installation. No live Blogger changes were made.
