import cherrypy
import webbrowser
import requests
from dotenv import load_dotenv
import os
import json

# Load credentials
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
USERS_FILE = "users.json"

# Ensure users file exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({}, f, indent=2)

def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

class StravaAuthApp:
    @cherrypy.expose
    def index(self):
        return "Strava Auth Server Running. Go to /authorize to begin."

    @cherrypy.expose
    def authorize(self):
        # Launch browser with authorization URL
        auth_url = (
            f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}"
            f"&response_type=code&redirect_uri={REDIRECT_URI}"
            f"&approval_prompt=auto&scope=activity:read_all"
        )
        webbrowser.open(auth_url)
        return "Opened browser for Strava OAuth. Check your browser!"

    @cherrypy.expose
    def exchange_token(self, code=None, scope=None, state=None):
        if not code:
            cherrypy.response.status = 400
            return "Missing authorization code."

        # Exchange code for token
        response = requests.post("https://www.strava.com/oauth/token", data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        })

        if response.status_code != 200:
            cherrypy.response.status = 400
            return f"Token exchange failed: {response.text}"

        data = response.json()
        athlete = data.get('athlete', {})
        user_id = str(athlete.get('id'))

        user_entry = {
            "firstname": athlete.get("firstname"),
            "lastname": athlete.get("lastname"),
            "access_token": data.get("access_token"),
            "refresh_token": data.get("refresh_token"),
            "expires_at": data.get("expires_at")
        }

        users = load_users()
        users[user_id] = user_entry
        save_users(users)

        print(f"Saved user {user_id} ({athlete.get('firstname')} {athlete.get('lastname')})")

        return "Authorization complete. You may close this window."

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
    })
    cherrypy.quickstart(StravaAuthApp())

