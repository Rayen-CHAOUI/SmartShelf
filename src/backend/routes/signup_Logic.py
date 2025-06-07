from backend.Save_Data.save_user import load_users, save_users

######### signup logic with auto-increment ID

def signup(username, password):
    users = load_users()

    # Check if username already exists
    if any(u["username"] == username for u in users):
        return False, "Username already exists."

    # Generate new auto-increment ID
    if users:
        last_id = max(int(u["id"]) for u in users if "id" in u and u["id"].isdigit())
        new_id = str(last_id + 1)
    else:
        new_id = "1"

    users.append({
        "id": new_id,
        "username": username,
        "password": password  # Consider hashing this in production
    })

    save_users(users)
    return True, "Signup successful."
