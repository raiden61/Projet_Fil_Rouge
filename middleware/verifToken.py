from flask import Flask, request, jsonify # pip install flask
import jwt
import bcrypt
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("SECRET_KEY")


def verify_token(token):

    try:
        decoded_data = jwt.decode(token, secret_key, algorithms=["HS256"])

        if datetime.utcnow() > datetime.utcfromtimestamp(decoded_data["exp"]):
            raise jwt.ExpiredSignatureError("Le token a expiré")
        
        # Le token est valide
        return decoded_data
    
    except jwt.ExpiredSignatureError:
        print("Le token a expiré.")
        return 505
    
    except jwt.InvalidTokenError:
        print("Token invalide.")
        return 404
        
        