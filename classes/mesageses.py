import os
import openai
from flask import Flask, request, jsonify # pip install flask
from filterSpecialCaracters import filter_special_characters
from middleware.verifToken import verify_token
import jwt

from database import db_singleton

openai.api_key = os.getenv("OPENAI_API_KEY")
my_engine = os.getenv("OPENAI_ENGINE")
secret_key = os.getenv("SECRET_KEY")

class Message:
    def __init__(self):
        self.id = None
        self.IsHuman = None
        self.conversation_id = None
        self.message = None
        self.sending_date = None
        self.users_id = None
        self.personnage_id = None

    def to_map(self):
        return {
            'id': self.id,
            'IsHuman': self.IsHuman,
            'conversation_id': self.conversation_id,
            'message': self.message,
            'sending_date': self.sending_date,
            'users_id': self.users_id,
            'personnage_id': self.personnage_id
            
        }

    @classmethod
    def from_map(cls, map):
        message = cls()
        message.id = map.get('id')
        message.IsHuman = map.get('IsHuman')
        message.conversation_id = map.get('conversation_id')
        message.message = map.get('message')
        message.sending_date = map.get('sending_date')
        message.users_id = map.get('users_id')
        message.personnage_id = map.get('personnage_id')

        return message
    
    def generate_message(self, message, personnageConversation, personnageDescription, universDescription):
        # Générer avec OpenAI
        # Utiliser OpenAI pour générer un message d'un personnage
        response = openai.Completion.create(
            engine=my_engine,  # Choisir le moteur de génération de texte
            prompt=f"In the context of a role-playing game, you will play the character {personnageConversation}. Here is the description: {personnageDescription} from the Marvel universe, here is the description: {universDescription} and you must respond to the following message:{message}",
            max_tokens=200,  # Limitez le nombre de tokens pour contrôler la longueur de la réponse
            n=1,  # Nombre de réponses à générer
            stop=None  # Vous pouvez spécifier des mots pour arrêter la génération
        )
        reponse = response.choices[0].text.strip()

        filtered_text = filter_special_characters(reponse)
        
        self.response_message = filtered_text
        return self.response_message

