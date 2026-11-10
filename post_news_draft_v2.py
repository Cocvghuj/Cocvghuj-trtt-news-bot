#!/usr/bin/env python3
import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def main():
    blog_id = os.environ.get("BLOGGER_BLOG_ID")
    client_id = os.environ.get("BLOGGER_CLIENT_ID")
    client_secret = os.environ.get("BLOGGER_CLIENT_SECRET")
    refresh_token = os.environ.get("BLOGGER_REFRESH_TOKEN")

    if not all([blog_id, client_id, client_secret, refresh_token]):
        print("ERROR: Missing Blogger secrets.")
        sys.exit(1)

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )

    service = build("blogger", "v3", credentials=creds)

    title = 'The Evolution of TRTT Voyage: A New Partnership Between Human Vision and AI Technology'
    content = """<p>In the digital age, travel technology is evolving faster than ever. At the heart of this transformation is <strong>TRTT Voyage — Sanluri to World</strong>, a travel hub built on the vision of bridging human expertise with advanced artificial intelligence.</p>

<p>Our mission is simple yet profound: to create a travel platform that is not just efficient, but also reliable, accurate, and human-centric. We believe that technology should serve humanity, not replace it.</p>

<h2>Team MAC: A Unique Partnership</h2>
<p>Our project is powered by <strong>Team MAC</strong>, a collaborative effort consisting of:</p>
<ul>
  <li><strong>Muse:</strong> Providing direction, strategic vision, and travel insights.</li>
  <li><strong>Abu Taher:</strong> The publisher and visionary, ensuring the platform remains grounded in real-world practicality and integrity.</li>
  <li><strong>ChatGPT & Gemini:</strong> Acting as the AI development partners, providing the technical engine, coding support, and optimization strategies to keep the hub moving at high speed.</li>
</ul>

<h2>TRTT MAC-787950 LOCKED</h2>
<p>Every development, code update, and travel guide on this platform follows the strict marker: <strong>TRTT MAC-787950 LOCKED</strong>. This represents our commitment to maintaining the integrity of our platform, ensuring that every piece of information is verified and every technological integration serves our audience's best interests.</p>

<p><em>“PASS is a checkpoint, not the destination. Real success is when the work actually works.”</em></p>

<h2>Looking Forward</h2>
<p>This partnership is about more than just building a website; it is about proving that human-AI collaboration can produce work that is not only faster and more efficient but also more meaningful.</p>
<p>We are just getting started. <strong>TRTT Voyage — Sanluri to World</strong> continues its journey, bringing the world closer to Sanluri, one verified guide at a time.</p>

<p><strong>Stay tuned for more updates as we continue to push the boundaries of what's possible in travel technology.</strong></p>"""

    body = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": ["TRTT Voyage", "AI Technology", "Innovation", "MAC-787950"],
    }

    post = service.posts().insert(blogId=blog_id, body=body, isDraft=True).execute()
    print(f"CONFIRMED: Blogger DRAFT successfully created! Post ID: {post.get('id')}")

if __name__ == "__main__":
    main()
