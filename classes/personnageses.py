class Personnage:
    def __init__(self, name):
        self.id = None
        self.name = name
        self.description = None
        self.univers_id = None
        self.user_id = None

    def to_map(self):
        return {
            'id': self.id,
            'name': self.name,
            #'description': self.description
            'univers_id': self.univers_id,
            'user_id': self.user_id,
        }

    @classmethod
    def from_map(cls, map):
        personnage = cls(map.get('name', ''))
        personnage.id = map.get('id')
        personnage.description = map.get('description')
        personnage.univers_id = map.get('univers_id')
        personnage.user_id = map.get('user_id')

        return personnage

    def generate_description(self):
        # Générer avec OpenAI
        self.description = f"Description du personnage {self.name} générée par OpenAI"

    def generate_new_description(self,new_name):
        # Générer avec OpenAI
        self.new_description = f"Description du personnage {new_name} générée par OpenAI"
