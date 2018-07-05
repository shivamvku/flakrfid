import json
import datetime


# class that provides JSON serialization of UserInfo object (transforms it into dict)
class UserEncoder(json.JSONEncoder):
    def default(self, o):
        if type(o) is datetime.datetime:
            # return {"time_span": str(o)}
            return str(o)
        return o.__dict__


# class for encapsulating user profile data
class UserInfo(object):

    # initialize
    def __init__(self, u_id, u_name, email, first_name, last_name, key_id, start_on, end_on):
        self._user_id = u_id
        self._user_name = u_name
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._current_key_id = key_id
        self._session_start = start_on
        self._session_end = end_on

    # string repr of UserInfo object (using json serializer)
    def __repr__(self):
        return json.dumps(self, cls=UserEncoder)

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, id):
        self.user_id = id

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, name):
        self._user_name = name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        self._first_name = first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        self._last_name = last_name

    @property
    def current_key_id(self):
        return self._current_key_id

    @current_key_id.setter
    def current_key_id(self, id):
        self._current_key_id = id

    @property
    def session_start(self):
        return self._session_start

    @session_start.setter
    def session_start(self, start_on):
        self._session_start = start_on

    @property
    def session_end(self):
        return self._session_end

    @session_end.setter
    def session_end(self, end_on):
        self._session_end = end_on
