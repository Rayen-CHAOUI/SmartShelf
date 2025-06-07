# src/backend/data/save_user.py

import json
import os

# Define the path to the users.json file
DATA_DIR = os.path.dirname(__file__)
USERS_FILE = os.path.join(DATA_DIR, "users.json")

# Load users from the file
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []  # Return empty list if file is corrupted

# Save users to the file
def save_users(users):
    os.makedirs(DATA_DIR, exist_ok=True)  # Ensure directory exists
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)
