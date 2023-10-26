# Description: This file contains the code for the Flask application.
from flask import Flask, request, jsonify # pip install flask
import mysql.connector # pip install mysql-connector-python
from controllers.univers import Univers_Controller
from controllers.personnages import Personnages_Controller
from controllers.users import users_Controller
from controllers.auth import auth_Controller

# Création de l'application Flask
app = Flask(__name__)
class Test(Univers_Controller):

    # Définition des routes pour l'authentification
    @app.route('/auth', methods=['POST'])
    def handle_auth():
        return auth_Controller.auth_method()

    # Définition des routes pour les users
    @app.route('/users', methods=['GET', 'POST'])
    def handle_users():
        return users_Controller.user_Method()
    
    @app.route('/users/<string:users>', methods=['GET', 'PUT'])
    def handle_usersSpecifique(users):
        return users_Controller.user_MethodSpecifique(users)


    # Définition des routes pour les univers
    @app.route('/univers', methods=['GET', 'POST'])
    def handle_univers():
        return Univers_Controller.universMethod()
    
    @app.route('/univers/<string:univers>', methods=['GET', 'PUT', 'DELETE'])
    def handle_universSpecifique(univers):
        return Univers_Controller.universMethodSpecifique(univers)
    

    # Définition des routes pour les personnages
    @app.route('/univers/<string:univers>/personnages', methods=['GET', 'POST'])
    def handle_personnages(univers):
        return Personnages_Controller.PersonnagesMethod(univers)
    
    @app.route('/univers/<string:univers>/personnages/<string:perso>', methods=['GET', 'PUT', 'DELETE'])
    def handle_personnagesSpecifique(univers, perso):
        return Personnages_Controller.PersonnagesMethodSpecifique(univers, perso)
    