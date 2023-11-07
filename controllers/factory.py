from controllers.univers import Univers_Controller
from controllers.personnages import Personnages_Controller
from controllers.users import users_Controller

class ControllerFactory:
    def create_controller(self, controller_type):
        if controller_type == 'univers':
            return Univers_Controller()
        elif controller_type == 'personnages':
            return Personnages_Controller()
        elif controller_type == 'users':
            return users_Controller()
        else:
            raise ValueError("Type de contrôleur non pris en charge")

# Utilisation de la Factory
factory = ControllerFactory()

# Exemple de création d'une instance de contrôleur
univers_controller = factory.create_controller('univers')
