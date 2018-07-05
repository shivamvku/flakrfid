import datetime
from ..db import SqliteManager as dbm
from ..models.models import Session


def create_session(key_id, user_id, started_on=datetime.datetime.now()):
    db = dbm.get_db()
    try:
        cur = db.cursor()
        affected_count = cur.execute('''INSERT OR IGNORE INTO Session (key_id, user_id, started_on)
                    VALUES ( ?, ?, ? )''', (key_id, user_id, started_on))
        db.commit()
        if affected_count > 0:
            cur.execute('SELECT id FROM Session WHERE key_id = ? AND user_id = ? ', (key_id, user_id,))
            result = cur.fetchone()
            session_id = result[0]
            dbm.close_connection(db)
            return Session(session_id=session_id, key_id=key_id, user_id=user_id, started_on=started_on, closed_on="")
        else:
            raise "Affected rows: ", affected_count
    except:
        return None
    finally:
        dbm.close_connection(db)


def get_sessions(limit=0):
    db = dbm.get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM Session')
    results = cur.fetchall() if limit == 0 else cur.fetchmany(size=limit)
    sessions = [Session(res[0], res[1], res[2], res[3], res[4]) for res in results]
    dbm.close_connection(db)
    return sessions


def search_session(session_id=None, key_id=None, user_id=None, started_on=None, closed_on=None, limit=1,
                   exclusive=False, is_active=False):
    if not (session_id is None and key_id is None and user_id is None and started_on is None and closed_on is None):
        db = dbm.get_db()
        cur = db.cursor()
        params = tuple([p for p in [session_id, key_id, user_id, started_on, closed_on] if p is not None])
        condition_operator = ' AND ' if exclusive else ' OR '
        sql_conditions = condition_operator.join(filter(
            lambda x: x is not '', [' id = ? ' if session_id is not None else '',
                                    ' key_id = ? ' if key_id is not None else '',
                                    ' user_id = ? ' if user_id is not None else '',
                                    ' started_on = ? ' if started_on is not None else '',
                                    ' closed_on IS NULL' if is_active else
                                    ' closed_on = ? ' if closed_on is not None else '']))
        sql_command = 'SELECT * FROM Session WHERE ' + sql_conditions
        print('From server - session factory - search sql command is %s %s' % (sql_command, params))
        cur.execute(sql_command, params)
        results = [cur.fetchone()] if limit == 1 else cur.fetchall()
        print('From server - session factory - search results: %s' % results)
        dbm.close_connection(db)
        if None is results or 0 == len(results) or None is results[0]:
            return None
        else:
            sessions = []
            if len(results) > 1:
                sessions = [Session(res[0], res[1], res[2], res[3], res[4]) for res in results]
            else:
                res = results[0]
                sessions.append(Session(res[0], res[1], res[2], res[3], res[4]))
            return sessions[0] if limit == 1 else sessions
    else:
        return None


def delete_session(session_id=None, key_id=None, user_id=None, started_on=None, closed_on=None):
    if not (session_id is None and key_id is None and user_id is None and started_on is None and closed_on is None):
        db = dbm.get_db()
        cur = db.cursor()
        params = tuple([p for p in [session_id, key_id, user_id, started_on, closed_on] if p is not None])
        condition_operator = ' AND '
        sql_conditions = condition_operator.join(filter(
            lambda x: x is not '', [' id = ? ' if session_id is not None else '',
                                    ' key_id = ? ' if key_id is not None else '',
                                    ' user_id = ? ' if user_id is not None else '',
                                    ' started_on = ? ' if started_on is not None else '',
                                    ' closed_on = ? ' if closed_on is not None else '']))
        # delete session
        sql_command = 'DELETE FROM Session WHERE ' + sql_conditions
        cur.execute(sql_command, params)
        db.commit()
        # check if session deleted
        sql_command = 'SELECT * FROM Session WHERE ' + sql_conditions + (' LIMIT 1 ' if session_id is not None else '')
        cur.execute(sql_command, params)
        result = cur.fetchone()
        dbm.close_connection(db)
        return None is result
    else:
        return None


def update_session(session_id, key_id=None, user_id=None, started_on=None, closed_on=None):
    if not (key_id is None and user_id is None and started_on is None and closed_on is None) and session_id is not None:
        db = dbm.get_db()
        cur = db.cursor()
        params = tuple([p for p in [key_id, user_id, started_on, closed_on] if p is not None])
        updates_separator = ' , '
        sql_updates = updates_separator.join(filter(
            lambda x: x is not '', [' key_id = ? ' if key_id is not None else '',
                                    ' user_id = ? ' if user_id is not None else '',
                                    ' started_on = ? ' if started_on is not None else '',
                                    ' closed_on = ? ' if closed_on is not None else '']))
        # update session
        sql_command = 'UPDATE Session SET ' + sql_updates + ' WHERE id = ? '
        params += (session_id,)
        # params *= 2
        cur.execute(sql_command, params)
        db.commit()
        # return updated session
        sql_command = 'SELECT * FROM Session WHERE id = ? LIMIT 1 '
        cur.execute(sql_command, (session_id,))
        result = cur.fetchone()
        session = Session(session_id=result[0],
                          key_id=result[1],
                          user_id=result[2],
                          started_on=result[3],
                          closed_on=result[4])
        dbm.close_connection(db)
        return session
    else:
        return None
