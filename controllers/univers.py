# Description: This file contains the code for the Flask application.
from flask import Flask, request, jsonify # pip install flask
import mysql.connector # pip install mysql-connector-python
from dotenv import load_dotenv  # Ajout de cette ligne
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


class Univers_Controller():
    # Définition des routes pour les univers
    
    def universMethod():
        # Create a database connection and cursor
        conn, cursor = get_database_cursor()

        if request.method == 'GET':

            try:
                query = "SELECT * FROM univers"
                cursor.execute(query)
                rows = cursor.fetchall()

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

            """ # Get all the univers from the database
            cursor.execute("SELECT name, description FROM univers")
            univers = cursor.fetchall()

            universes = []
            for row in univers:
                universe_temp = Univers.from_map(row)
                universes.append(universe_temp.to_map())


            return jsonify({"univers": univers}) """

        elif request.method == 'POST':
            data = request.json
            universe = Univers.from_map(data)
            universe.generate_description()
            try:
                cursor.execute("INSERT INTO univers (name, description) VALUES (%s, %s)", (data['name'], universe.description,)) # Insert the universe name into the database
                conn.commit() # Commit the changes to the database
                return jsonify({'message': f'Univers {data["name"]} créé avec succès!'}), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                cursor.close()
                conn.close()

            """ 
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
             """
        
    def universMethodSpecifique(univers):
        # Create a database connection and cursor
        conn, cursor = get_database_cursor()
        if request.method == 'GET':
            try:
                cursor.execute("SELECT * FROM univers WHERE name = %s", (univers,))
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


            """ # Get all the univers from the database
            cursor.execute("SELECT name, description FROM univers WHERE name = %s", (univers,))
            univers = cursor.fetchall()
            return jsonify({"univers": univers}) """
        

        #faut que je rajoute dans le PUT le fait de changer la description
        elif request.method == 'PUT':
            conn, cursor = get_database_cursor()
            try:
                # Get the JSON data from the request
                data = request.json

                # Fetch the universe ID from the database using the name
                cursor.execute("SELECT * FROM univers WHERE name = %s", (univers,))
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



            
            """ #faut que je rajoute dans le PUT le fait de changer la description
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
                    return jsonify({"error": 'Cet univers n\'a pas été modifié.'}), 505 """




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








            """ cursor.execute("SELECT id FROM univers WHERE name = %s", (univers,))# Get the universe ID from the database
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
                return jsonify({"error": 'Cet univers n\'a pas été supprimé.'}), 505 """
            