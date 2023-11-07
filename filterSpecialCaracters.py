import re


def filter_special_characters(reponse):
    # Utiliser une expression régulière pour ne garder que les caractères alphabétiques et les espaces
    filtered_text = re.sub(r'[^a-zA-Z\s]', '', reponse.replace('\n', ''))
    return filtered_text
