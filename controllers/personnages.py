# Description: This file contains the code for the Flask application.
from flask import Flask, request, jsonify # pip install flask
import mysql.connector # pip install mysql-connector-python
from controllers.univers import Univers_Controller
from dotenv import load_dotenv  # Ajout de cette ligne
from classes.personnageses import Personnage
from classes.universes import Univers
import os

load_dotenv()

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


class Personnages_Controller(Univers_Controller):
    # Définition des routes pour les personnages
    def PersonnagesMethod(univers):
        # Create a database connection and cursor
        conn, cursor = get_database_cursor()

        if request.method == 'GET':

            try:
                # Get the universe ID from the database
                cursor.execute("SELECT id FROM univers WHERE name = %s", (univers,))
                univers_select_id = cursor.fetchone()

                if not univers_select_id:
                    # Aucun résultat trouvé pour cet univers
                    return jsonify({'error': 'L\'univers n\'existe pas'}), 404

                # Get all the personnages from the database using JOIN
                cursor.execute("SELECT personnages.id, personnages.name, personnages.description, personnages.univers_id, univers.name as univers_name FROM personnages INNER JOIN univers ON personnages.univers_id = univers.id WHERE univers.id = %s", (univers_select_id[0],))
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

            """ # Get all the personnages from the database
            cursor.execute("SELECT id FROM univers WHERE name = %s", (univers,))# Get the universe ID from the database
            universSelect_id = cursor.fetchone() # Fetch the first row
            cursor.execute("SELECT univers.name, personnages.name, personnages.description FROM personnages INNER JOIN univers on personnages.univers_id = univers.id WHERE univers.id = %s", (universSelect_id)) # Get all the personnages from the database
            personnages = cursor.fetchall()
            return jsonify({"personnages": personnages}) """
        
        elif request.method == 'POST':

            data = request.json
            personnage = Personnage.from_map(data)
            personnage.generate_description()
            try: 
                # Get the universe ID from the database
                cursor.execute("SELECT id FROM univers WHERE name = %s", (univers,))
                univers_select_id = cursor.fetchone()
                if not univers_select_id:
                    # Aucun résultat trouvé pour cet univers
                    return jsonify({'error': 'L\'univers n\'existe pas'}), 404
                cursor.execute("INSERT INTO personnages (name, description, univers_id) VALUES (%s, %s, %s)", (data['name'], personnage.description, univers_select_id[0],)) # Insert the personnage name into the database
                conn.commit() # Commit the changes to the database
                return jsonify({'message': f'Personnage {data["name"]} dans l\'univers {univers}({univers_select_id[0]}) créé avec succès!'}), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                cursor.close()
                conn.close()


            """ # Get the JSON data from the request
            data = request.json
            cursor.execute("SELECT id FROM univers WHERE name = %s", (univers,))
            universSelect_id = cursor.fetchone()[0] # Fetch the first row and get the first column

            # Ensure that the 'name' key is present in the JSON data
            if 'name' in data:
                personnage_name = data['name']
                personnage_description = data['description']

                try: 
                    # Insert the personnage name into the database
                    cursor.execute("INSERT INTO personnages (name, description, univers_id) VALUES (%s, %s, %s)", (personnage_name, personnage_description, universSelect_id)) # Insert the personnage name into the database
                    conn.commit()

                    # Close the cursor and connection
                    cursor.close()
                    conn.close()

                    return jsonify({"message": f'Personnage "{personnage_name}" créé avec succès! dans l\"univers {univers} avec la description suivante "{personnage_description}"'}), 1
                except mysql.connector.errors.IntegrityError:
                    # Return a JSON response for IntegrityError
                    return jsonify({"error": 'Ce nom de personnage est déjà utilisé.'}), 409
            else:
                return 'Erreur: Veuillez fournir le nom du personnage dans les données JSON du POST request.', 400 """
            
        #faut que je fasse un PUT pour modifier la description d'un personnage
        elif request.method == 'PUT':
            data = request.json
            personnage = Personnage.from_map(data)
            personnage.generate_new_description(data['new_name'])
            try:
                
                cursor.execute("SELECT id FROM univers WHERE name = %s", (univers,))
                universSelect_id = cursor.fetchone()[0] # Fetch the first row and get the first column
                if not universSelect_id:
                    # Aucun résultat trouvé pour cet univers
                    return jsonify({'error': 'L\'univers n\'existe pas'}), 404
                cursor.execute("SELECT id FROM personnages WHERE name = %s AND univers_id = %s", (data['name'], universSelect_id,))# Get the personnage ID from the database
                personnage_id = cursor.fetchone() # Fetch the first row
                if personnage_id is not None and isinstance(personnage_id, tuple):
                    cursor.execute("UPDATE personnages SET name = %s, description = %s WHERE id = %s", (data['new_name'], personnage.new_description, personnage_id[0],))
                    conn.commit()
                    personnage.generate_description()
                    return jsonify({"message": f'Nom et Description du personnage "{data["name"]}" mis à jour avec succès! Nouveau Nom: "{data["new_name"]}", Nouvelle description : "{personnage.new_description}"'}), 200
                else:
                    return jsonify({"error": f'Personnage "{data["name"]}" introuvable!'}), 404
            except mysql.connector.errors.IntegrityError:
                # Return a JSON response for IntegrityError
                return jsonify({"error": 'Ce nom de personnage est déjà utilisé.'}), 409
            finally:
                cursor.close()
                conn.close()


            """ # Get the JSON data from the request
            data = request.json
            cursor.execute("SELECT id FROM univers WHERE name = %s", (univers,))
            universSelect_id = cursor.fetchone()[0] # Fetch the first row and get the first column
            try:
                cursor.execute("SELECT id FROM personnages WHERE name = %s AND univers_id = %s", (data['name'], universSelect_id,))# Get the personnage ID from the database
                personnage_id = cursor.fetchone() # Fetch the first row
                conn.commit()
                if personnage_id is not None and isinstance(personnage_id, tuple):
                    cursor.execute("UPDATE personnages SET name = %s WHERE id = %s", (data['new_name'], personnage_id[0],))
                    conn.commit()
                    return jsonify({"message": f'Personnage "{data["name"]}" mis à jour avec succès! Nouveau nom : "{data["new_name"]}"'}), 200
                else:
                    return jsonify({"error": f'Personnage "{data["name"]}" introuvable!'}), 404
            except mysql.connector.errors.IntegrityError:
                # Return a JSON response for IntegrityError
                return jsonify({"error": 'Ce nom de personnage est déjà utilisé.'}), 409 """
        

        elif request.method == 'DELETE':
            data = request.json
            try:
                cursor.execute("SELECT id FROM personnages WHERE name = %s", (data['name'],))# Get the personnage ID from the database
                personnage_id = cursor.fetchone() # Fetch the first row
                conn.commit()
                if personnage_id is not None and isinstance(personnage_id, tuple):
                    personnage = Personnage.from_map(data)
                    cursor.execute("DELETE FROM personnages WHERE id = %s", (personnage_id[0],))
                    conn.commit()
                    return jsonify({"message": f'Personnage "{data["name"]}" supprimé avec succès!'}), 200
                else:
                    return jsonify({"error": f'Personnage "{data["name"]}" introuvable!'}), 404
            except mysql.connector.errors.IntegrityError:
                # Return a JSON response for IntegrityError
                return jsonify({"error": 'Ce nom de personnage est déjà utilisé.'}), 409
            finally:
                cursor.close()
                conn.close()
                
                
            

            """ # Get the JSON data from the request
            data = request.json
            cursor.execute("SELECT id FROM univers WHERE name = %s", (univers,))
            universSelect_id = cursor.fetchone()[0] # Fetch the first row and get the first column
            try:
                cursor.execute("SELECT id FROM personnages WHERE name = %s AND univers_id = %s", (data['name'], universSelect_id,))# Get the personnage ID from the database
                personnage_id = cursor.fetchone() # Fetch the first row
                conn.commit()
                if personnage_id is not None and isinstance(personnage_id, tuple):
                    cursor.execute("DELETE FROM personnages WHERE id = %s", (personnage_id[0],))
                    conn.commit()
                    return jsonify({"message": f'Personnage "{data["name"]}" supprimé avec succès!'}), 200
                else:
                    return jsonify({"error": f'Personnage "{data["name"]}" introuvable!'}), 404
            except mysql.connector.errors.IntegrityError:
                # Return a JSON response for IntegrityError
                return jsonify({"error": 'Ce nom de personnage est déjà utilisé.'}), 409 """
            