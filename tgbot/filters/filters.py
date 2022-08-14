from backend.tg_backend.models import Organizers, Level

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


def is_organizer(id_p):
    for member in Organizers.objects.all():
        if member.id == id_p:
            return True
    return False

def is_admin(id_p):
    if (is_organizer(id_p)):
        if Level.objects.get(id = id_p).level == 'developer':
            return True
    return False