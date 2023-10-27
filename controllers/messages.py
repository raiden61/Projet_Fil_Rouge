from flask import Flask, request, jsonify # pip install flask
import mysql.connector # pip install mysql-connector-python
from dotenv import load_dotenv  # Ajout de cette ligne
from classes.mesageses import Message
from middleware.verifToken import verify_token
from datetime import datetime
import jwt
import os
from database import get_database_cursor

load_dotenv()
secret_key = os.getenv("SECRET_KEY")


class message_controller():
    def MessageMethod(personnageConversation):
        conn, cursor = get_database_cursor()
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
                    cursor.execute("SELECT id FROM personnages WHERE name = %s", (personnageConversation,))
                    personnage_id = cursor.fetchone()
                    cursor.execute("""
            SELECT messages.id, messages.IsHuman, messages.conversation_id, messages.message, messages.sending_date, users.username, personnages.name 
            FROM messages
            INNER JOIN users ON messages.user_id = users.id
            INNER JOIN personnages ON messages.personnage_id = personnages.id
            WHERE messages.personnage_id = %s
            ORDER BY messages.sending_date
        """, (personnage_id[0],))
                    
                    rows = cursor.fetchall()
                    messages = []
                    for row in rows:
                        message_temp = Message.from_map({
                            'id': row[0],
                            'IsHuman': row[1],
                            'conversation_id': row[2],
                            'message': row[3],
                            'sending_date': row[4],
                            'users_id': row[5],
                            'personnage_id': row[6]
                        })
                        messages.append(message_temp.to_map())
                    return jsonify(messages), 200
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()
                
        elif request.method == 'POST':
            data = request.get_json()
            message = Message.from_map(data)
            cursor.execute("""
            SELECT conversations.id, users.username, personnages.name, conversations.creation_date
            FROM conversations
            INNER JOIN users ON conversations.user_id = users.id
            INNER JOIN personnages ON conversations.personnage_id = personnages.id
            WHERE conversations.user_id = %s AND personnages.name = %s
        """, (user_id[0],personnageConversation,))
            row = cursor.fetchone()
            cursor.execute("SELECT id FROM personnages WHERE name = %s", (personnageConversation,))
            personnage_id = cursor.fetchone()
            if row is None:
                return jsonify({'error': 'Cette conversation n\'existe pas'}), 404
            else:
                try:
                    if message.message == "":
                        return jsonify({'error': 'Le message ne peut pas être vide'}), 404
                    
                    ## A change pour inclure les messages de l'IA
                    is_human = request.headers.get('IsHuman')
                    if is_human == "True":
                        human = True
                    else:
                        human = False

                    # Get the current date and time
                    current_datetime = datetime.now()
                    # Format the datetime as a string with year, month, day, hour, and minute
                    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("""INSERT INTO messages (IsHuman, conversation_id, message, sending_date, user_id, personnage_id) 
                                   VALUES (%s, %s, %s, %s, %s, %s)""", (human, row[0], message.message, formatted_datetime, user_id[0], personnage_id[0]))
                    message.id = cursor.lastrowid
                    return jsonify(message.to_map()), 201
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
                finally:
                    cursor.close()
                    conn.close()


