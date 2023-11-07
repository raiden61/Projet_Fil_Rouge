# Description: This file contains the code for the Flask application.
from flask import Flask, request, jsonify # pip install flask
from controllers.personnages import Personnages_Controller
from controllers.users import users_Controller
from controllers.auth import auth_Controller
from controllers.conversation import Conversation_Controller
from controllers.messages import message_controller

from controllers.factory import ControllerFactory

# Utilisation de la Factory
controller_factory = ControllerFactory()

# Création de l'application Flask
app = Flask(__name__)

class Test():

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
        #return Univers_Controller.universMethod()
        univers_controller = controller_factory.create_controller('univers')
        return univers_controller.universMethod()
    
    @app.route('/univers/<string:univers>', methods=['GET', 'PUT', 'DELETE'])
    def handle_universSpecifique(univers):
        #return Univers_Controller.universMethodSpecifique(univers)
        univers_controller = controller_factory.create_controller('univers')
        return univers_controller.universMethodSpecifique(univers)
    

    # Définition des routes pour les personnages
    @app.route('/univers/<string:univers>/personnages', methods=['GET', 'POST', 'PUT',  'DELETE'])
    def handle_personnages(univers):
        #return Personnages_Controller.PersonnagesMethod(univers)
        personnages_controller = controller_factory.create_controller('personnages')
        return personnages_controller.PersonnagesMethod(univers)
        
    

    # Définition des routes pour les conversations
    @app.route('/conversation', methods=['GET', 'POST'])
    def handle_conversation():
        return Conversation_Controller.ConversationMethod()
    
    @app.route('/conversation/<string:personnageConversation>', methods=['GET', 'DELETE'])
    def handle_conversationSpecifique(personnageConversation):
        return Conversation_Controller.ConversationMethodSpecifique(personnageConversation)
    

    # Définition des routes pour les messages
    @app.route('/conversation/<string:personnageConversation>/messages', methods=['GET', 'POST'])
    def handle_messages(personnageConversation):
        return message_controller.MessageMethod(personnageConversation)
    
    @app.route('/conversation/<string:personnageConversation>', methods=['PUT'])
    def handle_messagesSpecifique(personnageConversation):
        return message_controller.MessageMethodSpecifique(personnageConversation)

