from flask import Flask, request, jsonify # pip install flask
from dotenv import load_dotenv  # Ajout de cette ligne
from classes.mesageses import Message
from middleware.verifToken import verify_token
from datetime import datetime
import jwt
import os
from database import db_singleton

load_dotenv()
secret_key = os.getenv("SECRET_KEY")


class message_controller():
    def MessageMethod(personnageConversation):
        # Create a database connection and cursor
        conn, cursor= db_singleton.get_cursor()

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
            conversationID = row[0]
            cursor.execute("SELECT id FROM personnages WHERE name = %s", (personnageConversation,))
            personnage_id = cursor.fetchone()
            if row is None:
                return jsonify({'error': 'Cette conversation n\'existe pas'}), 404
            try:
                if message.message == "":
                    return jsonify({'error': 'Le message ne peut pas être vide'}), 404

                # Obtenir la date et l'heure actuelles
                current_datetime = datetime.now()
                # Formater la date et l'heure en tant que chaîne avec année, mois, jour, heure et minute
                formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                
                cursor.execute("""INSERT INTO messages (IsHuman, conversation_id, message, sending_date, user_id, personnage_id) 
                                VALUES (%s, %s, %s, %s, %s, %s)""", (True, conversationID, message.message, formatted_datetime, user_id[0], personnage_id[0]))
                message.id = cursor.lastrowid
                conn.commit()

               # Générer avec OpenAI
                cursor.execute("""SELECT p.univers_id
                            FROM personnages p
                            INNER JOIN users us on p.user_id = us.id
                            WHERE p.name = %s AND us.id = %s
                       """, (personnageConversation, user_id))
                univers_id = cursor.fetchall()
                if univers_id is None:
                    return jsonify({'error': 'Le personnage n\'existe pas'}), 404
                else:
                
                    if univers_id:
                        univers_id = univers_id[0]

                    cursor.execute("""SELECT p.name, p.description, u.name, u.description, us.id
                                        FROM personnages p
                                        INNER JOIN	univers u on p.univers_id = u.id
                                        INNER JOIN users us on u.user_id = us.id
                                        WHERE us.id = %s AND p.name = %s AND u.id = %s
                                        """, (user_id, personnageConversation, univers_id))
                    row = cursor.fetchall()
                    if row is None:
                        return jsonify({'error': 'Le personnage n\'existe pas'}), 404
                    else:
                        for row in row:
                            personnageDescription = row[1]
                            universDescription = row[3]

                Message.generate_message(message, personnageConversation, personnageDescription, universDescription)
                cursor.execute("""INSERT INTO messages (IsHuman, conversation_id, message, sending_date, user_id, personnage_id)
                                VALUES (%s, %s, %s, %s, %s, %s)""", (False, conversationID, Message.response_message, formatted_datetime, user_id[0], personnage_id[0]))
                conn.commit()
                message.id = cursor.lastrowid
                return jsonify({'success': f'Message envoyé message de la personne {message.message} reponse de l\'ia {Message.response_message}'}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                cursor.close()
                conn.close()


    def MessageMethodSpecifique(personnageConversation):
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
            cursor.close()
            conn.close()



        if request.method == 'PUT':
            data = request.get_json()
            message = Message.from_map(data)
            # à faire


