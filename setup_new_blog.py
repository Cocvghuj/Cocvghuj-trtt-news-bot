import os
from googleapiclient.discovery import build

# GitHub Secrets থেকে Blog ID এবং API Key গ্রহণ
BLOG_ID = os.environ.get("FLIGHTSCOUTPRO_BLOG_ID") or os.environ.get("NEW_BLOG_ID")
API_KEY = os.environ.get("BLOGGER_API_KEY")

def init_blogger_service():
    """Blogger API v3 সার্ভিস তৈরি করে"""
    return build('blogger', 'v3', developerKey=API_KEY)

def create_info_pages(service):
    """গুগল ও অ্যাডসেন্স পলিসি অনুযায়ী প্রফেশনাল পেজসমূহ ব্যাকগ্রাউন্ডে তৈরি করে"""
    
    pages_to_create = [
        {
            "title": "About Us",
            "content": """
            <h2>Welcome to FlightScoutPro</h2>
            <p><strong>FlightScoutPro</strong> is a dedicated travel and aviation review platform designed to help travelers find cheap flights, explore worldwide destinations, and access civil engineer-reviewed travel insights.</p>

            <h3>Our Network & Mission</h3>
            <p>FlightScoutPro operates as an officially managed partner site within the <strong>TRTT NEWS 24 BD Network</strong> (EuroVoyage HUB Twin Network). Our primary goal is to provide accurate, transparent, and updated flight scouting information to make your journey affordable and hassle-free.</p>

            <h3>Why Choose Us?</h3>
            <ul>
                <li><strong>Verified Deals:</strong> Up-to-date information on cheap flights and travel routes.</li>
                <li><strong>Technical Accuracy:</strong> Travel hubs reviewed with structural precision.</li>
                <li><strong>Network Security:</strong> Backed and monitored by TRTT Network standards.</li>
            </ul>
            <p>For official inquiries or partner details, visit our main network portal at <a href="https://trttnews24bd.blogspot.com" target="_blank">TRTT NEWS 24 BD</a>.</p>
            """
        },
        {
            "title": "Privacy Policy",
            "content": """
            <h2>Privacy Policy for FlightScoutPro</h2>
            <p>At <strong>FlightScoutPro</strong>, reachable from <em>https://flightscoutpro.blogspot.com</em>, one of our main priorities is the privacy of our visitors. This Privacy Policy document contains types of information that is collected and recorded by FlightScoutPro and how we use it.</p>

            <h3>Log Files</h3>
            <p>FlightScoutPro follows a standard procedure of using log files. These files log visitors when they visit websites. All hosting companies do this as part of hosting services' analytics. The information collected by log files includes internet protocol (IP) addresses, browser type, Internet Service Provider (ISP), date and time stamp, referring/exit pages, and possibly the number of clicks.</p>

            <h3>Cookies and Web Beacons</h3>
            <p>Like any other website, FlightScoutPro uses 'cookies'. These cookies are used to store information including visitors' preferences, and the pages on the website that the visitor accessed or visited. The information is used to optimize the users' experience by customizing our web page content based on visitors' browser type and/or other information.</p>

            <h3>Google DoubleClick DART Cookie</h3>
            <p>Google is one of a third-party vendor on our site. It also uses cookies, known as DART cookies, to serve ads to our site visitors based upon their visit to our site and other sites on the internet.</p>

            <h3>GDPR & CCPA Data Protection Rights</h3>
            <p>We would like to make sure you are fully aware of all of your data protection rights. Every user is entitled to the right to access, rectification, erasure, and data portability.</p>

            <h3>Consent</h3>
            <p>By using our website, you hereby consent to our Privacy Policy and agree to its terms and conditions.</p>
            """
        },
        {
            "title": "Terms and Conditions",
            "content": """
            <h2>Terms and Conditions</h2>
            <p>Welcome to <strong>FlightScoutPro</strong>!</p>
            <p>These terms and conditions outline the rules and regulations for the use of FlightScoutPro's Website, located at <em>https://flightscoutpro.blogspot.com</em>.</p>

            <h3>Content Disclaimer</h3>
            <p>By accessing this website we assume you accept these terms and conditions. Do not continue to use FlightScoutPro if you do not agree to take all of the terms and conditions stated on this page.</p>

            <h3>License & Intellectual Property</h3>
            <p>Unless otherwise stated, FlightScoutPro and/or its licensors own the intellectual property rights for all material on FlightScoutPro. All intellectual property rights are reserved under the umbrella of TRTT NEWS 24 BD Network.</p>
            """
        },
        {
            "title": "Contact Us",
            "content": """
            <h2>Contact Us</h2>
            <p>If you have any questions, feedback, or business queries regarding FlightScoutPro or our network partnership, please feel free to reach out to us.</p>

            <p><strong>Primary Contact Details:</strong></p>
            <ul>
                <li><strong>Website:</strong> <a href="https://flightscoutpro.blogspot.com">FlightScoutPro</a></li>
                <li><strong>Network Hub:</strong> <a href="https://trttnews24bd.blogspot.com" target="_blank">TRTT NEWS 24 BD</a></li>
                <li><strong>Technical Management:</strong> Managed via GitHub Actions & Blogger API v3</li>
            </ul>
            """
        }
    ]

    for page in pages_to_create:
        try:
            body = {
                "kind": "blogger#page",
                "title": page["title"],
                "content": page["content"]
            }
            request = service.pages().insert(blogId=BLOG_ID, body=body)
            response = request.execute()
            print(f"✅ Success: Created page '{page['title']}' - ID: {response.get('id')}")
        except Exception as e:
            print(f"❌ Error creating page '{page['title']}': {e}")

if __name__ == "__main__":
    if not BLOG_ID or not API_KEY:
        print("❌ Error: BLOG_ID or API_KEY is missing in GitHub Secrets!")
    else:
        print(f"🚀 Starting Auto-Setup for Blog ID: {BLOG_ID}")
        blogger = init_blogger_service()
        create_info_pages(blogger)
