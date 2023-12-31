class Users:
    def __init__(self, name, password, email, first_name, last_name):
        self.id = None
        self.username = name
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def to_map(self):
        return {
            'id': self.id,
            'username': self.username,
            #'password': self.password,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    @classmethod
    def from_map(cls, map):
        user = cls()
        user.id = map.get('id')
        user.username = map.get('username')
        user.password = map.get('password')
        user.email = map.get('email')
        user.first_name = map.get('first_name')
        user.last_name = map.get('last_name')

        return user
