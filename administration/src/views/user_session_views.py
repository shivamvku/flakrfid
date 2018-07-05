# *********** user auth requests ***********

from . import (
    app,
    service_manager,
    jsonify,
    request,
    Response
)
from .auth_views import (
    verify_token,
    get_request_auth
)


# <editor-fold desc="User Auth Views">


@app.route('/api/user/auth-request', methods=['POST'])
def api_user_auth_request_new():
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    user = (request.get_json())
    if None is not user:
        user_session = service_manager.create_user_auth_request(user['user_id'], user['timestamp'])
        return jsonify(user_session)
    else:
        return Response('Faild action', status=404, mimetype='application/json')


@app.route('/api/user/auth-requests/<int:user_id>', methods=['GET'])
def api_user_auth_requests(user_id):
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    sessions = service_manager.get_user_auth_requests(user_id=user_id)
    if None is sessions:
        message = {
            'status': 404,
            'message': 'Not Found - no sessions for the selected user were found',
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        print(sessions)
        resp = jsonify(sessions)
        resp.status_code = 200
        return resp

# </editor-fold>
