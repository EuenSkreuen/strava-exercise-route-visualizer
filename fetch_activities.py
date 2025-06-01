import requests
import json
import os
import time

USERS_FILE = "users.json"
DATA_DIR = "data"

# Ensure data folder exists
os.makedirs(DATA_DIR, exist_ok=True)

# Load users
with open(USERS_FILE, 'r') as f:
    users = json.load(f)

for user_id, user in users.items():
    print(f"Fetching activities for {user['firstname']} {user['lastname']} (ID: {user_id})")

    activities = []
    page = 1
    per_page = 200

    headers = {
        "Authorization": f"Bearer {user['access_token']}"
    }

    while True:
        response = requests.get(
            "https://www.strava.com/api/v3/athlete/activities",
            headers=headers,
            params={"page": page, "per_page": per_page}
        )

        if response.status_code == 401:
            print(f"Unauthorized for user {user_id}. Access token may have expired.")
            break

        if response.status_code != 200:
            print(f"Error fetching page {page}: {response.status_code} - {response.text}")
            break

        data = response.json()

        if not data:
            break  # No more pages

        activities.extend(data)

        print(f"Fetched page {page} with {len(data)} activities.")
        page += 1

        # Rate limit: pause a bit between pages
        time.sleep(1)

    # Save to file
    output_path = os.path.join(DATA_DIR, f"{user_id}.json")
    with open(output_path, "w") as out:
        json.dump(activities, out, indent=2)

    print(f"Saved {len(activities)} activities to {output_path}")
