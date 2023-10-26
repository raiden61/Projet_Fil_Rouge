class Univers:
    def __init__(self, name):
        self.id = None
        self.name = name
        self.description = None
        self.user_id = None

    def to_map(self):
        return {
            'id': self.id,
            'name': self.name,
            #'description': self.description
            'user_id': self.user_id,
        }

    @classmethod
    def from_map(cls, map):
        universe = cls(map.get('name', ''))
        universe.id = map.get('id')
        universe.description = map.get('description')
        universe.user_id = map.get('user_id')

        return universe

    def generate_description(self):
        # Générer avec OpenAI
        self.description = f"Description de l'univers {self.name} générée par OpenAI"
    
    
    def generate_new_description(self,new_name):
        # Générer avec OpenAI
        self.new_description = f"Description de l'univers {new_name} générée par OpenAI"
