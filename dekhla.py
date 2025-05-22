#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from passlib.hash import django_pbkdf2_sha256
import sqlite3


class User:
    def __init__(self, user_id, username, is_admin, groupe):
        self.id = user_id
        self.username = username
        self.role = 'admin' if is_admin else 'user'
        self.groupe = groupe


class LoginManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def authenticate(self, username, raw_password):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT auth_user.id, username, password, is_superuser, p.groupe
                FROM auth_user
                LEFT JOIN accounts_profile AS p ON auth_user.id = p.user_id
                WHERE username = ?
            """, (username,))
            result = cursor.fetchone()

            if result:
                user_id, uname, hashed_password, is_superuser, groupe = result
                if django_pbkdf2_sha256.verify(raw_password, hashed_password):
                    return User(user_id, uname, is_superuser, groupe)
        return None


if __name__ == '__main__':

    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")

    login_manager = LoginManager("./db.sqlite3")
    user = login_manager.authenticate(username, password)
    if user:
        print(f"Bienvenue {user.username} {user.role}!")
    else:
        print("Identifiants incorrects.")
