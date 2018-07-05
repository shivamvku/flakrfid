import os
from ..config import DATA_DIR_PATH as data_path
from ..config import DATA_EXCEL_PATH as excel_path


class StorageManager(object):
    def __init__(self):
        self.default_excel_seed_file = os.path.join(excel_path, 'data_template.xls')
        self.default_json_seed_file = os.path.join(data_path, 'tagReadings.txt')

    def store_file(self, file, type):
        if None is file:
            return None
        print('From server - storage manager - file received %s' % file)
        if '' == file.filename:
            return None
        file_name = file.filename
        print('From server - storage manager - filename is %s' % file_name)
        file_src = self.get_path_by_type(file_name=file_name, type_id=type)
        file.save(file_src)
        print('From server - storage manager - file stored at %s' % file_src)
        return file_src

    def get_path_by_type(self, file_name, type_id):
        if 0 == type_id:
            return os.path.join(excel_path, file_name)
        else:
            return os.path.join(data_path, file_name)
