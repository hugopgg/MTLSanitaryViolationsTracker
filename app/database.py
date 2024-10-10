# ============================================
# Auteur: Hugo Perreault Gravel 
# ============================================

import sqlite3
from models.violation import Violation
from models.violationSummary import ViolationSummary

# ============================================
# Utility Class for Database Operations
# ============================================

DB_PATH = "db/database.db"


class Database:
    def __init__(self):
        self.connection = None

    # ============================
    # Connection
    # ============================

    # Get database connection
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(DB_PATH)
        return self.connection

    # Disconnect from database
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # ============================
    # Violations
    # ============================

    # Get all violations
    def get_all_violations(self):
        cursor = self.get_connection().cursor()
        query = "SELECT * FROM violations"
        cursor.execute(query)
        violations = cursor.fetchall()
        if violations is None:
            return None
        else:
            return [Violation(*violation) for violation in violations]

    # Get all establishments
    def get_all_etablissements(self):
        cursor = self.get_connection().cursor()
        query = "SELECT DISTINCT etablissement,\
            buisness_id FROM violations ORDER BY etablissement"
        cursor.execute(query)
        etablissements = cursor.fetchall()
        if etablissements is None:
            return None
        else:
            return etablissements

    # Delete all violations
    def delete_all_violations(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM violations"
        cursor.execute(query)
        connection.commit()

    # Delete all violations from buisness_id
    def delete_violations_by_buisness_id(self, buisness_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM violations WHERE buisness_id = ?"
        cursor.execute(query, (buisness_id,))
        connection.commit()

    # Insert all violations from a batch
    def insert_all_violations(self, violations):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO violations (id_poursuite,\
            buisness_id, date, description, adresse, date_jugement,\
                etablissement, montant, proprietaire, ville,\
                    statut,\
                        date_statut,\
                            categorie)\
                                VALUES (?, ?, ?, ?, ?, ?,\
                                    ?, ?, ?, ?, ?, ?, ?)"
        cursor.executemany(query, violations)
        connection.commit()

    # Search violations from criteria and search type
    def get_violations_from_search(self, criteria, search_type):
        cursor = self.get_connection().cursor()
        criteria_like = f"%{criteria}%"
        if search_type == "etablissement":
            query = "SELECT * FROM violations WHERE etablissement LIKE ?"
        elif search_type == "proprietaire":
            query = "SELECT * FROM violations WHERE proprietaire LIKE ?"
        elif search_type == "rue":
            query = "SELECT * FROM violations WHERE adresse LIKE ?"
        else:
            return None
        cursor.execute(query, (criteria_like,))
        violations = cursor.fetchall()
        if violations is None:
            return None
        else:
            return [Violation(*violation) for violation in violations]

    # Get violations between dates
    def get_violations_between_dates(self, start_date, end_date):
        cursor = self.get_connection().cursor()
        query = "SELECT * FROM violations WHERE date BETWEEN ? AND ?"
        cursor.execute(query, (start_date, end_date))
        violations = cursor.fetchall()
        if violations is None:
            return None
        else:
            return [Violation(*violation) for violation in violations]

    # Get violations from business ID
    def get_violations_by_buisness_id(self, buisness_id):
        cursor = self.get_connection().cursor()
        query = "SELECT * FROM violations WHERE buisness_id = ?"
        cursor.execute(query, (buisness_id,))
        violations = cursor.fetchall()
        if violations is None:
            return None
        else:
            return [Violation(*violation) for violation in violations]

    # Get violations summary
    def get_violations_summary(self):
        cursor = self.get_connection().cursor()
        query = "SELECT etablissement,\
            COUNT(*) as count FROM violations\
                GROUP BY etablissement ORDER BY count DESC"
        cursor.execute(query)
        violations_summary = cursor.fetchall()
        if violations_summary is None:
            return None
        else:
            return [
                ViolationSummary(row[0], row[1]) for row in violations_summary
            ]

    # Update etablissement by buisness_id
    def update_etablissement_by_buisness_id(
        self, buisness_id, new_etablissement
    ):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = "UPDATE violations SET etablissement = ? WHERE buisness_id = ?"
        cursor.execute(query, (new_etablissement, buisness_id))
        connection.commit()

    # ============================
    # Inspection Requests
    # ============================

    # Insert inspection request
    def insert_demande_inspection(
        self,
        etablissement,
        adresse,
        ville,
        date_demande,
        nom_client,
        description_demande,
    ):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO demandes_inspection \
            (etablissement, adresse,\
                ville, date_demande,\
                    nom_client,\
                        description_demande) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(
            query,
            (
                etablissement,
                adresse,
                ville,
                date_demande,
                nom_client,
                description_demande,
            ),
        )
        connection.commit()

    # Delete inspection request from demande_id
    def delete_inspection_request(self, id_demande):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM demandes_inspection WHERE id_demande = ?"
        cursor.execute(query, (id_demande,))
        connection.commit()

    # ============================
    # Users
    # ============================

    # get login info
    def get_login_info(self, username):
        cursor = self.get_connection().cursor()
        query = "select salt, hash from users where username=?"
        cursor.execute((query), (username,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0], user[1]

    # create user
    def insert_user(
        self, nom, prenom, username, email, salt, hash, etablissements
    ):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            (
                "insert into users(nom, prenom, username, email,\
                    salt, hash, etablissements_list) "
                "values(?, ?, ?, ?, ?, ?, ?)"
            ),
            (nom, prenom, username, email, salt, hash, etablissements),
        )
        connection.commit()

    # return true if username exists
    def username_exist(self, username):
        cursor = self.get_connection().cursor()
        query = "SELECT COUNT(*) FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        count = cursor.fetchone()[0]
        return count > 0
