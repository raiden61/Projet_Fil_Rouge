# Description: This file contains the code for the Flask application.
from flask import Flask, request, jsonify # pip install flask
import mysql.connector # pip install mysql-connector-python
from controllers.univers import Univers
from controllers.personnages import Personnages

# Création de l'application Flask
app = Flask(__name__)
class Test(Univers):

    # Définition des routes pour les univers
    @app.route('/univers', methods=['GET', 'POST'])
    def handle_univers():
        return Univers.universMethod()
    @app.route('/univers/<string:univers>', methods=['GET', 'PUT', 'DELETE'])
    def handle_universSpecifique(univers):
        return Univers.universMethodSpecifique(univers)
    
    @app.route('/univers/<string:univers>/personnages', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def handle_personnages(univers):
        return Personnages.PersonnagesMethod(univers)