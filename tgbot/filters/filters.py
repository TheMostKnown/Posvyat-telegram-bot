class User:
    """The object is the user.
    chat_id - user's tg chat id
    username - user's tg tag
    """

    def __init__(self,
                 chat_id=0,
                 username=''
                 ):
        self.chat_id = chat_id
        self.username = username

    def __repr__(self):
        return f'<User(chat_id="{self.chat_id}", username="{self.username}")>'

    def __eq__(self, other):
        return type(other) == User and self.chat_id == other.chat_id and self.username == other.username