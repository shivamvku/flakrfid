import os
import json
from sessionHandler import SessionHandler


# class that encapsulates session storage logic
class SessionRepository(object):
    # initialize SessionRepository object for managing session storage
    def __init__(self, data_storage_path):
        self.data_storage_path = data_storage_path

    # method for getting session from storage by sessionId
    def get_session(self, session_id):
        if os.stat(self.data_storage_path).st_size > 0:
            with open(self.data_storage_path, 'r') as jsonStorage:
                sessions = []
                for line in jsonStorage:
                    sessions.append(json.loads(line))
                for s in sessions:
                    session = SessionHandler.session_hook_handler(s)
                    if session.session_id == session_id:
                        return session
        return None

    # method for getting all sessions from storage
    def get_sessions(self):
        if os.stat(self.data_storage_path).st_size > 0:
            with open(self.data_storage_path, 'r') as jsonStorage:
                sessions = []
                for line in jsonStorage:
                    sessions.append(json.loads(line))
                return sessions
        return None

    # method for storing a session into storage file
    def store_session(self, session):
        with open(self.data_storage_path, 'a') as jsonStorage:
            jsonStorage.write(str(session))
            jsonStorage.write('\n')
            jsonStorage.flush()
            os.fsync(jsonStorage)

    # method for getting last id
    def get_last_id(self):
        if os.stat(self.data_storage_path).st_size > 0:
            with open(self.data_storage_path, 'r') as jsonStorage:
                sessions = [SessionHandler.session_hook_handler(json.loads(line)) for line in jsonStorage.readlines()]
                last_id = -1
                for s in sessions:
                    if last_id < s.session_id:
                        last_id = s.session_id
                return last_id
