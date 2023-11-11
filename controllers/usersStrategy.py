# Description: This file contains the code for the Flask application.
from flask import Flask, request, jsonify # pip install flask
import mysql.connector # pip install mysql-connector-python
from dotenv import load_dotenv  # Ajout de cette ligne
from classes.userses import Users
from middleware.verifToken import verify_token
import os
import bcrypt
from database import db_singleton
load_dotenv()

class UserHandlingStrategy:
    def handle(self, request, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")

class GetAllUsersStrategy(UserHandlingStrategy):
    def handle(self, request, *args, **kwargs):
        # Create a database connection and cursor
        conn, cursor = db_singleton.get_cursor()
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


class GetSingleUserStrategy(UserHandlingStrategy):
    def handle(self, request, *args, **kwargs):
        conn, cursor = db_singleton.get_cursor()
        verify_token(request.headers.get('Token'))
        if verify_token(request.headers.get('Token')) == 404:
            return jsonify({'error': 'Token invalide'}), 404
        elif verify_token(request.headers.get('Token')) == 505:
            return jsonify({'error': 'Token expiré'}), 505
        else:
            try:
                # Obtenez le nom d'utilisateur à partir de la requête
                user_name = kwargs.get('users')
                cursor.execute("SELECT * FROM users WHERE username = %s", (user_name,))
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

class CreateUserStrategy(UserHandlingStrategy):
    
    def handle(self, request, *args, **kwargs):
        conn, cursor = db_singleton.get_cursor()
        verify_token(request.headers.get('Token'))
        if verify_token(request.headers.get('Token')) == 404:
            return jsonify({'error': 'Token invalide'}), 404
        elif verify_token(request.headers.get('Token')) == 505:
            return jsonify({'error': 'Token expiré'}), 505
        else:
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


class UpdateUserStrategy(UserHandlingStrategy):
    def handle(self, request, *args, **kwargs):
        conn, cursor = db_singleton.get_cursor()

        verify_token(request.headers.get('Token'))
        if verify_token(request.headers.get('Token')) == 404:
            return jsonify({'error': 'Token invalide'}), 404
        elif verify_token(request.headers.get('Token')) == 505:
            return jsonify({'error': 'Token expiré'}), 505
        else:
            try:
                data = request.get_json()
                users_selected = Users.from_map(data)
                user_name = kwargs.get('users')
                cursor.execute("UPDATE users SET username = %s, password = %s, mail = %s, first_name = %s, last_name = %s WHERE username = %s", (users_selected.username, users_selected.password, users_selected.email, users_selected.first_name, users_selected.last_name, user_name,))
                conn.commit()
                return jsonify(users_selected.to_map()), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                cursor.close()
                conn.close()