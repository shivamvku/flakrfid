from . import images_service
from . import key_factory
from . import session_factory
from . import user_auth_request_service
from . import user_factory
from .auth_service import AuthManager
from .csrf_service import generate_csrf
from .db_seed import DbInitializer
from .db_backup import backup_db, backup_file_names
from .storage_manager import StorageManager
from ..db import SqliteManager
from .. import app

if not app.debug:
    from ..embedded.mfrc_service import ServiceMFRC
from ..models.adapters import UserProfile, SessionView


class ServiceManager(object):
    @staticmethod
    def start_db(drop_create=False, seed_data=False, backup_data=False):
        if backup_data:
            if not backup_db():
                return False
        if drop_create:
            SqliteManager.db_init()
        if seed_data:
            stm = StorageManager()
            file = stm.default_excel_seed_file
            ServiceManager.seed_from_excel(filename=file)
        return True

    @staticmethod
    def seed_from_excel(file_location=None, filename=None):
        seed = DbInitializer()
        if None is not filename:
            return seed.seed_from_excel(filename)
        else:
            return seed.seed_from_excel(file_location)

    @staticmethod
    def get_excel_template(filename=None):
        seed = DbInitializer()
        return seed.get_excel_template(filename=filename)

    @staticmethod
    def seed_from_json():
        seed = DbInitializer()

    @staticmethod
    def get_backup_file_names():
        return backup_file_names()

    # api for keys
    # <editor-fold desc="API for managing Keys">
    @staticmethod
    def get_keys():
        return key_factory.get_keys()

    @staticmethod
    def search_key(key_id=None, tag_id=None, room_id=None, block_name=None,
                   sector_name=None, floor=None, room_repr=None, limit=1, exclusive=False):
        return key_factory.search_key(
            key_id, tag_id, room_id, block_name, sector_name, floor, room_repr, limit, exclusive)

    @staticmethod
    def create_key(tag_id, room_id, block_name, sector_name, floor, room_repr):
        return key_factory.create_key(tag_id, room_id, block_name, sector_name, floor, room_repr)

    @staticmethod
    def delete_key(key_id=None, room_id=None, delete_history=False):
        return key_factory.delete_key(key_id, room_id, delete_history)

    @staticmethod
    def update_key(key_id, tag_id=None, room_id=None, block_name=None, sector_name=None, floor=None, room_repr=None):
        return key_factory.update_key(key_id, tag_id, room_id, block_name, sector_name, floor, room_repr)

    # </editor-fold>

    # api for users
    # <editor-fold desc="API for managing Users and Auth">
    @staticmethod
    def get_users():
        return user_factory.get_users()

    @staticmethod
    def search_user(user_id=None, tag_id=None, first_name=None, last_name=None, email=None, role_id=None, pic_id=None,
                    limit=1, exclusive=False):
        return user_factory.search_user(user_id, tag_id, first_name, last_name, email, role_id, pic_id, limit,
                                        exclusive)

    @staticmethod
    def create_user(tag_id, first_name=None, last_name=None, email=None, password=None, role_id=1, pic_id=1):
        return user_factory.create_user(tag_id, first_name, last_name, email, password, role_id, pic_id)

    @staticmethod
    def delete_user(user_id, delete_history=True):
        return user_factory.delete_user(user_id, delete_history)

    @staticmethod
    def update_user(user_id, tag_id=None, first_name=None, last_name=None, email=None, role_id=None, pic_id=None):
        return user_factory.update_user(user_id=user_id, tag_id=tag_id,
                                        first_name=first_name, last_name=last_name,
                                        email=email, role_id=role_id, pic_id=pic_id)

    @staticmethod
    def get_password(user_id):
        return user_factory.get_password(user_id=user_id)

    @staticmethod
    def secure_password(raw_password):
        return AuthManager.secure_password(raw_password=raw_password)

    @staticmethod
    def set_password(user, password):
        return user_factory.set_password(user_id=user.id, new_password=password)

    @staticmethod
    def check_password(password_hash, password):
        return AuthManager.check_password(password_hash=password_hash, password=password)

    @staticmethod
    def generate_token(user, password):
        return AuthManager.encode_auth_token(user=user)

    @staticmethod
    def validate_token(auth_token):
        email = AuthManager.decode_auth_token(auth_token=auth_token)
        if email is None or 'ERROR' in email:
            return False
        return user_factory.search_user(email=email) is not None

    @staticmethod
    def generate_csrf():
        return generate_csrf()

    @staticmethod
    def get_user_ui_model(user):
        pic_url = images_service.get_img_url(user.pic_id, True)
        return UserProfile(user.id, user.tag_id, user.first_name, user.last_name, user.email, user.role_id, pic_url)

    # </editor-fold>

    # api for sessions
    # <editor-fold desc="API for managing Sessions">
    @staticmethod
    def get_sessions():
        return session_factory.get_sessions()

    @staticmethod
    def search_session(session_id=None, key_id=None, user_id=None, started_on=None, closed_on=None, limit=1,
                       exclusive=False, is_active=False):
        return session_factory.search_session(session_id, key_id, user_id, started_on, closed_on, limit, exclusive,
                                              is_active)

    @staticmethod
    def create_session(key_id=None, user_id=None, started_on=None):
        return session_factory.create_session(key_id, user_id, started_on)

    @staticmethod
    def delete_session(session_id=None, key_id=None, user_id=None, started_on=None, closed_on=None):
        return session_factory.delete_session(session_id, key_id, user_id, started_on, closed_on)

    @staticmethod
    def update_session(session_id, key_id=None, user_id=None, started_on=None, closed_on=None):
        return session_factory.update_session(session_id, key_id, user_id, started_on, closed_on)

    @staticmethod
    def get_session_ui_model(session):
        room_repr = (ServiceManager.search_key(key_id=session.key_id)).room_repr
        user = ServiceManager.search_user(user_id=session.user_id)
        first_name, last_name = user.first_name, user.last_name
        return SessionView(session_id=session.id, key_id=session.key_id, room_repr=room_repr,
                           user_id=session.user_id, first_name=first_name, last_name=last_name,
                           started_on=session.started_on, closed_on=session.closed_on)

    # </editor-fold>

    # api for user auth requests
    # <editor-fold desc="API for User-Auth requests">
    @staticmethod
    def create_user_auth_request(user_id, timestamp):
        return user_auth_request_service.create_user_auth_request(user_id=user_id, timestamp=timestamp)

    @staticmethod
    def get_user_auth_requests(user_id, limit=0):
        return user_auth_request_service.get_user_auth_requests(user_id=user_id, limit=limit)

    # </editor-fold>

    # api for matching
    @staticmethod
    def init_reader():
        if not app.debug:
            reader = ServiceMFRC()
            print('From server - service manager - reader activated')
            data = reader.do_read()
            print('From server - service manager - reader message is %s' % data['message'])
            print('From server - service manager - tag data is %s' % data['data'])
            return data
        else:
            return {
                'message': 'No tag data detected...',
                'data': '00000000'
            }

    @staticmethod
    def upload_image(image):
        return images_service.save_img(image)
