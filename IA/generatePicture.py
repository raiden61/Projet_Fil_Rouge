import requests
import os
import openai
from filterSpecialCaracters import filter_special_characters

my_engine = os.getenv("OPENAI_ENGINE")
ia_picture_key = os.getenv("PICTURE_API_KEY")


def generate_picture_univers(self, name, description):
        # Get the picture from the IA
        response_pictures = openai.Completion.create(
            engine= my_engine, # Choisir le moteur de génération de texte
            prompt=f"Generate an English prompt for Stable Diffusion, with a maximum length of 300 characters, to create a background image for the {name} universe, the description of which is as follows: {description}", 
            max_tokens=200,  # Limitez le nombre de tokens pour contrôler la longueur de la réponse
            n=1,  # Nombre de réponses à générer
            stop=None  # Vous pouvez spécifier des mots pour arrêter la génération
        )
        self.response_pictures = response_pictures.choices[0].text.strip()

        filtered_text_pictures = filter_special_characters(self.response_pictures)
        
        prompt_text = filtered_text_pictures
        # Get the picture from the IA
        r = requests.post('https://clipdrop-api.co/text-to-image/v1',
        files = {
            'prompt': (None, prompt_text , 'text/plain')
        },
        headers = { 'x-api-key': ia_picture_key}
        )
        if (r.ok):
            # r.content contains the bytes of the returned image
            with open(f'IA/Pictures/univers/{self.name}.jpg', 'wb') as f:
                f.write(r.content)

        else:
            r.raise_for_status()