"""Vercel status endpoint. This handler does not create or publish Blogger posts."""
MARKER = "787950 LOCKED"

def handler(request):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json", "Cache-Control": "no-store"},
        "body": {
            "status": "ready",
            "marker": MARKER,
            "publishing_mode": "DRAFT_ONLY",
            "message": "Review Blogger drafts manually before publishing.",
        },
    }
