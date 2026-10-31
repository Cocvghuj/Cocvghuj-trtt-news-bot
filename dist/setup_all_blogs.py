import os
from googleapiclient.discovery import build

# GitHub Secrets থেকে API Key এবং Blog IDs সংগ্রহ
API_KEY = os.environ.get("BLOGGER_API_KEY")

BLOGS = [
    {
        "name": "FlightScoutPro",
        "id": os.environ.get("FLIGHTSCOUTPRO_BLOG_ID") or os.environ.get("NEW_BLOG_ID"),
        "url": "https://flightscoutpro.blogspot.com"
    },
    {
        "name": "TRTT NEWS 24 BD",
        "id": os.environ.get("TRTT_BLOG_ID"), # যদি সিক্রেটে থাকে, না থাকলে ম্যানুয়ালি পেস্ট করবে
        "url": "https://trttnews24bd.blogspot.com"
    }
]

def init_blogger_service():
    """Blogger API v3 সার্ভিস তৈরি করে"""
    return build('blogger', 'v3', developerKey=API_KEY)

def create_network_pages(service, blog):
    """ব্লগ অনুযায়ী পারফেক্ট ইনফরমেশন ও গুগল স্ট্যান্ডার্ড পেজ তৈরি করে"""
    blog_id = blog["id"]
    blog_name = blog["name"]
    blog_url = blog["url"]

    if not blog_id:
        print(f"⚠️ Skipped {blog_name}: Blog ID is missing.")
        return

    print(f"🚀 Starting Setup for: {blog_name} (ID: {blog_id})")

    pages = [
        {
            "title": "About Us",
            "content": f"""
            <h2>Welcome to {blog_name}</h2>
            <p><strong>{blog_name}</strong> is an officially managed site within the <strong>TRTT NEWS 24 BD Network</strong>.</p>
            <p>Our goal is to provide accurate, verified, and updated technical and travel news insights directly to our audience.</p>
            <h3>Our Core Values</h3>
            <ul>
                <li><strong>Transparency:</strong> Authentic and checked information.</li>
                <li><strong>Security:</strong> Protected and monitored via standard API integrations.</li>
            </ul>
            <p>Main Portal: <a href="https://trttnews24bd.blogspot.com" target="_blank">TRTT NEWS 24 BD Hub</a></p>
            """
        },
        {
            "title": "Privacy Policy",
            "content": f"""
            <h2>Privacy Policy for {blog_name}</h2>
            <p>At <strong>{blog_name}</strong>, accessible from <em>{blog_url}</em>, privacy is one of our top priorities.</p>
            <h3>Information Collection & Log Files</h3>
            <p>Like most websites, we collect standard log files and use cookies to improve user experience and deliver optimized content according to Google AdSense and search guidelines.</p>
            <h3>Consent</h3>
            <p>By using our website, you hereby consent to our Privacy Policy and agree to its terms.</p>
            """
        },
        {
            "title": "Terms and Conditions",
            "content": f"""
            <h2>Terms and Conditions</h2>
            <p>Welcome to <strong>{blog_name}</strong>!</p>
            <p>By accessing <em>{blog_url}</em>, you agree to comply with our terms of service, intellectual property guidelines, and general network usage policies enforced by TRTT NEWS 24 BD Network.</p>
            """
        },
        {
            "title": "Contact Us",
            "content": f"""
            <h2>Contact Us</h2>
            <p>If you have any questions or business inquiries regarding {blog_name}, feel free to get in touch with us.</p>
            <ul>
                <li><strong>Website:</strong> <a href="{blog_url}">{blog_name}</a></li>
                <li><strong>Network Hub:</strong> <a href="https://trttnews24bd.blogspot.com" target="_blank">TRTT NEWS 24 BD</a></li>
            </ul>
            """
        }
    ]

    for page in pages:
        try:
            body = {
                "kind": "blogger#page",
                "title": page["title"],
                "content": page["content"]
            }
            request = service.pages().insert(blogId=blog_id, body=body)
            response = request.execute()
            print(f"  ✅ Created Page: '{page['title']}' for {blog_name} (Page ID: {response.get('id')})")
        except Exception as e:
            print(f"  ❌ Error creating '{page['title']}' for {blog_name}: {e}")

if __name__ == "__main__":
    if not API_KEY:
        print("❌ Error: BLOGGER_API_KEY is missing in GitHub Secrets!")
    else:
        blogger = init_blogger_service()
        for blog in BLOGS:
            create_network_pages(blogger, blog)
