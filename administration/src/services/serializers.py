import json
import datetime
import base64
from ..models.models import Session, User, Key


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if type(o) is datetime.datetime:
            return str(o)
        # code below for blobs
        # elif type(o) is str and len(o) > 100:
        #     return base64.b64decode(o)
        return o.__dict__


class JSONSerializer(object):
    @staticmethod
    def json_deserialize(data_string):
        return dict(json.loads(data_string))

    @staticmethod
    def key_instance_deserialize(parsed_dict):
        key_repr = parsed_dict['room_repr'] if 'room_repr' in parsed_dict and parsed_dict['room_repr'] is not None else \
        parsed_dict['block_name'] + parsed_dict['sector_name'] + parsed_dict['floor'] + '-' + parsed_dict['room_id']
        return Key(key_id=parsed_dict['id'],
                   tag_id=parsed_dict['tag_id'],
                   room_id=parsed_dict['room_id'],
                   block_name=parsed_dict['block_name'],
                   sector_name=parsed_dict['sector_name'],
                   floor=parsed_dict['floor'],
                   room_repr=key_repr)

    @staticmethod
    def key_instance_serialize(key_instance):
        return json.dumps(key_instance, cls=CustomJSONEncoder)

    @staticmethod
    def key_instances_serialize(key_list):
        return [JSONSerializer.key_instance_serialize(key) for key in key_list]

    @staticmethod
    def session_instance_deserialize(parsed_dict):
        return Session(session_id=parsed_dict['id'],
                       user_id=parsed_dict['user_id'],
                       key_id=parsed_dict['key_id'],
                       started_on=parsed_dict['started_on'],
                       closed_on=parsed_dict['closed_on'])

    @staticmethod
    def session_instance_serialize(session_instance):
        return json.dumps(session_instance, cls=CustomJSONEncoder)

    @staticmethod
    def session_instances_serialize(session_list):
        return [JSONSerializer.session_instance_serialize(session) for session in session_list]

    @staticmethod
    def user_instance_deserialize(parsed_dict):
        pic_id = parsed_dict['pic_id'] if 'pic_id' in parsed_dict else 0
        return User(user_id=parsed_dict['id'],
                    tag_id=parsed_dict['tag_id'],
                    first_name=parsed_dict['first_name'],
                    last_name=parsed_dict['last_name'],
                    email=parsed_dict['email'],
                    role_id=parsed_dict['role_id'],
                    pic_id=pic_id)

    @staticmethod
    def user_instance_serialize(user_instance):
        return json.dumps(user_instance, cls=CustomJSONEncoder)

    @staticmethod
    def user_instances_serialize(user_list):
        return [JSONSerializer.user_instance_serialize(user) for user in user_list]

    @staticmethod
    def create_user_dict(user, pic_id):
        return {
            'id': user['user_id'] if 'user_id' in user else user['id'] if 'id' in user else -1,
            'tag_id': user['tag_id'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email'],
            'role_id': user['role_id'],
            'pic_id': pic_id
        }

    @staticmethod
    def jwt_cookie_serialize(serialized_user_data, auth_token):
        data = {
            'data': serialized_user_data,
            'token': auth_token
        }
        return json.dumps(data)

    @staticmethod
    def user_session_instance_deserialize(parsed_dict):
        return {
            'user_id': parsed_dict['user_id'],
            'key_id': parsed_dict['key_id'],
            'timestamp': parsed_dict['timestamp']
        }

    @staticmethod
    def user_session_instance_serialize(user_session_instance):
        return json.dumps(user_session_instance, cls=CustomJSONEncoder)

    @staticmethod
    def unicode_to_ascii(unicode_string):
        if 'unicode' in type(unicode_string):
            return unicode_string.encode('ascii', 'ignore')
        else:
            return unicode_string  # it is not unicode


class ImageB64Serializer(object):
    @staticmethod
    def get_image_from_base64(image_base64):
        return base64.b64decode(image_base64)
