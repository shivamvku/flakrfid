from ..db import SqliteManager as dbm
from ..models.models import Key


def create_key(tag_id, room_id, block_name, sector_name, floor, room_repr):
    if None is tag_id or None is room_id or None is sector_name or None is block_name or None is floor:
        return None
    db = dbm.get_db()
    try:
        cur = db.cursor()
        affected_count = cur.execute('''
            INSERT OR REPLACE INTO Key (tag_id, room_id, block_name, sector_name, floor, room_repr)
            VALUES ( ?, ?, ?, ?, ?, ? )''', (tag_id, room_id, block_name, sector_name, floor, room_repr))
        db.commit()
        if affected_count > 0:
            cur.execute('SELECT id FROM Key WHERE tag_id = ? AND room_repr = ? ', (tag_id, room_repr,))
            result = cur.fetchone()
            print(result)
            key_id = int(result[0])
            dbm.close_connection(db)
            dbm.close_connection(db)
            return Key(
                key_id=key_id,
                tag_id=tag_id,
                room_id=room_id,
                block_name=block_name,
                sector_name=sector_name,
                floor=floor,
                room_repr=room_repr)
        else:
            raise "Affected rows: ", affected_count
    except:
        dbm.close_connection(db)
        return None


def get_keys(limit=0):
    db = dbm.get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM Key')
    results = cur.fetchall() if limit == 0 else cur.fetchmany(size=limit)
    keys = [Key(res[0], res[1], res[2], res[3], res[4], res[5], res[6]) for res in results]
    dbm.close_connection(db)
    return keys


def search_key(key_id=None, tag_id=None, room_id=None, block_name=None, sector_name=None, floor=None,
               room_repr=None, limit=1, exclusive=False):
    if not (key_id is None and tag_id is None and room_id is None and None is block_name
            and None is sector_name and None is floor and None is room_repr):
        db = dbm.get_db()
        cur = db.cursor()
        params = tuple([p for p in [key_id, tag_id, room_id, block_name, sector_name, floor, room_repr]
                        if p is not None])
        condition_operator = ' AND ' if exclusive else ' OR '
        sql_conditions = condition_operator.join(filter(
            lambda x: x is not '', [' id = ? ' if key_id is not None else '',
                                    ' tag_id = ? ' if tag_id is not None else '',
                                    ' room_id = ? ' if room_id is not None else '',
                                    ' block_name = ? ' if block_name is not None else '',
                                    ' sector_name = ? ' if sector_name is not None else '',
                                    ' floor = ? ' if floor is not None else '',
                                    ' room_repr = ? ' if room_repr is not None else '']))
        sql_command = 'SELECT * FROM Key WHERE ' + sql_conditions
        print('From server - key factory - search sql command: %s %s' % (sql_command, params))
        cur.execute(sql_command, params)
        results = [cur.fetchone()] if limit == 1 else cur.fetchall()
        print('From server - key factory - search results: %s' % results)
        dbm.close_connection(db)
        if None is results or 0 == len(results) or None is results[0]:
            return None
        else:
            keys = []
            if len(results) > 1:
                keys = [Key(res[0], res[1], res[2], res[3], res[4], res[5], res[6]) for res in results]
            else:
                res = results[0]
                keys.append(Key(res[0], res[1], res[2], res[3], res[4], res[5], res[6]))
            return keys[0] if limit == 1 else keys
    else:
        return None


def delete_key(key_id=None, room_id=None, delete_history=False):
    if not (None is key_id and None is room_id):
        db = dbm.get_db()
        cur = db.cursor()
        params = tuple([p for p in [key_id, room_id] if p is not None])
        condition_operator = ' AND '
        sql_conditions = condition_operator.join(filter(
            lambda x: x is not '', [' id = ? ' if key_id is not None else '',
                                    ' room_id = ? ' if room_id is not None else '']))
        # delete all sessions where key_id matches selected key
        linked_sessions = None
        if True == delete_history:
            if None is key_id:
                sql_command = 'SELECT * FROM Key WHERE ' + sql_conditions
                cur.execute(sql_command, params)
                key_ids = tuple([i[0] for i in cur.fetchall()])
            else:
                key_ids = (key_id,)
            if 0 > len(key_ids) or None is key_ids:
                return False
            session_sql_conditions = ' OR '.join('key_id = ?' for i in range(len(key_ids)))
            sql_command = 'DELETE FROM Session WHERE ' + session_sql_conditions
            cur.execute(sql_command, key_ids)
            db.commit()
            # check if matched sessions deleted
            sql_command = 'SELECT * FROM Session WHERE ' + session_sql_conditions
            cur.execute(sql_command, key_ids)
            linked_sessions = cur.fetchall()
        # delete key
        sql_command = 'DELETE FROM Key WHERE ' + sql_conditions
        cur.execute(sql_command, params)
        db.commit()
        # check if key deleted
        sql_command = 'SELECT * FROM Key WHERE ' + sql_conditions + ' LIMIT 1 '
        cur.execute(sql_command, params)
        result = cur.fetchone()
        dbm.close_connection(db)
        return None is result and None is linked_sessions
    else:
        return False


def update_key(key_id, tag_id=None, room_id=None, block_name=None, sector_name=None, floor=None, room_repr=None):
    if not (tag_id is None and room_id is None and block_name is None and
                    sector_name is None and floor is None and room_repr is None) and key_id is not None:
        db = dbm.get_db()
        cur = db.cursor()
        params = tuple(
            [p for p in [tag_id, room_id, block_name, sector_name, floor, room_repr] if p is not None])
        updates_separator = ' , '
        sql_updates = updates_separator.join(filter(
            lambda x: x is not '', [' tag_id = ? ' if tag_id is not None else '',
                                    ' room_id = ? ' if room_id is not None else '',
                                    ' block_name = ? ' if block_name is not None else '',
                                    ' sector_name = ? ' if sector_name is not None else '',
                                    ' floor = ? ' if floor is not None else '',
                                    ' room_repr = ? ' if room_repr is not None else '']))
        # update key
        sql_command = 'UPDATE Key SET ' + sql_updates + ' WHERE id = ?'
        params += (key_id,)
        cur.execute(sql_command, params)
        print('The command: %s ' % sql_command)
        db.commit()
        # return updated key
        sql_command = 'SELECT * FROM Key WHERE id = ? LIMIT 1 '
        cur.execute(sql_command, (key_id,))
        result = cur.fetchone()
        if None is not result:
            key = Key(
                key_id=result[0],
                tag_id=result[1],
                room_id=result[2],
                block_name=result[3],
                sector_name=result[4],
                floor=result[5],
                room_repr=result[6])
            print('From server - key factory - retrieved key %s' % key.room_repr)
            print('From server - key factory - retrieved key-tag %s' % key.tag_id)
            return key
        dbm.close_connection(db)
        return None
    else:
        return None
