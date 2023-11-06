import os
import openai
import re

openai.api_key = os.getenv("OPENAI_API_KEY")
my_engine = os.getenv("OPENAI_ENGINE")

class Univers:
    def __init__(self, name):
        self.id = None
        self.name = name
        self.description = None
        self.user_id = None

    def to_map(self):
        return {
            'id': self.id,
            'name': self.name,
            #'description': self.description
            'user_id': self.user_id,
        }

    @classmethod
    def from_map(cls, map):
        universe = cls(map.get('name', ''))
        universe.id = map.get('id')
        universe.description = map.get('description')
        universe.user_id = map.get('user_id')

        return universe

    def generate_description(self):
        # Générer avec OpenAI
        # Utiliser OpenAI pour générer une description d'un univers
        response = openai.Completion.create(
            engine= my_engine, # Choisir le moteur de génération de texte
            prompt=f"Give me an English description of the {self.name} universe.", 
            max_tokens=150,  # Limitez le nombre de tokens pour contrôler la longueur de la réponse
            n=1,  # Nombre de réponses à générer
            stop=None  # Vous pouvez spécifier des mots pour arrêter la génération
        )
        self.reponse = response.choices[0].text.strip()

        filtered_text = self.filter_special_characters(self.reponse)
        
        self.description = filtered_text

        return self.description

        #self.description = f"Description de l'univers {self.name} générée par OpenAI"

    def generate_new_description(self,new_name):
        # Générer avec OpenAI
        # Utiliser OpenAI pour générer une description d'un univers
        response = openai.Completion.create(
            engine= my_engine, # Choisir le moteur de génération de texte
            prompt=f"Give me an English description of the {new_name} universe.", 
            max_tokens=150,  # Limitez le nombre de tokens pour contrôler la longueur de la réponse
            n=1,  # Nombre de réponses à générer
            stop=None  # Vous pouvez spécifier des mots pour arrêter la génération
        )
        self.reponse = response.choices[0].text.strip()

        filtered_text = self.filter_special_characters(self.reponse)
        
        self.new_description = filtered_text
        
        return self.new_description
    
        #self.new_description = f"Description de l'univers {new_name} générée par OpenAI"

    def filter_special_characters(self, text):
        # Utiliser une expression régulière pour ne garder que les caractères alphabétiques et les espaces
        filtered_text = re.sub(r'[^a-zA-Z\s]', '', text)
        return filtered_text
