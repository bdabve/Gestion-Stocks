#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from collections import namedtuple
from passlib.hash import django_pbkdf2_sha256
from datetime import datetime


class Database:
    def __init__(self, db_name="your_database.db"):
        self.db_name = db_name

    def connect(self):
        """Create and return a database connection."""
        return sqlite3.connect(self.db_name)

    def fetch_all(self, query, params=None):
        """Fetch all rows from a SELECT query."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            return cursor.fetchall()

    def fetch_namedtuple(self, query, params=None):
        """
        Executes a SELECT query and returns results as a list of namedtuples.
        """
        with self.connect() as conn:
            conn.row_factory = sqlite3.Row  # enables accessing by column name
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            rows = cursor.fetchall()

            if not rows:
                return []

            RowTuple = namedtuple("Row", rows[0].keys())
            return [RowTuple(*row) for row in rows]

    def execute_query(self, query, params=None):
        """Execute an INSERT, UPDATE, or DELETE query."""
        with self.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params or [])
                conn.commit()
                return {'success': True}
            except sqlite3.Error as err:
                return {'success': False, 'message': str(err)}

    def get_item_id(self, id_name, table_name, column_name, value):
        """
        Get the ID of a row based on a specific column value.
        Example: get_item_id("prod_id", "products", "name", "Apple")
        """
        query = f"SELECT {id_name} FROM {table_name} WHERE {column_name} = ?"
        result = self.fetch_all(query, [value])
        return result[0][0] if result else None

    def get_category_name(self, cat_id):
        query = "SELECT name FROM magasin_category WHERE cat_id = ?"
        result = self.fetch_namedtuple(query, [cat_id])
        return result[0].name

    def insert_new_article(self, article_data, mov_date, qte, prix):
        user_id = 1  # Placeholder for user ID, replace with actual user ID logic
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                conn.execute("BEGIN")  # Start transaction

                # Step 2: Insert into magasin_article
                fields = [
                    'created',
                    'category_id',
                    'code', 'slug',
                    'designation', 'ref', 'umesure', 'emp',
                    'qte', 'prix', 'valeur', 'observation'
                ]
                placeholders = ', '.join('?' for _ in fields)
                insert_article_query = f'INSERT INTO magasin_article({", ".join(fields)}) VALUES({placeholders})'
                cursor.execute(insert_article_query, article_data)

                # Get the last inserted article ID
                art_id = cursor.lastrowid

                # --- Insert into magasin_movement
                insert_movement_query = '''
                INSERT INTO magasin_movement(art_id_id, movement_date, user_id_id, movement, qte, prix)
                VALUES (?, ?, ?, ?, ?, ?)
                '''
                movement_params = [art_id, mov_date, user_id, 'Initial', qte, prix]
                cursor.execute(insert_movement_query, movement_params)
                conn.commit()
                return {'success': True, 'lastrowid': art_id, 'message': '✅ Article et mouvement ajoutés avec succès'}
        except sqlite3.Error as err:
            return {'success': False, 'message': f'❌ Erreur lors de l\'ajout: {str(err)}'}

    def article_has_movement(self, art_id):
        """
        Chack if a product has movements
        """
        query = "SELECT movement_id FROM magasin_movement WHERE art_id_id = ?"
        result = self.fetch_all(query, [art_id])
        return True if result else False

    def article_movements(self, art_id):
        """
        Get all movement for art_id_id
        """
        query = '''SELECT DATE(mov.movement_date) AS mov_date, user.username, mov.movement, art.code,
                   art.designation, mov.qte, mov.prix
                   FROM magasin_movement AS mov
                   INNER JOIN magasin_article AS art ON mov.art_id_id = art.art_id
                   INNER JOIN auth_user AS user ON user.id = mov.user_id_id
                   WHERE mov.art_id_id = ? ORDER BY mov_date DESC'''
        result = self.fetch_all(query, [art_id])
        return result

    def process_stock_entry(self, article, ent_qte, ent_prix, ent_date):
        user_id = 1  # Placeholder for user ID, replace with actual user ID logic
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                # --- Calculate new stock values ---
                new_qte = article.qte + ent_qte
                if ent_prix != article.prix:
                    total_val = (ent_qte * ent_prix) + article.valeur
                    new_prix = total_val / new_qte
                else:
                    new_prix = article.prix

                new_valeur = new_qte * new_prix
                # --- Update article stock and price ---
                update_query = "UPDATE magasin_article SET qte = ?, prix = ?, valeur = ? WHERE art_id = ?"
                cursor.execute(update_query, [new_qte, new_prix, new_valeur, article.art_id])
                # --- Insert movement record ---
                insert_query = """
                    INSERT INTO magasin_movement (art_id_id, movement_date, movement, qte, prix, user_id_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                cursor.execute(insert_query, [article.art_id, ent_date, 'Entree', ent_qte, ent_prix, user_id])
                # --- Commit if all succeeds ---
                conn.commit()
            return {'success': True}
        except sqlite3.Error as e:
            return {'success': False, 'message': str(e)}

    def process_stock_sortie(self, art_id, sortie_qte, sortie_date):
        """
        Process stock sortie in SQLite: update article quantity and log the movement.
        """
        user_id = 1  # Placeholder for user ID, replace with actual user ID logic
        try:
            with self.connect() as conn:
                cursor = conn.cursor()

                # --- Fetch current qte and prix --
                cursor.execute("SELECT qte, prix FROM magasin_article WHERE art_id = ?", (art_id,))
                row = cursor.fetchone()
                if not row:
                    return {'success': False, 'message': 'Article non trouvé'}

                current_qte, prix = row

                # --- Check stock is sufficient ---
                if sortie_qte > current_qte:
                    return {'success': False, 'message': 'Stock insuffisant pour la sortie'}

                # --- Calculate new stock values ---
                new_qte = current_qte - sortie_qte
                new_valeur = new_qte * prix

                # --- Update article stock and price ---
                cursor.execute(
                    "UPDATE magasin_article SET qte = ?, valeur = ? WHERE art_id = ?",
                    (new_qte, new_valeur, art_id)
                )

                # --- Insert movement record ---
                cursor.execute(
                    """
                    INSERT INTO magasin_movement (art_id_id, movement_date, movement, qte, prix, user_id_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (art_id, sortie_date, "Sortie", sortie_qte, prix, user_id)
                )
                conn.commit()           # --- Commit if all succeeds ---
                return {'success': True}

        except sqlite3.Error as err:
            return {'success': False, 'message': str(err)}

    # -- USERS --
    def create_user(self, username, email, password, retype_password, first_name, last_name,
                    poste_travaille, groupe, is_superuser=False):
        """
        Create a new user with hashed password and related profile, after validating.

        Returns:
            dict: {'success': True/False, 'message': str}
        """
        if password != retype_password:
            return {'success': False, 'message': "❌ Les mots de passe ne correspondent pas."}

        try:
            hashed_password = django_pbkdf2_sha256.hash(password)
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with self.connect() as conn:
                cursor = conn.cursor()

                # Check if username already exists
                cursor.execute("SELECT id FROM auth_user WHERE username = ?", (username,))
                if cursor.fetchone():
                    return {'success': False, 'message': "❌ Ce nom d'utilisateur existe déjà."}

                # Insert into auth_user
                user_params = (username, email, hashed_password, first_name, last_name, int(is_superuser), today)
                cursor.execute("""
                    INSERT INTO auth_user (username, email, password, first_name, last_name,
                                           is_superuser, is_staff, is_active, date_joined)
                    VALUES (?, ?, ?, ?, ?, ?, 1, 1, ?)
                """, user_params)

                user_id = cursor.lastrowid

                # Insert into accounts_profile
                p_params = (user_id, poste_travaille, groupe)
                cursor.execute("INSERT INTO accounts_profile (user_id, poste_travaille, groupe) VALUES (?, ?, ?)", p_params)

                conn.commit()
                return {'success': True, 'message': f"✅ Utilisateur {username} créé avec succès."}

        except Exception as e:
            return {'success': False, 'message': f"❌ Erreur lors de la création de l'utilisateur: {str(e)}"}

    def update_user(self, user_id, username, fname, lname, email, poste_travaille, groupe):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                # -- Start transaction
                cursor.execute('BEGIN')
                # -- Update user in auth_user table
                cursor.execute(
                    'UPDATE auth_user SET username = ?, first_name = ?, last_name = ? , email = ? WHERE id = ?',
                    (username, fname, lname, email, user_id)
                )
                # -- Update user in profiles table
                cursor.execute(
                    'UPDATE accounts_profile SET poste_travaille = ?, groupe = ? WHERE user_id = ?',
                    (poste_travaille, groupe, user_id)
                )
                conn.commit()
                return {'success': True, 'message': '✅ Utilisateur modifié avec succès'}
        except sqlite3.Error as e:
            return {'success': False, 'message': str(e)}


if __name__ == '__main__':
    db_handler = Database('./db.sqlite3')
    query = 'SELECT * FROM magasin_article WHERE art_id = ?'
    result = db_handler.fetch_namedtuple(query, [3])
    print(result)
