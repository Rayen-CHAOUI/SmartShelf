from backend.Save_Data.save_user import load_users, save_users

def remove_user(user_id):
    users = load_users()
    updated_users = [user for user in users if user["id"] != user_id]

    if len(updated_users) == len(users):
        return False, "User ID not found."

    save_users(updated_users)
    return True, "User removed successfully."
