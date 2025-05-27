#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from collections import namedtuple
from passlib.hash import django_pbkdf2_sha256
from datetime import datetime


class Database:
    def __init__(self, db_name="your_database.db"):
        self.db_name = db_name

    # -- Global functions --
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

    # -- Articles Page --
    def get_category_name(self, cat_id):
        query = "SELECT name FROM magasin_category WHERE cat_id = ?"
        result = self.fetch_namedtuple(query, [cat_id])
        return result[0].name

    def update_article(self, article_data, art_id, code):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()

                # Check if code already exists
                cursor.execute("SELECT art_id FROM magasin_article WHERE code = ? AND art_id != ?", (code, art_id))
                if cursor.fetchone():
                    return {'success': False, 'message': f"❌ Article avec ce code {code} existe déjà."}

                update_query = """
                UPDATE magasin_article
                SET category_id = ?, code = ?, slug = ?, designation = ?, ref = ?, umesure = ?, emp = ?,
                    qte = ?, prix = ?, valeur = ?, observation = ?
                WHERE art_id = ?
                """
                cursor.execute(update_query, article_data)
                conn.commit()
                return {'success': True, 'message': '✅ Article et mouvement ajoutés avec succès'}
        except sqlite3.Error as err:
            return {'success': False, 'message': f'❌ Erreur lors de l\'ajout: {str(err)}'}

    def insert_new_article(self, article_data, code, mov_date, qte, prix, user_id):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                conn.execute("BEGIN")  # Start transaction

                # Check if code already exists
                cursor.execute("SELECT art_id FROM magasin_article WHERE code = ?", (code,))
                if cursor.fetchone():
                    return {'success': False, 'message': f"❌ Article avec ce code {code} existe déjà."}

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
            return {'success': False, 'message': f"❌ Erreur lors de l'ajout: {str(err)}"}

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

    def process_stock_entry(self, article, ent_qte, ent_prix, ent_date, user_id):
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

    def process_stock_sortie(self, art_id, sortie_qte, sortie_date, user_id):
        """
        Process stock sortie in SQLite: update article quantity and log the movement.
        """
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

    def get_all_missing_codes(self, name):
        """
        Return a list of all missing article codes for a given category ID.

        Parameters:
            cat_id (int): Category ID.

        Returns:
            dict: {'success': True/False, 'missing_codes': list, 'message': str}
        """
        try:
            # Get the category slug
            category_row = self.fetch_all("SELECT cat_id FROM magasin_category WHERE name = ?", (name,))
            if not category_row:
                return {'success': False, 'missing_codes': [], 'message': "❌ Catégorie introuvable."}

            cat_id = category_row[0][0]

            # Get all codes for that category
            code_rows = self.fetch_all("SELECT code FROM magasin_article WHERE category_id = ?", (cat_id,))
            codes = [row[0] for row in code_rows]

            existing_numbers = []
            len_numbers = 3  # Default length of padding (e.g., 001)

            for code in codes:
                if '-' in code:
                    parts = code.split('-')
                    if len(parts) == 2 and parts[1].isdigit():
                        num_part = parts[1]
                        len_numbers = max(len_numbers, len(num_part))
                        existing_numbers.append(int(num_part))

            if not existing_numbers:
                return {
                    'success': True,
                    'missing_codes': [f"{name}-{1:0{len_numbers}d}"],
                    'message': "✅ Aucun code existant, premier code généré."
                }

            max_number = max(existing_numbers)
            missing = [f"{name}-{i:0{len_numbers}d}" for i in range(1, max_number + 1) if i not in existing_numbers]

            return {
                'success': True,
                'missing_codes': missing,
                'message': f"✅ {len(missing)} codes manquants trouvés."
            }

        except Exception as e:
            return {'success': False, 'missing_codes': [], 'message': f"❌ Erreur: {str(e)}"}

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

    def change_user_password(self, user_id, new_password, retype_password):
        """
        Change a user's password after verifying and matching the new password confirmation.

        Parameters:
            user_id (str): id of the user.
            new_password (str): New password.
            retype_password (str): New password confirmation.

        Returns:
            dict: { 'success': True/False, 'message': str }
        """
        if new_password != retype_password:
            return {'success': False, 'message': "❌ Les mots de passe ne correspondent pas."}

        try:
            with self.connect() as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT password FROM auth_user WHERE id = ?", (user_id,))
                row = cursor.fetchone()

                if not row:
                    return {'success': False, 'message': "❌ Utilisateur introuvable."}

                hashed_new_password = django_pbkdf2_sha256.hash(new_password)
                cursor.execute(
                    "UPDATE auth_user SET password = ? WHERE id = ?",
                    (hashed_new_password, user_id)
                )

                return {'success': True, 'message': "✅ Mot de passe mis à jour avec succès."}

        except Exception as e:
            return {'success': False, 'message': f"❌ Erreur: {str(e)}"}

    # -- Commande Page
    def commande_status(self, cmd_id):
        """
        This function will return False if command is active
        this behavor is used to enable or disable active status command pushButton
        """
        query = "SELECT status FROM magasin_command WHERE command_id = ?"
        result = self.fetch_all(query, [cmd_id])
        if len(result) == 0:
            return False
        else:
            return False if result[0][0] == 1 else True


if __name__ == '__main__':
    db_handler = Database('./db.sqlite3')
    # query = 'SELECT * FROM magasin_article WHERE art_id = ?'
    # result = db_handler.fetch_namedtuple(query, [3])
    # print(result)
    result = db_handler.get_all_missing_codes('BHS')
    print(result)
