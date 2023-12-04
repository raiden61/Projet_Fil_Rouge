from controllers.univers import Univers_Controller
from controllers.personnages import Personnages_Controller
from controllers.users import users_Controller

class ControllerFactory:
    # Méthode de création d'une instance de contrôleur
    def create_controller(self, controller_type):
        # Création d'une instance de contrôleur en fonction du type
        if controller_type == 'univers':
            return Univers_Controller()
        # Ajouter les autres types de contrôleurs ici
        elif controller_type == 'personnages':
            return Personnages_Controller()
        # Ajouter les autres types de contrôleurs ici
        elif controller_type == 'users':
            return users_Controller()
        else:
            # Type de contrôleur non pris en charge
            raise ValueError("Type de contrôleur non pris en charge")

# Utilisation de la Factory
factory = ControllerFactory()

# Exemple de création d'une instance de contrôleur
univers_controller = factory.create_controller('univers')


personnages_controller = factory.create_controller('personnages')
users_controller = factory.create_controller('users')



