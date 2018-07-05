# *********** auth ***********

from . import (
    app,
    service_manager,
    jsonify,
    request,
    Response
)


# *********** auth ***********
# <editor-fold desc="Authentication checking views">

def get_request_auth(request):
    try:
        auth_header_value = request.headers.get('Authorization', None)
        if not auth_header_value:
            print('Invalid JWT header: No authorization headers')
            raise Exception('Invalid JWT header: No authorization headers')
        header_parts = auth_header_value.split(' ')

        if header_parts[0].lower() != 'token':
            print('Invalid JWT header: Unsupported authorization type')
            raise Exception('Invalid JWT header: Unsupported authorization type')
        elif len(header_parts) == 1:
            print('Invalid JWT header: Token missing')
            raise Exception('Invalid JWT header: Token missing')
        elif len(header_parts) > 2:
            print('Invalid JWT header: Token contains spaces')
            raise Exception('Invalid JWT header: Token contains spaces')

        return '1%s' % header_parts[1]
    except Exception as e:
        print('Exception hit on get request auth')
        return '0%s' % repr(e)


def verify_token(token):
    return service_manager.validate_token(auth_token=token)


@app.route('/api/login', methods=['POST'])
def api_user_login():
    try:
        auth_data = request.get_json()
        email = auth_data['email']
        password = auth_data['password']
        print('Entered api login route on server side...')
        print('Email is %s' % email)
        print('Password is %s' % password)
        user_qs = service_manager.search_user(email=email, limit=1)
        if user_qs is None:
            raise Exception('User email not registered!')
        password_qs = service_manager.get_password(user_id=user_qs.id)
        if password_qs is None:
            raise Exception('User has not set the password yet!')
        user_auth = service_manager.check_password(password_qs, password)
        if user_auth is None or user_auth is False:
            raise Exception('Incorrect password!')
        token = service_manager.generate_token(user=user_qs, password=password_qs)
        if token is None:
            raise Exception('Failed to generate a user token...')
        # TODO: generating csrf for http headers in ajax calls (during login)
        # csrf = service_manager.generate_csrf()
        # if csrf is None:
        #     raise Exception('Failed to generate a csrf token...')
        print('Printing the token from get auth...')
        print(token)
        resp = jsonify(token)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e.message)
        resp = jsonify({
            'status': 404,
            'message': e.message
        })
        resp.status_code = 404
        return resp


        # </editor-fold>
