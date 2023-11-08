import mysql.connector
import os
from flask import jsonify # pip install flask
import csv

# Nouveau code avec singleton
class DatabaseSingleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
            cls._instance._conn = None
            cls._instance._cursor = None
            cls._instance.connect()
        return cls._instance
    def connect(self):
        if self._conn is None or not self._conn.is_connected():
            try:
                self._conn = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME")
                )
                self._cursor = self._conn.cursor()
            except Exception as e:
                # Gérer les erreurs de connexion
                print(f"Erreur lors de la connexion à la base de données : {str(e)}")
    def get_cursor(self):
        self.connect()  # Assurez-vous que la connexion est établie avant chaque requête
        try:
            if self._conn is not None and self._conn.is_connected():
                cursor = self._conn.cursor()
                return self._conn, cursor
            else:
                return jsonify("Erreur de connexion à la base de données.")
        except Exception as e:
            return jsonify(f"Erreur lors de la connexion à la base de données : {str(e)}")
        
# Utilisez cette instance unique pour la connexion à la base de données
db_singleton = DatabaseSingleton()

""" class DatabaseToCSVAdapter:
    def __init__(self, database):
        self.database = database

    def execute_query_and_export_to_csv(self, query, query_params, csv_file_path):
        conn, cursor = self.database.get_cursor()
        cursor.execute(query, query_params)
        rows = cursor.fetchall()

        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
 """

