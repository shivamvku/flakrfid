class Key:
    def __init__(self, key_id, tag_id, room_id, block_name, sector_name, floor, room_repr):
        self.id = key_id
        self.tag_id = tag_id
        self.room_id = room_id
        self.block_name = block_name
        self.sector_name = sector_name
        self.floor = floor
        self.room_repr = room_repr


class User:
    def __init__(self, user_id, tag_id, first_name, last_name, email, role_id, pic_id):
        self.id = user_id
        self.tag_id = tag_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role_id = role_id
        self.pic_id = pic_id


class Session:
    def __init__(self, session_id, user_id, key_id, started_on, closed_on):
        self.id = session_id
        self.user_id = user_id
        self.key_id = key_id
        self.started_on = started_on
        self.closed_on = closed_on
