from ..db import SqliteManager as dbm


def create_user_auth_request(user_id, timestamp):
    db = dbm.get_db()
    cur = db.cursor()
    affected_count = cur.execute(
        '''INSERT OR IGNORE INTO UserSession (user_id, timestamp) VALUES ( ?, ?, ?, ?, ?, ? )''', (user_id, timestamp,))
    db.commit()
    if affected_count > 0:
        cur.execute('SELECT id FROM UserSession WHERE user_id = ? AND timestamp = ?', (user_id, timestamp,))
        result = cur.fetchone()
        session_id = int(result[0])
        dbm.close_connection(db)
        return {"id": session_id, "user_id": user_id, "timestamp": timestamp}
    else:
        dbm.close_connection(db)
        return None


def get_user_auth_requests(user_id, limit=0):
    db = dbm.get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM UserSession WHERE user_id = ?', (user_id,))
    results = cur.fetchall() if limit == 0 else cur.fetchmany(size=limit)
    sessions = [{"id": res[0], "user_id": res[1], "timestamp": res[2]} for res in results]
    dbm.close_connection(db)
    return sessions
