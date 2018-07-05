import os
from ..db import SqliteManager as dbm
from ..config import UPLOAD_URI as upu


def get_img_rel_url(img_url):
    start_of_rel_url = img_url.find('/static')
    return img_url[start_of_rel_url:]


def get_img_url(pic_id, is_relative=False):
    if None is pic_id:
        return os.path.join(upu, 'default.png')
    db = dbm.get_db()
    cur = db.cursor()
    sql_command = 'SELECT location FROM ImageStore WHERE id = ?'
    params = (pic_id,)
    cur.execute(sql_command, params)
    result = cur.fetchone()
    print('From server image service - Image location is %s' % result)
    pic_url = result[0]
    dbm.close_connection(db)
    return pic_url if not is_relative else get_img_rel_url(pic_url)


def get_img_id(pic_url):
    if None is pic_url or '' is pic_url:
        pic_url = os.path.join(upu, 'default.png')
    db = dbm.get_db()
    cur = db.cursor()
    sql_command = 'SELECT id FROM ImageStore WHERE location = ?'
    params = (pic_url,)
    cur.execute(sql_command, params)
    result = cur.fetchone()
    print('From server image service - Image id is %s' % result)
    pic_id = result[0]
    dbm.close_connection(db)
    return pic_id


def save_img(image):
    if None is image:
        return os.path.join(upu, 'default.png'), 1
    print('From server - image service - image file received %s' % image)
    if '' == image.filename:
        return os.path.join(upu, 'default.png'), 1
    file = image
    file_name = image.filename
    print('From server - image service - image filename is %s' % file_name)
    file_src = os.path.join(upu, file_name)
    db = dbm.get_db()
    cur = db.cursor()
    sql_command = 'SELECT id FROM ImageStore WHERE name = ? AND location = ?'
    params = (file_name, file_src,)
    cur.execute(sql_command, params)
    stored_pic = cur.fetchone()
    if None is not stored_pic and os.path.isfile(file_src):
        pic_id = stored_pic[0]
        print('From server image service - already stored image - id is %s' % pic_id)
    else:
        file.save(file_src)
        print('From server - image service - new file src is %s' % file_src)
        sql_command = 'INSERT OR IGNORE INTO ImageStore (name, location) VALUES (?, ?)'
        params = (file_name, file_src,)
        cur.execute(sql_command, params)
        db.commit()
        sql_command = 'SELECT id FROM ImageStore WHERE name = ? AND location = ?'
        cur.execute(sql_command, params)
        stored_pic = cur.fetchone()
        pic_id = stored_pic[0]
        print('From server image service - newly stored image - id is %s' % pic_id)
    dbm.close_connection(db)
    return file_src, pic_id
