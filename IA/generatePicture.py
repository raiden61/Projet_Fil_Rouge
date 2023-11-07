import requests
import os
import openai
from filterSpecialCaracters import filter_special_characters
from flask import jsonify

my_engine = os.getenv("OPENAI_ENGINE")
ia_picture_key = os.getenv("PICTURE_API_KEY")


def generate_picture_univers(self, name, description, isDescription, univers):
        # Get the picture from the IA
        if isDescription == 1:
            prompt = f"Here is the description of the {name} universe: {description} \n\n Write a prompt to generate an image using the Text-to-image artificial intelligence named StableDiffusion to represent the {name} universe. The prompt should be in English and not exceed 300 characters."
        elif isDescription == 2:
            prompt = f"Voici la description du personnage {name}: {description} \n\n Ecris moi un prompt pour générer une image avec l'intelligence artificielle Text-to-image nommé StableDiffusion afin de représenter le personnage {name} issu de l'univers {univers}. Le prompt doit etre en anglais et ne pas dépasser 300 caractères."
        else:
            return jsonify({'error': 'isDescription invalide'}), 404
        response_pictures = openai.Completion.create(
            engine=my_engine,  # Choisir le moteur de génération de texte
            prompt=prompt,
            max_tokens=200,  # Limitez le nombre de tokens pour contrôler la longueur de la réponse
            n=1,  # Nombre de réponses à générer
            stop=None  # Vous pouvez spécifier des mots pour arrêter la génération
        )
        response_text = response_pictures.choices[0].text.strip()

        filtered_text_pictures = filter_special_characters(response_text)

        prompt_text = filtered_text_pictures
        # Get the picture from the IA
        r = requests.post('https://clipdrop-api.co/text-to-image/v1',
        files = {
            'prompt': (None, prompt_text , 'text/plain')
        },
        headers = { 'x-api-key': ia_picture_key}
        )
        if (r.ok):

            if isDescription == 1:
                # r.content contains the bytes of the returned image
                with open(f'IA/Pictures/univers/{name}.jpg', 'wb') as f:
                    f.write(r.content)
            elif isDescription == 2:
                # r.content contains the bytes of the returned image
                with open(f'IA/Pictures/personnages/{name}.jpg', 'wb') as f:
                    f.write(r.content)
            else:
                return jsonify({'error': 'isDescription invalide'}), 404

        else:
            r.raise_for_status()