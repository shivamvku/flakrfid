import os
import time
import shutil
from ..config import DATA_DIR_PATH as data_dir_path
from ..config import DATABASE_URI as db


def backup_db():
    file_location = os.path.join(
        data_dir_path, 'backup-' + str(time.strftime("%x")).replace('/', '.') + '.sqlite')
    shutil.copy2(db, file_location)
    if not os.path.isfile(file_location):
        return False
    else:
        return True


def backup_file_names():
    file_names = [f for f in os.listdir(data_dir_path) if os.path.isfile(
        os.path.join(data_dir_path, f)) if 'backup' in f]
    return file_names
