import os
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ১. গিটহাব সিক্রেটস থেকে এনভায়রনমেন্ট ভেরিয়েবল ফেচ করা
MARKER = os.environ.get('TRAVEL_PAYOUT_MARKER', '787950')
AMAZON_URL = os.environ.get('AMAZON_LINK', 'https://amzn.to/4shg6Hn')
GITHUB_HUB = "https://Cocvghuj.github.io/Cocvghuj-trtt-news-bot/"

def generate_elite_guide():
    print("Generating Next-Gen Evergreen Travel Guide...")
    
    # আকর্ষনীয় চিরসবুজ শিরোনাম ও কনটেন্ট
    elite_guide_title = "The Ultimate 2026 Secret European Transit & Budget Travel Blueprint"
    
    elite_html_content = f"""
    <h2>The Ultimate 2026 Secret European Transit & Budget Travel Blueprint</h2>
    <p>Discover how modern travelers are bypassing traditional booking traps using autonomous routing, smart transit solutions, and verified digital tools across Europe.</p>
    
    <h3>1. Smart Flight & Transit Connections</h3>
    <p>To secure the best flight deals and avoid hidden markup fees, check out our trusted partner network:</p>
    <ul>
        <li>✈️ Direct Flight Deals: <a href="https://aviasales.tpo.lv/Fb8U9yav" target="_blank">Aviasales Hub (Marker {MARKER})</a></li>
        <li>🚆 Smart Euro Transit & Stays: <a href="https://tpo.lv/h3LrTZcS" target="_blank">Trip.com Gateway</a></li>
    </ul>
    
    <h3>2. Essential Travel Gear</h3>
    <p>Always pack light and carry necessary digital gear. Browse top-rated items at the official <a href="{AMAZON_URL}" target="_blank">Amazon Verified Travel Store</a>.</p>
    
    <hr>
    <div style="background: rgba(0, 242, 254, 0.08); padding: 25px; border-radius: 12px; margin-top: 20px; border-left: 4px solid #00f2fe;">
        <h3 style="margin-top: 0; color: #0066ff;">⚡ Experience the Next-Gen Travel Engine</h3>
        <p>Want to calculate live routes, check instant budgets, and bypass high booking commissions? Use our interactive platform:</p>
        <p><a href="{GITHUB_HUB}" target="_blank" style="background: #0066ff; color: #fff; padding: 12px 25px; border-radius: 25px; font-weight: bold; text-decoration: none; display: inline-block; margin-top: 10px;">Launch Live GitHub Hub Engine</a></p>
    </div>
    """
    return elite_guide_title, elite_html_content

def publish_to_blogger(title, content):
    blog_id = os.environ.get('BLOGGER_BLOG_ID')
    client_id = os.environ.get('BLOGGER_CLIENT_ID')
    client_secret = os.environ.get('BLOGGER_CLIENT_SECRET')
    refresh_token = os.environ.get('BLOGGER_REFRESH_TOKEN')

    if not all([blog_id, client_id, client_secret, refresh_token]):
        print("Error: Blogger API credentials missing in GitHub Secrets!")
        return

    # গুগল ক্রেমেনশিয়াল দিয়ে অথেন্টিকেশন তৈরি
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token"
    )

    try:
        service = build('blogger', 'v3', credentials=creds)
        
        post_body = {
            'title': title,
            'content': content
        }

        # ব্লগে পোস্ট পুশ করার রিকোয়েস্ট
        request = service.posts().insert(blogId=blog_id, body=post_body)
        response = request.execute()
        
        print(f"Successfully published to Blogger! Post ID: {response.get('id')}")
    except Exception as e:
        print(f"Failed to publish to Blogger: {str(e)}")

if __name__ == "__main__":
    title, content = generate_elite_guide()
    publish_to_blogger(title, content)
