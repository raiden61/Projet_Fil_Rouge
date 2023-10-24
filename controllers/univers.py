# Description: This file contains the code for the Flask application.
from flask import Flask, request, jsonify # pip install flask
import mysql.connector # pip install mysql-connector-python
from dotenv import load_dotenv  # Ajout de cette ligne
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


class Univers():
    # Définition des routes pour les univers
    
    def universMethod():
        # Create a database connection and cursor
        conn, cursor = get_database_cursor()

        if request.method == 'GET':
            # Get all the univers from the database
            cursor.execute("SELECT name, description FROM univers")
            univers = cursor.fetchall()
            return jsonify({"univers": univers})

        elif request.method == 'POST':
            # Get the JSON data from the request
            data = request.json

            # Ensure that the 'name' key is present in the JSON data
            if 'name' in data:
                universe_name = data['name']
                universe_description = data['description']

                try: 
                    # Insert the universe name into the database
                    cursor.execute("INSERT INTO univers (name, description) VALUES (%s, %s)", (universe_name, universe_description,)) # Insert the universe name into the database
                    conn.commit()

                    # Close the cursor and connection
                    cursor.close()
                    conn.close()

                    return jsonify({"message": f'Univers "{universe_name}" créé avec succès! avec la description suivante "{universe_description}"'}), 1
                except mysql.connector.errors.IntegrityError:
                    # Return a JSON response for IntegrityError
                    return jsonify({"error": 'Ce nom d\'univers est déjà utilisé.'}), 409
            else:
                return 'Erreur: Veuillez fournir le nom de l\'univers dans les données JSON du POST request.', 400
            
        
    def universMethodSpecifique(univers):
        # Create a database connection and cursor
        conn, cursor = get_database_cursor()
        if request.method == 'GET':
            # Get all the univers from the database
            cursor.execute("SELECT name, description FROM univers WHERE name = %s", (univers,))
            univers = cursor.fetchall()
            return jsonify({"univers": univers})
        
        #faut que je rajoute dans le PUT le fait de changer la description
        elif request.method == 'PUT':
            # Get the JSON data from the request
            data = request.json
            cursor.execute("SELECT id FROM univers WHERE name = %s", (univers,))# Get the universe ID from the database
            univers_id = cursor.fetchone() # Fetch the first row
            conn.commit()
            if univers_id is not None and isinstance(univers_id, tuple):
                cursor.execute("UPDATE univers SET name = %s WHERE id = %s", (data['new_name'] , univers_id[0],))
                conn.commit()
                return jsonify({"message": f"Modification de l\'univers {univers} en {data['new_name']}"}), 200 # Return a JSON response for success
            elif univers_id is None:
                return jsonify({"error": 'Cet univers n\'existe pas.'}), 404
            else:
                return jsonify({"error": 'Cet univers n\'a pas été modifié.'}), 505
                
        elif request.method == 'DELETE':
            cursor.execute("SELECT id FROM univers WHERE name = %s", (univers,))# Get the universe ID from the database
            univers_id = cursor.fetchone() # Fetch the first row   
            conn.commit()
            if univers_id is not None and isinstance(univers_id, tuple):
                cursor.execute("DELETE FROM personnages WHERE univers_id = %s", (univers_id[0],)) # Delete all characters associated with the universe
                conn.commit()
                cursor.execute("DELETE FROM univers WHERE id = %s", (univers_id[0],))# Delete the universe from the database
                conn.commit()
                return jsonify({"message": f"Suppression de l\'univers {univers} ainsi que les personnages qui contienne cette {univers}"}), 200 # Return a JSON response for success
            elif univers_id is None:
                return jsonify({"error": 'Cet univers n\'existe pas.'}), 404
            else:
                return jsonify({"error": 'Cet univers n\'a pas été supprimé.'}), 505
        
                        
















            
""" elif request.method == 'PUT':
            # Get the JSON data from the request
            data = request.json
            try:
                cursor.execute("SELECT id FROM univers WHERE name = %s", (data['name'],))# Get the universe ID from the database
                univers_id = cursor.fetchone() # Fetch the first row
                conn.commit()
                if univers_id is not None and isinstance(univers_id, tuple):
                    cursor.execute("UPDATE univers SET name = %s WHERE id = %s", (data['new_name'], univers_id[0],))# Update the universe name in the database
                    conn.commit()
                    return jsonify({"message": f"Modification de l\'univers {data['name']} en {data['new_name']}"}), 200 # Return a JSON response for success
                elif univers_id is None:
                    return jsonify({"error": 'Cet univers n\'existe pas.'}), 404 # Return a JSON response for error
                else:
                    return jsonify({"error": 'Cet univers n\'a pas été modifié.'}), 505 # Return a JSON response for error
            except mysql.connector.errors.IntegrityError:
                # Return a JSON response for IntegrityError
                return jsonify({"error": 'Ce nom d\'univers est déjà utilisé.'}), 409
        
        elif request.method == 'DELETE':
            # Get the JSON data from the request
            data = request.json
            try:
                cursor.execute("SELECT id FROM univers WHERE name = %s", (data['name'],))# Get the universe ID from the database
                univers_id = cursor.fetchone() # Fetch the first row
                conn.commit()
                if univers_id is not None and isinstance(univers_id, tuple):
                    cursor.execute("DELETE FROM univers WHERE id = %s", (univers_id[0],))# Delete the universe from the database
                    conn.commit()
                    return jsonify({"message": f"Suppression de l\'univers {data['name']}"}), 200 # Return a JSON response for success
                elif univers_id is None:
                    return jsonify({"error": 'Cet univers n\'existe pas.'}), 404 # Return a JSON response for error
                else:
                    return jsonify({"error": 'Cet univers n\'a pas été supprimé.'}), 505 # Return a JSON response for error
            except mysql.connector.errors.IntegrityError:
                # Return a JSON response for IntegrityError
                return jsonify({"error": 'Ce nom d\'univers est déjà utilisé.'}), 409 # Return a JSON response for error
 """