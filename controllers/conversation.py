from flask import Flask, request, jsonify # pip install flask
import mysql.connector # pip install mysql-connector-python
from dotenv import load_dotenv  # Ajout de cette ligne
from classes.conversationses import Conversations
from middleware.verifToken import verify_token
from datetime import datetime
import jwt
import os
from database import get_database_cursor
from classes.personnageses import Personnage
from classes.userses import Users

load_dotenv()
secret_key = os.getenv("SECRET_KEY")


class Conversation_Controller():
    def ConversationMethod():
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

            if request.method == "GET":
                try: 

                    cursor.execute("""
            SELECT conversations.id, users.username, personnages.name, conversations.creation_date
            FROM conversations
            INNER JOIN users ON conversations.user_id = users.id
            INNER JOIN personnages ON conversations.personnage_id = personnages.id
            WHERE conversations.user_id = %s
        """, (user_id[0],))

                    rows = cursor.fetchall()
                    conversations = []

                    for row in rows:
                        conversation_temp = Conversations.from_map({
                            'id': row[0],
                            'username': row[1],
                            'personnage_name': row[2],
                            'creation_date': row[3]
                        })
                        conversations.append(conversation_temp.to_map())

                    return jsonify(conversations), 200

                except Exception as e:
                    return jsonify({'error': str(e)}), 500

                finally:
                    cursor.close()
                    conn.close()

            elif request.method == "POST":
                data = request.json
                conversation = Conversations.from_map(data)
                try:
                    cursor.execute("SELECT id FROM personnages WHERE name = %s AND user_id = %s", (data["nameOfPerso"], user_id[0],))
                    personnage_select_id = cursor.fetchone()
                    if not personnage_select_id:
                        # Aucun résultat trouvé pour cet univers
                        return jsonify({'error': 'Le personnage n\'existe pas.'}), 404
                    cursor.execute("SELECT * FROM conversations WHERE user_id = %s AND personnage_id = %s", (user_id[0], personnage_select_id[0],))
                    row = cursor.fetchone()
                    if row is not None:
                        return jsonify({'error': 'Cette conversation existe déjà'}), 403
                    else:
                        # Get the current date and time
                        current_datetime = datetime.now()
                        # Format the datetime as a string with year, month, day, hour, and minute
                        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
                        cursor.execute("""INSERT INTO conversations (user_id, personnage_id, creation_date) 
                                       VALUES (%s, %s, %s)""", (user_id[0], personnage_select_id[0], formatted_datetime,))
                        conn.commit()
                        return jsonify({'success': f'Conversation entre {user["username"]} et {data["nameOfPerso"]} créée '}), 200
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()

    def ConversationMethodSpecifique(personnageConversation):
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

            if request.method == "GET":
                try:
                    cursor.execute("""
            SELECT conversations.id, users.username, personnages.name, conversations.creation_date
            FROM conversations
            INNER JOIN users ON conversations.user_id = users.id
            INNER JOIN personnages ON conversations.personnage_id = personnages.id
            WHERE conversations.user_id = %s AND personnages.name = %s
        """, (user_id[0],personnageConversation,))
                    row = cursor.fetchone()
                    if row is None:
                        return jsonify({'error': 'Cette conversation n\'existe pas'}), 404
                    else:
                        conversation = Conversations.from_map({
                            'id': row[0],
                            'username': row[1],
                            'personnage_name': row[2],
                            'creation_date': row[3]
                        })
                        return jsonify(conversation.to_map()), 200
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()

            elif request.method == "DELETE":
                try:
                    cursor.execute("""
            SELECT conversations.id, users.username, personnages.name, conversations.creation_date
            FROM conversations
            INNER JOIN users ON conversations.user_id = users.id
            INNER JOIN personnages ON conversations.personnage_id = personnages.id
            WHERE conversations.user_id = %s AND personnages.name = %s
        """, (user_id[0],personnageConversation,))
                    row = cursor.fetchone()
                    if row is None:
                        return jsonify({'error': 'Cette conversation n\'existe pas'}), 404
                    
                    else:
                        cursor.execute("DELETE FROM conversations WHERE conversations.id = %s", (row[0],))
                        conn.commit()
                        return jsonify({'success': f'Conversation entre {user["username"]} et {personnageConversation} supprimée '}), 200
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()