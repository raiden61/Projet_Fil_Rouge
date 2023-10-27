class Conversations:
    def __init__(self):
        self.id = None
        self.username = None
        self.personnage_name = None
        self.creation_date = None

    def to_map(self):
        return {
            'id': self.id,
            'username': self.username,
            'personnage_name': self.personnage_name,
            'creation_date': self.creation_date
        }

    @classmethod
    def from_map(cls, map):
        conversation = cls()
        conversation.id = map.get('id')
        conversation.username = map.get('username')
        conversation.personnage_name = map.get('personnage_name')
        conversation.creation_date = map.get('creation_date')

        return conversation
