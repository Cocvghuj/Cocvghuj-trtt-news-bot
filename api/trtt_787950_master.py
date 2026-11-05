import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

MARKER = '787950 LOCKED'

# তোমার Secrets থেকে নেবে - তুমি যা বসিয়েছো
BLOG_IDS = [
    os.environ.get('BLOGGER_BLOG_ID'),
    os.environ.get('BLOGGER_BLOG_ID_2')  # flightscoutpro এর জন্য যেটা বানাবে
]

def get_service():
    creds = Credentials(
        token=None,
        refresh_token=os.environ.get('BLOGGER_REFRESH_TOKEN'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.environ.get('GOOGLE_OAUTH_CLIENT_ID'),
        client_secret=os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET'),
        scopes=['https://www.googleapis.com/auth/blogger']
    )
    return build('blogger', 'v3', credentials=creds)

def auto_push_post(title, content):
    service = get_service()
    tagged_content = f"{content}<br/><p><b>{MARKER}</b></p>"
    results = []
    for bid in BLOG_IDS:
        if bid and bid.strip():
            body = {
                'kind': 'blogger#post',
                'title': title,
                'content': tagged_content,
                'labels': [MARKER, 'TRTT', 'Travel']
            }
            results.append(service.posts().insert(blogId=bid, body=body, isDraft=False).execute())
    return results

# Vercel Python handler - এটাই সঠিক
def handler(request):
    return {
        "statusCode": 200,
        "body": f"Bot operational - Marker {MARKER} - Blogs: {BLOG_IDS}"
    }
