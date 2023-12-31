# Description: This file contains the code for the Flask application.
from flask import Flask, request, jsonify # pip install flask
import mysql.connector # pip install mysql-connector-python
from controllers.univers import Univers_Controller
from dotenv import load_dotenv  # Ajout de cette ligne
from classes.personnageses import Personnage
from classes.universes import Univers
from middleware.verifToken import verify_token
import os
import jwt
from database import db_singleton

load_dotenv()
secret_key = os.getenv("SECRET_KEY")




class Personnages_Controller(Univers_Controller):
    # Définition des routes pour les personnages
    @staticmethod
    def PersonnagesMethod(univers):
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
                    # Get the universe ID from the database
                    cursor.execute("SELECT id FROM univers WHERE name = %s AND user_id = %s", (univers, user_id[0],))
                    univers_select_id = cursor.fetchone()
                    if not univers_select_id:
                        # Aucun résultat trouvé pour cet univers
                        return jsonify({'error': 'L\'univers n\'existe pas.'}), 404
                    # Get all the personnages from the database using JOIN
                    cursor.execute("""SELECT personnages.id, personnages.name, personnages.description, personnages.univers_id, univers.name as univers_name FROM personnages 
                                   INNER JOIN univers ON personnages.univers_id = univers.id 
                                   WHERE univers.id = %s AND personnages.user_id = %s""", (univers_select_id[0], user_id[0],))
                    personnages = cursor.fetchall()
                    # Convert the rows to Univers and Personnages instances
                    univers = Univers.from_map({'id': univers_select_id[0], 'name': univers})
                    personnages_list = []
                    for row in personnages:
                        personnage = Personnage.from_map({'id': row[0], 'name': row[1], 'description': row[2], 'univers_id': row[3]})
                        personnages_list.append(personnage.to_map())
                    return jsonify({"univers": univers.to_map(), "personnages": personnages_list}), 200
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()
            
            elif request.method == 'POST':
                data = request.json
                personnage = Personnage.from_map(data)
                try: 
                    # Get the universe ID from the database
                    cursor.execute("SELECT id FROM univers WHERE name = %s AND user_id = %s", (univers,user_id[0],))
                    univers_select_id = cursor.fetchone()

                    if not univers_select_id:
                        # Aucun résultat trouvé pour cet univers
                        return jsonify({'error': 'L\'univers n\'existe pas'}), 404
                    # Get all the personnages from the database using JOIN
                    cursor.execute("SELECT * FROM personnages WHERE name = %s", (data['name'],))
                    row = cursor.fetchone()
                    if row is not None:
                        name_personnage = row[1]
                        description_personnage = row[2]
                        cursor.execute("""INSERT INTO personnages (name, description, univers_id, user_id) 
                                     VALUES (%s, %s, %s, %s)""", (name_personnage, description_personnage, univers_select_id[0],user_id[0],))
                        conn.commit()
                        return jsonify({'message': f'Depuis un existant le Personnage {data["name"]} dans l\'univers {univers}({univers_select_id[0]}) a etait créé avec succès! {user["username"]} id : {user_id[0]}'}), 201
                    else:
                        personnage.generate_descriptionOfPersonnage(univers)
                        cursor.execute("""INSERT INTO personnages (name, description, univers_id, user_id) 
                                    VALUES (%s, %s, %s, %s)""", (data['name'], personnage.descriptionOfPersonnage, univers_select_id[0],user_id[0],)) # Insert the personnage name into the database
                        conn.commit() 
                        return jsonify({'message': f'Personnage {data["name"]} dans l\'univers {univers}({univers_select_id[0]}) créé avec succès! {user["username"]} id : {user_id[0]}'}), 201
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()

            elif request.method == 'PUT':
                data = request.json
                personnage = Personnage.from_map(data)
                personnage.generate_new_descriptionOfPersonnage(data['new_name'], univers)
                try:
                    cursor.execute("SELECT id FROM univers WHERE name = %s AND user_id = %s", (univers,user_id[0],))
                    universSelect_id = cursor.fetchone() # Fetch the first row and get the first column
                    if not universSelect_id:
                        # Aucun résultat trouvé pour cet univers
                        return jsonify({'error': 'L\'univers n\'existe pas'}), 404
                    cursor.execute("SELECT id FROM personnages WHERE name = %s AND univers_id = %s AND user_id = %s", (data['name'], universSelect_id[0],user_id[0],))# Get the personnage ID from the database
                    personnage_id = cursor.fetchone() # Fetch the first row
                    if personnage_id is not None and isinstance(personnage_id, tuple):
                        cursor.execute("UPDATE personnages SET name = %s, description = %s WHERE id = %s", (data['new_name'], personnage.new_descriptionOfPersonnage, personnage_id[0],))
                        conn.commit()
                        #personnage.generate_description()
                        return jsonify({"message": f'Nom et Description du personnage "{data["name"]}" mis à jour avec succès! Nouveau Nom: "{data["new_name"]}", Nouvelle description : "{personnage.new_descriptionOfPersonnage}"'}), 200
                    else:
                        return jsonify({"error": f'Personnage "{data["name"]}" introuvable!'}), 404
                except mysql.connector.errors.IntegrityError:
                    # Return a JSON response for IntegrityError
                    return jsonify({"error": 'Ce nom de personnage est déjà utilisé.'}), 409
                finally:
                    cursor.close()
                    conn.close()
                      
            elif request.method == 'DELETE':
                data = request.json
                personnage = Personnage.from_map(data)
                try:
                    cursor.execute("SELECT personnages.id FROM personnages INNER JOIN users on personnages.user_id = users.id WHERE name = %s AND users.id = %s", (data['name'], user_id[0]))# Get the personnage ID from the database
                    personnage_id = cursor.fetchone() # Fetch the first row
                    conn.commit()
                    if personnage_id is not None and isinstance(personnage_id, tuple):
                        personnage = Personnage.from_map({'id': personnage_id[0], 'name': data['name']})
                        cursor.execute("DELETE FROM personnages WHERE id = %s ", (personnage_id[0],))
                        conn.commit()
                        return jsonify({"message": f'Personnage "{data["name"]}" supprimé avec succès!'}), 200
                    else:
                        return jsonify({"error": f'Personnage "{data["name"]}" introuvable!'}), 404
                except mysql.connector.errors.IntegrityError as e:
                    # Return a JSON response for IntegrityError
                    return jsonify({"error": 'Erreur d\'intégrité dans la base de données.'}), 500

                finally:
                    cursor.close()
                    conn.close()
