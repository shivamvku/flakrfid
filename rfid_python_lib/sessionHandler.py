from sessionInfo import SessionInfo


class SessionHandler(object):
    # method for hooking parsed json object into SessionInfo for usage in SessionRepository
    @staticmethod
    def session_hook_handler(parsed_dict):
        return SessionInfo(session_id=parsed_dict['_session_id'],
                           user_id=parsed_dict['_user_id'],
                           time_stamp=parsed_dict['_time_stamp'],
                           key_id=parsed_dict['_key_id'])
