import models


class UserProfile:
    def __init__(self, user_id, tag_id, first_name, last_name, email, role_id, pic_url):
        self.user_id = user_id
        self.tag_id = tag_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role_id = role_id
        self.role_title = 'Profesor' if role_id == 1 else 'Student'
        self.pic_url = pic_url


class SessionView:
    def __init__(self, session_id, key_id, room_repr, user_id, first_name, last_name, started_on, closed_on, ):
        self.id = session_id
        self.key_id = key_id
        self.room_repr = room_repr
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.started_on = started_on
        self.closed_on = closed_on
