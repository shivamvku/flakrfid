import jwt
import datetime
from ..config import SECRET_KEY as key
from werkzeug.security import generate_password_hash, check_password_hash


class AuthManager():
    @staticmethod
    def secure_password(raw_password):
        """
        Hashes the password using werkzeug.security.generate_password_hash function
        :param raw_password:
        :return: string
        """
        return generate_password_hash(raw_password)

    @staticmethod
    def check_password(password_hash, password):
        """
        Validates the password hash using werkzeug.security.check_password_hash function
        :param password:
        :return: bool
        """
        print("Password is %s" % password)
        print("Hashed password is %s" % password_hash)
        print("Password check becomes %s" % check_password_hash(password_hash, password))
        print("Hashing the form password is %s" % AuthManager.secure_password(password))
        print("Password check becomes %s" % check_password_hash(password_hash, AuthManager.secure_password(password)))
        return check_password_hash(password_hash, password)

    @staticmethod
    def encode_auth_token(user):
        """
        Encodes a new auth token for cookie
        :param user:
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user.email
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'ERROR: Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'ERROR: Invalid token. Please log in again.'
