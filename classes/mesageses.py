class Message:
    def __init__(self):
        self.id = None
        self.IsHuman = None
        self.conversation_id = None
        self.message = None
        self.sending_date = None
        self.users_id = None
        self.personnage_id = None

    def to_map(self):
        return {
            'id': self.id,
            'IsHuman': self.IsHuman,
            'conversation_id': self.conversation_id,
            'message': self.message,
            'sending_date': self.sending_date,
            'users_id': self.users_id,
            'personnage_id': self.personnage_id
            
        }

    @classmethod
    def from_map(cls, map):
        message = cls()
        message.id = map.get('id')
        message.IsHuman = map.get('IsHuman')
        message.conversation_id = map.get('conversation_id')
        message.message = map.get('message')
        message.sending_date = map.get('sending_date')
        message.users_id = map.get('users_id')
        message.personnage_id = map.get('personnage_id')

        return message
