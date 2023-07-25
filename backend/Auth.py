import datetime
import time

import jwt

from werkzeug.security import generate_password_hash, check_password_hash

from Common import Config


class Auth:
    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    @staticmethod
    def check_password(hash, password):
        return check_password_hash(hash, password)

    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # 过期时间验证
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))

            payload = jwt.decode(auth_token, Config.SECRET_KEY, options={'verify_exp': False}, algorithms=['HS256'])
            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    @staticmethod
    def encode_jwt(userid, isAdmin, email, username):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'data': {
                'id': userid,
                'isAdmin': isAdmin,
                'email': email,
                'username': username
            }
        }

        return jwt.encode(
            payload,
            Config.SECRET_KEY,
            algorithm='HS256'
        )

    @staticmethod
    def decode_JWT(auth_token):
        # try:
        payload = jwt.decode(auth_token, Config.SECRET_KEY, options={'verify_exp': False}, algorithms=['HS256'])
        if ('data' in payload and 'id' in payload['data']):
            return payload
        else:
            raise jwt.InvalidTokenError
    # raise jwt.ExpiredSignatureError:
    #     return 'Token过期'
    # except jwt.InvalidTokenError:
    #     return '无效Token'
