import requests
import feedparser
import os

BLOGS = [
    "trttnews24bd.blogspot.com",
    "flightscoutpro.blogspot.com"
]

# Add from environment variables if present
if os.environ.get("BLOGGER_BLOG_ID"):
    BLOGS.append(os.environ.get("BLOGGER_BLOG_ID"))
if os.environ.get("FLIGHTSCOUTPRO_BLOG_ID"):
    BLOGS.append(os.environ.get("FLIGHTSCOUTPRO_BLOG_ID"))

# Deduplicate
BLOGS = list(set(BLOGS))

for blog in BLOGS:
    # Handle domain or ID
    if "." not in blog:
        # Assuming ID needs to be mapped to a URL if it is just an ID
        # Since we don\'t have a mapper, we skip if it is just an ID for now, 
        # or treat it as a subdomain of blogspot
        continue
    
    base_url = f"https://{blog}"
    rss_url = f"{base_url}/feeds/posts/default?alt=rss"
    sitemap_url = f"{base_url}/sitemap.xml"
    
    print(f"--- Processing {base_url} ---")
    
    # Sitemap Ping
    try:
        r = requests.get(f"https://www.google.com/ping?sitemap={sitemap_url}", timeout=10)
        print(f"Sitemap Ping: {r.status_code}")
    except Exception as e:
        print(f"Sitemap Ping failed: {e}")
        
    # Index Links
    feed = feedparser.parse(rss_url)
    links = [entry.link for entry in feed.entries[:3]]
    for link in links:
        try:
            r = requests.post("https://pubsubhubbub.appspot.com/publish", 
                              data={"hub.url": link, "hub.mode": "publish"}, timeout=10)
            print(f"Indexed {link}: {r.status_code}")
        except Exception as e:
            print(f"Failed to index {link}: {e}")
