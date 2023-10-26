# Description: This file contains the code for the Flask application.
from flask import Flask, request, jsonify # pip install flask
import mysql.connector # pip install mysql-connector-python
from dotenv import load_dotenv  # Ajout de cette ligne
from classes.universes import Univers
from classes.verifToken import verify_token
import jwt
import os


load_dotenv()

secret_key = os.getenv("SECRET_KEY")

# Connectez-vous à la base de données
def get_database_cursor():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    return conn, cursor


class Univers_Controller():
    # Définition des routes pour les univers
    
    def universMethod():
        # Create a database connection and cursor
        conn, cursor = get_database_cursor()
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

                    cursor.execute("INSERT INTO univers (name, description, user_id) VALUES (%s, %s, %s)", (data['name'], universe.description, user_id[0],)) # Insert the universe name into the database
                    conn.commit() # Commit the changes to the database
                    return jsonify({'message': f'Univers {data["name"]} créé avec succès! sur votre compte {user["username"]} {user_id[0]}'}), 201
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()
        
    def universMethodSpecifique(univers):
        # Create a database connection and cursor
        conn, cursor = get_database_cursor()
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
                        return jsonify({'error': 'L\'univers n\'existe pas'}), 404

                    universes = []
                    for row in rows:
                        universe_temp = Univers.from_map({'id': row[0], 'name': row[1], 'description': row[2]})
                        universes.append(universe_temp.to_map())

                    return jsonify(universes), 200

                except Exception as e:
                    return jsonify({'error': str(e)}), 500

                finally:
                    cursor.close()
                    conn.close()
            
            #faut que je rajoute dans le PUT le fait de changer la description
            elif request.method == 'PUT':
                conn, cursor = get_database_cursor()
                try:
                    # Get the JSON data from the request
                    data = request.json

                    # Fetch the universe ID from the database using the name
                    cursor.execute("SELECT * FROM univers WHERE name = %s AND user_id = %s", (univers,user_id[0],))
                    row = cursor.fetchone()

                    if row is not None:
                        # Create an instance of Univers using from_map
                        universe = Univers.from_map({'id': row[0], 'name': row[1], 'description': row[2]})

                        # Update the name attribute
                        universe.name = data['new_name']

                        # Update the database
                        cursor.execute("UPDATE univers SET name = %s WHERE id = %s", (universe.name, universe.id))
                        conn.commit()

                        # Return a JSON response for success
                        return jsonify({"message": f"Modification de l'univers {univers} en {universe.name}"}), 200
                    else:
                        # Aucun résultat trouvé pour cet univers
                        return jsonify({"error": 'Cet univers n\'existe pas.'}), 404

                except Exception as e:
                    return jsonify({'error': str(e)}), 500

                finally:
                    cursor.close()
                    conn.close()

            elif request.method == 'DELETE':
                try:
                    cursor.execute("SELECT id FROM univers WHERE name = %s", (univers,))
                    univers_data = cursor.fetchone()

                    if univers_data is not None and isinstance(univers_data, tuple):
                        universe = Univers.from_map({'id': univers_data[0], 'name': univers})
                        cursor.execute("DELETE FROM personnages WHERE univers_id = %s", (universe.id,))
                        cursor.execute("DELETE FROM univers WHERE id = %s", (universe.id,))
                        conn.commit()

                        return jsonify({"message": f"Suppression de l'univers {universe.name} ainsi que les personnages qui contiennent cet univers"}), 200

                    elif univers_data is None:
                        return jsonify({"error": 'Cet univers n\'existe pas.'}), 404

                    else:
                        return jsonify({"error": 'Cet univers n\'a pas été supprimé.'}), 505

                except Exception as e:
                    return jsonify({'error': str(e)}), 500

                finally:
                    cursor.close()
                    conn.close()
                