# Description: This file contains the code for the Flask application.
from flask import Flask, request, jsonify # pip install flask
import mysql.connector # pip install mysql-connector-python
from dotenv import load_dotenv  # Ajout de cette ligne
from classes.userses import Users
import os
import bcrypt

import jwt
from datetime import datetime, timedelta
from middleware.verifToken import verify_token
from database import get_database_cursor

load_dotenv()

secret_key = os.getenv("SECRET_KEY")



class auth_Controller():

    def auth_method():
        conn, cursor = get_database_cursor()
        if request.method == "POST":
            try: 
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')
                if not username or not password:
                    return jsonify({'error': 'Missing username or password'}), 400
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                if not user:
                    return jsonify({'error': 'l\'Username n\'existe pas'}), 403
                if bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):

                    # Durée de validité du token (3 heure)
                    expiration_time = datetime.utcnow() + timedelta(hours=3)

                    token = jwt.encode({"exp": expiration_time, "username": username}, secret_key, algorithm="HS256")
                    return jsonify({"token": token}), 200

                else:
                    return jsonify({'error': 'Mot de passe incorrect'}), 403
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                cursor.close()
                conn.close()

            
                            

