#!/usr/bin/env python3
import hashlib

class AuthenticationManager:
    def __init__(self, users_data):
        self.users_data = users_data

    def authenticate_user(self, username, password):
        hashed_password = self.users_data.get(username, {}).get("password", "")
        return hashed_password and hashlib.sha256(password.encode()).hexdigest() == hashed_password

