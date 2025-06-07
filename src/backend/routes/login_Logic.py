# src/backend/routes/loginLogic.py
from backend.Save_Data.save_user import load_users

 
########## login logic

def login(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True, "Login successful."
    return False, "Invalid username or password."


