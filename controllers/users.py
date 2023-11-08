# Description: This file contains the code for the Flask application.
from flask import Flask, request, jsonify # pip install flask
import mysql.connector # pip install mysql-connector-python
from dotenv import load_dotenv  # Ajout de cette ligne
from classes.userses import Users
from middleware.verifToken import verify_token
import os
import bcrypt

#from database import get_database_cursor
from database import db_singleton


load_dotenv()

# Création de l'application Flask
from .usersStrategy import GetAllUsersStrategy, GetSingleUserStrategy, CreateUserStrategy, UpdateUserStrategy

class users_Controller():
    def __init__(self, strategy=None):
        self.strategy = strategy

    def user_Method(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.strategy = GetAllUsersStrategy()
        elif request.method == 'POST':
            self.strategy = CreateUserStrategy()

        # Autres conditions pour d'autres méthodes HTTP

        return self.strategy.handle(request, *args, **kwargs)

    def user_MethodSpecifique(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.strategy = GetSingleUserStrategy()
        elif request.method == 'PUT':
            self.strategy = UpdateUserStrategy()

        # Autres conditions pour d'autres méthodes HTTP

        return self.strategy.handle(request, *args, **kwargs)


""" 
class users_Controller():
    def user_Method():
        # Create a database connection and cursor
        conn, cursor = db_singleton.get_cursor()

        if request.method == 'GET':
            verify_token(request.headers.get('Token'))
            if verify_token(request.headers.get('Token')) == 404:
                return jsonify({'error': 'Token invalide'}), 404
            elif verify_token(request.headers.get('Token')) == 505:
                return jsonify({'error': 'Token expiré'}), 505
            else:
                try:
                    query = "SELECT * FROM users"
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    users = []
                    for row in rows:
                        user_temp = Users.from_map({'id': row[0], 'username': row[1], 'password': row[2], 'email': row[3], 'first_name': row[4], 'last_name': row[5]})
                        users.append(user_temp.to_map())

                    return jsonify(users), 200
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()

        elif request.method == 'POST':
            try:
                # Get the JSON data sent by the client
                data = request.get_json()

                # Create a new user object from the JSON data
                user = Users.from_map(data)

                # Hash the password
                password_Hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


                # Insert the new user into the database
                query = "INSERT INTO users (username, password, mail, first_name, last_name) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (user.username, password_Hash, user.email, user.first_name, user.last_name))
                conn.commit()

                # Return the new user with the id generated by the database
                user.id = cursor.lastrowid
                return jsonify(user.to_map()), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                cursor.close()
                conn.close()
        
    
    def user_MethodSpecifique(users):
        # Create a database connection and cursor
        conn, cursor = db_singleton.get_cursor()

        verify_token(request.headers.get('Token'))
        if verify_token(request.headers.get('Token')) == 404:
            return jsonify({'error': 'Token invalide'}), 404
        elif verify_token(request.headers.get('Token')) == 505:
            return jsonify({'error': 'Token expiré'}), 505
        else:
            if request.method == 'GET':
                try:
                    cursor.execute("SELECT * FROM users WHERE username = %s", (users,))
                    users_selected = cursor.fetchone()

                    if users_selected is None:
                        return jsonify({'error': 'User not found'}), 404
                    users_selected = Users.from_map({'id': users_selected[0], 'username': users_selected[1], 'password': users_selected[2], 'email': users_selected[3], 'first_name': users_selected[4], 'last_name': users_selected[5]})
                    return jsonify(users_selected.to_map()), 200
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()

            elif request.method == 'PUT':
                try:
                    data = request.get_json()
                    users_selected = Users.from_map(data)
                    cursor.execute("UPDATE users SET username = %s, password = %s, mail = %s, first_name = %s, last_name = %s WHERE username = %s", (users_selected.username, users_selected.password, users_selected.email, users_selected.first_name, users_selected.last_name, users,))
                    conn.commit()
                    return jsonify(users_selected.to_map()), 200
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()

 """
                
