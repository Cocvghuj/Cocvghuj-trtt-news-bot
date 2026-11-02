# Install the TRTT Blogger menu

The menu script is hosted with the TRTT Vercel static site and is built from `trtt-blog-menu.js`.

## One-time Blogger change

1. Open Blogger Dashboard for **TRTT News 24 BD**.
2. Go to **Theme**.
3. Before editing, use **Backup** to download the current theme XML.
4. Open **Edit HTML**.
5. Find the closing `</body>` tag.
6. Immediately before `</body>`, add this single line:

```html
<script src="https://cocvghuj-trtt-news-bot.vercel.app/trtt-blog-menu.js"></script>
```

7. Save the theme, then open the blog in a private/incognito tab and check desktop and mobile widths.

Do not replace the whole theme XML. This is a one-line loader addition only.

## What the script does

- Inserts the TRTT VOYAGE menu as the first element inside the page body, above the existing theme header.
- Uses the latest requested links and the #ff2e63 / #ff5a8a colors.
- Provides a keyboard-accessible mobile menu button with `aria-expanded`, Escape-to-close, and outside-click close.
- Avoids inserting a duplicate menu if the script is evaluated more than once.

## Updating the menu later

Edit `trtt-blog-menu.js` in the GitHub repository and push to `main`. Vercel's Git integration should publish the updated static asset after a successful production deployment. Verify the deployment is READY before expecting the live Blogger page to use the new version.

## Important limitations

- Blogger's public API does not expose Theme XML or Layout/Gadget editing. This loader is the supported bridge for the menu asset; it does not grant GitHub control over every Blogger dashboard setting.
- Blogger settings such as privacy, search preferences, comments, and custom redirects are not all exposed by the API. They must be handled through Blogger's dashboard where no supported API exists.
- Keep a copy of the original theme backup so the one-line change can be reversed if needed.
