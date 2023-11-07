# Description: This file contains the code for the Flask application.
from flask import Flask, request, jsonify # pip install flask
import mysql.connector # pip install mysql-connector-python
from dotenv import load_dotenv  # Ajout de cette ligne
from classes.universes import Univers
from middleware.verifToken import verify_token
import jwt
import os
from database import db_singleton

load_dotenv()
secret_key = os.getenv("SECRET_KEY")




class Univers_Controller():
    # Définition des routes pour les univers
    @staticmethod
    def universMethod():
        # Create a database connection and cursor
        conn, cursor = db_singleton.get_cursor()
        verify_token(request.headers.get('Token'))
        if verify_token(request.headers.get('Token')) == 404:
            return jsonify({'error': 'Token invalide'}), 404
        elif verify_token(request.headers.get('Token')) == 505:
            return jsonify({'error': 'Token expiré'}), 505
        else:
            user = jwt.decode(request.headers.get('Token'), secret_key, algorithms=["HS256"])
            cursor.execute("SELECT id FROM users WHERE username = %s", (user['username'],))
            user_id = cursor.fetchone()

            if request.method == 'GET':
                try:
                    cursor.execute("SELECT * FROM univers WHERE user_id = %s", (user_id[0],))
                    rows = cursor.fetchall()
                    universes = []
                    for row in rows:
                        universe_temp = Univers.from_map({'id': row[0], 'name': row[1], 'description': row[2], 'user_id': row[3]})
                        universes.append(universe_temp.to_map())
                    return jsonify(universes), 200
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()

            elif request.method == 'POST':
                data = request.json
                universe = Univers.from_map(data)
                universe.generate_description()
                try:
                    cursor.execute("SELECT * FROM univers WHERE name = %s AND user_id = %s", (data['name'], user_id[0],))
                    row = cursor.fetchone()
                    if row is not None:
                        return jsonify({'error': 'L\'univers existe déjà.'}), 409
                    else:
                        cursor.execute("""INSERT INTO univers (name, description, user_id) 
                                       VALUES (%s, %s, %s)""", (data['name'], universe.description, user_id[0],)) # Insert the universe name into the database
                        conn.commit() # Commit the changes to the database
                        return jsonify({'message': f'Univers {data["name"]} créé avec succès!  {user["username"]} id : {user_id[0]} avec la description suivante : {universe.description}'}), 201
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()
    @staticmethod
    def universMethodSpecifique(univers):
        # Create a database connection and cursor
        conn, cursor = db_singleton.get_cursor()
        verify_token(request.headers.get('Token'))
        if verify_token(request.headers.get('Token')) == 404:
            return jsonify({'error': 'Token invalide'}), 404
        elif verify_token(request.headers.get('Token')) == 505:
            return jsonify({'error': 'Token expiré'}), 505
        else:
            user = jwt.decode(request.headers.get('Token'), secret_key, algorithms=["HS256"])
            cursor.execute("SELECT id FROM users WHERE username = %s", (user['username'],))
            user_id = cursor.fetchone()
            if request.method == 'GET':
                try:
                    cursor.execute("SELECT * FROM univers WHERE name = %s AND user_id = %s", (univers, user_id[0],))
                    rows = cursor.fetchall()
                    if not rows:
                        # Aucun résultat trouvé pour cet univers
                        return jsonify({'error': 'L\'univers n\'existe pas.'}), 404
                    universes = []
                    for row in rows:
                        universe_temp = Univers.from_map({'id': row[0], 'name': row[1], 'description': row[2], 'user_id': row[3]})
                        universes.append(universe_temp.to_map())
                    return jsonify(universes), 200
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()

            elif request.method == 'PUT':
                data = request.json
                univers_2 = Univers.from_map(data)
                univers_2.generate_new_description(data['new_name'])
                try:
                    cursor.execute("SELECT id FROM univers WHERE name = %s AND user_id = %s", (univers ,user_id[0],))
                    universSelect_id = cursor.fetchone()
                    #return jsonify(universSelect_id, univers_2.new_description, univers , user_id[0])
                    if universSelect_id is None:
                        # Aucun résultat trouvé pour cet univers
                        return jsonify({'error': 'L\'univers n\'existe pas.'}), 404
                    else:
                        cursor.execute("""UPDATE univers SET name = %s, description = %s 
                                       WHERE id = %s AND user_id = %s""", (data['new_name'], univers_2.new_description, universSelect_id[0], user_id[0],))
                        conn.commit()
                        return jsonify({"message": f"Modification de l'univers {univers} en {data['new_name']} avec la description suivante : {univers_2.new_description}"}), 200
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()        

            elif request.method == 'DELETE':
                try:
                    cursor.execute("SELECT id FROM univers WHERE name = %s AND user_id = %s", (univers, user_id[0],))
                    univers_data = cursor.fetchone()
                    if univers_data is not None and isinstance(univers_data, tuple):
                        universe = Univers.from_map({'id': univers_data[0], 'name': univers})
                        cursor.execute("DELETE FROM personnages WHERE univers_id = %s AND user_id = %s", (universe.id, user_id[0],))
                        cursor.execute("DELETE FROM univers WHERE id = %s AND user_id = %s", (universe.id, user_id[0],))
                        conn.commit()
                        return jsonify({"message": f"Suppression de l'univers {universe.name} de votre compte {user['username']} id :{user_id[0]} ainsi que les personnages qui contiennent cet univers"}), 200
                    elif univers_data is None:
                        return jsonify({"error": 'Cet univers n\'existe pas.'}), 404
                    else:
                        return jsonify({"error": 'Cet univers n\'a pas été supprimé de votre compte.'}), 505
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()
                