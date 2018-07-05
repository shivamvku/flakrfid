import getpass
import json
import sys
from src.services.service_manager import ServiceManager


def clean():
    if ServiceManager.start_db(drop_create=True, seed_data=False, backup_data=False):
        message = {
            'status': 200,
            'message': 'Successfully cleaned the database!'
        }
    else:
        message = {
            'status': 404,
            'message': 'Unable to backup data!'
        }
    result = json.dumps(message)
    print('Flushing the database...')
    print('--------------------------------------------')
    print(result)


def clean_with_backup():
    if ServiceManager.start_db(drop_create=True, seed_data=False, backup_data=True):
        message = {
            'status': 200,
            'message': 'Successfully cleaned the database!'
        }
    else:
        message = {
            'status': 404,
            'message': 'Unable to backup data!'
        }
    result = json.dumps(message)
    print('Backing up and flushing the database...')
    print('--------------------------------------------')
    print(result)


def load_data():
    if ServiceManager.start_db(drop_create=True, seed_data=True, backup_data=True):
        message = {
            'status': 200,
            'message': 'Successfully cleaned the database!'
        }
    else:
        message = {
            'status': 404,
            'message': 'Unable to backup data!'
        }
    result = json.dumps(message)
    print('Importing seed data into the database...')
    print('--------------------------------------------')
    print(result)


def show_backup_files():
    file_names = ServiceManager.get_backup_file_names()
    print('Listing backup files')
    print('--------------------------------------------')
    for file_name in file_names:
        print(file_name)


def create_user(is_void=True):
    print('Initializing the reader - move your tag close to the reader upon activation...')
    reader_data = ServiceManager.init_reader()
    if reader_data is None or 'No tag data detected...' in reader_data['message']:
        print('Reader did not detect your tag, enter this command again and move your tag closer...')
    else:
        tag_id = reader_data['data']
        first_name = raw_input('Type in the first name of the user: ').decode('utf-8')
        last_name = raw_input('Type in the last name of the user: ').decode('utf-8')
        email = raw_input('Type in email for the user: ').decode('utf-8')
        password = getpass.getpass('Type in password for the user: ').decode('utf-8')
        role_id = 2
        user = ServiceManager.create_user(tag_id=tag_id,
                                          email=email,
                                          password=password,
                                          first_name=first_name,
                                          last_name=last_name,
                                          role_id=role_id)
        if not is_void:
            return user


def create_super_user():
    user = create_user(is_void=False)
    ServiceManager.update_user(user_id=user.id, role_id=1)


def show_help():
    print('Shell options...')
    print('--------------------------------------------')
    for opt in command_options:
        print(opt)


def nop():
    print()


command_options = ['clean', 'clean -b', 'loaddata', 'showbackups', 'createuser', 'createsuperuser']

try:
    args = sys.argv
    if 'clean' in args:
        clean()
    if 'clean' in args and '-b' in args:
        clean_with_backup()
    if 'loaddata' in args:
        load_data()
    if 'showbackups' in args:
        show_backup_files()
    if 'createuser' in args:
        create_user()
    if 'createsuperuser' in args:
        create_super_user()
    if 'help' in args or '--help' in args:
        show_help()
    sys.exit(0)
except Exception as e:
    print('Full error: %s' % e)
    sys.exit(2)
