import os
import xlrd
import xlwt
from ..db import SqliteManager as dbm
from ..models.models import Key
from ..config import DATA_DIR_PATH as data_store_path
from ..config import DATA_EXCEL_PATH as xls_store_path


def switch(argument):
    switcher = {
        0: 'id',
        1: 'predio zgrade',
        2: 'odjel',
        3: 'kat',
        4: 'broj prostorije'
    }
    return switcher.get(argument, 'nepoznato')


def seed(file_location):
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_name('kljucevi')
    data = []
    for i in range(1, sheet.nrows):
        room_dict = {
            switch(0): 0
        }
        for j in range(sheet.ncols):
            field_name = switch(j)
            field_value = sheet.cell_value(i, j)
            room_dict[field_name] = field_value
        data.append(room_dict)
    db = dbm.get_db()
    cur = db.cursor()
    results = []
    for i in range(len(data)):
        row = data[i]
        room_id = int(row[switch(4)])
        block_name = row[switch(1)]
        sector_name = row[switch(2)]
        floor = int(row[switch(3)])
        room_repr = block_name + sector_name + str(floor) + '-' + str(room_id)
        params = tuple([p for p in (room_id, block_name, sector_name, floor, room_repr)])
        cur.execute('''INSERT OR IGNORE INTO Key (room_id, block_name, sector_name, floor, room_repr)
            VALUES ( ?, ?, ?, ?, ? )''', params)
        db.commit()
        cur.execute('SELECT id FROM Key WHERE room_id = ? ', (room_id,))
        room_pk = cur.fetchone()[0]
        data[i]['id'] = room_pk
        tag_id = ''
        results.append(Key(room_pk, tag_id, room_id, block_name, sector_name, floor, room_repr))
    dbm.close_connection(db)
    return results


def make_template():
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('kljucevi')
    for s in range(0, 5):
        col_name = switch(s)
        sheet.write(0, s, col_name)
    file_location = os.path.join(data_store_path, 'data_template.xls')
    workbook.save(file_location)


def template_exists(file_location=None, filename=None):
    if None is not filename:
        file_location = os.path.join(xls_store_path, filename)
    elif None is file_location:
        file_location = os.path.join(data_store_path, 'data_template.xls')
    if not os.path.isfile(file_location):
        return False
    else:
        return True


def get_template(filename=None):
    if None is not filename:
        file_location = os.path.join(xls_store_path, filename)
        return file_location
    else:
        if not template_exists():
            make_template()
        file_location = os.path.join(data_store_path, 'data_template.xls')
        return file_location
