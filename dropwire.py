import os
import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("RAINDROP_CLIENT_ID")
CLIENT_SECRET = os.getenv("RAINDROP_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"

# Step 1: Generate Authorization URL
def get_auth_url():
    return f"https://raindrop.io/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"

# Step 2: Local server to catch redirect, extract code, and exchange for token
class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/callback":
            query = parse_qs(parsed.query)
            code = query.get("code", [None])[0]
            if code:
                print(f"🔐 Received authorization code: {code}")
                token = exchange_code_for_token(code)
                if token:
                    print(f"\n✅ Access Token: {token}")
                    print("📌 Paste this into your .env file as RAINDROP_TOKEN")
                else:
                    print("❌ Failed to retrieve access token.")
            else:
                print("❌ Authorization code not found in callback.")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"You can close this tab.")
        else:
            self.send_response(404)
            self.end_headers()

# Function to exchange code for token
def exchange_code_for_token(code):
    url = "https://raindrop.io/oauth/access_token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Token exchange failed:", response.status_code, response.text)
        return None

def run_oauth_flow():
    print("🌐 Opening browser to authorize Raindrop app...")
    webbrowser.open(get_auth_url())

    print("🚀 Waiting for token...")
    httpd = HTTPServer(("localhost", 8000), OAuthHandler)
    httpd.handle_request()

RAINDROP_TOKEN = os.getenv("RAINDROP_TOKEN")
RAINDROP_API_URL = "https://api.raindrop.io/rest/v1/raindrops/0"  # 0 = default collection

def fetch_raindrop_items():
    headers = {
        "Authorization": f"Bearer {RAINDROP_TOKEN}"
    }
    response = requests.get(RAINDROP_API_URL, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch bookmarks: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    items = data.get("items", [])

    for item in items:
        print("🔹 Title:", item.get("title"))
        print("🔗 URL:", item.get("link"))
        print("📝 Note:", item.get("excerpt"))
        print("🏷️ Tags:", item.get("tags"))
        print("📅 Date:", item.get("created"))
        print("-" * 40)

    return items

if __name__ == "__main__":
    fetch_raindrop_items()
