# *********** sessions ***********

from . import (
    app,
    service_manager,
    jserial,
    jsonify,
    request,
    Response
)
from .auth_views import (
    verify_token,
    get_request_auth
)


# <editor-fold desc="Sessions Views">


@app.route('/api/sessions', methods=['GET'])
def api_sessions_get():
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    raw_sessions = service_manager.get_sessions()
    sessions = []
    for session in raw_sessions:
        sessions.append(service_manager.get_session_ui_model(session=session))
    data = jserial.session_instances_serialize(session_list=sessions)
    if None is not data:
        resp = jsonify(data)
        resp.status_code = 200
    else:
        message = {'status': 404, 'message': 'Not Found'}
        resp = jsonify(message)  # list of sessions - jsonify iterates over list
        resp.status_code = 404
    return resp


@app.route('/api/sessions/<int:session_id>', methods=['GET'])
def api_session_get(session_id):
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    session_raw = service_manager.search_session(session_id=session_id)
    if None is session_raw:
        message = {
            'status': 404,
            'message': 'Not Found' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        session = service_manager.get_session_ui_model(session=session_raw)
        data = jserial.session_instance_serialize(session_instance=session)
        resp = Response(data, status=200, mimetype='application/json')
        resp.status_code = 200
        return resp


@app.route('/api/sessions/key/<int:key_id>', methods=['GET'])
def api_sessions_get_by_key(key_id):
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    results = service_manager.search_session(key_id=key_id, limit=0)
    if None is not results:
        sessions = [service_manager.get_session_ui_model(session=session) for session in results]
        data = jserial.session_instances_serialize(session_list=sessions)
        resp = jsonify(data)
        resp.status_code = 200
    else:
        message = {'status': 404, 'message': 'Not Found'}
        resp = jsonify(message)
        resp.status_code = 404
    return resp


@app.route('/api/sessions/user/<int:user_id>', methods=['GET'])
def api_sessions_get_by_user(user_id):
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    results = service_manager.search_session(user_id=user_id, limit=0)
    if None is not results:
        sessions = [service_manager.get_session_ui_model(session) for session in results]
        data = jserial.session_instances_serialize(session_list=sessions)
        resp = jsonify(data)  # sessions of single user - jsonify iterates over list
        resp.status_code = 200
    else:
        message = {'status': 404, 'message': 'Not Found'}
        resp = jsonify(message)
        resp.status_code = 404
    return resp


@app.route('/api/sessions/new', methods=['POST'])
def api_session_new():
    print('From server - receiving data from new session')
    data = request.get_json()
    print('From server - new session data: %s' % data)
    if None is data:
        message = {
            'status': 404,
            'message': 'Not Found' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        message = {
            'status': 200,
            'data': ''
        }
        data_deserialized = jserial.json_deserialize(data)
        user_id = int(data_deserialized['user_id'])
        user = service_manager.search_user(tag_id=user_id)
        key_id = int(data_deserialized['key_id'])
        key = service_manager.search_key(tag_id=key_id)
        session = None
        if None is key_id or '' == key_id or None is user_id or '' == user_id:
            return Response('Key ID or user ID not found so no session can be registered, retry...', status=404,
                            mimetype='application/json')
        elif None is user or None is key:
            message = {
                'status': 404,
                'message': 'Not Found' + request.url + ' - ' + ('user ' if None is user else 'key') + ' not registered',
            }
            resp = jsonify(message)
            resp.status_code = 404
            return resp
        else:
            session = service_manager.search_session(key_id=key.id,
                                                     user_id=user.id,
                                                     exclusive=True,
                                                     is_active=True)
        if None is not session:
            session.closed_on = data_deserialized['timestamp']
            service_manager.update_session(
                session.id, session.key_id, session.user_id, session.started_on, session.closed_on
            )
        else:
            if not (-1 == key_id or -1 == user_id):
                session = service_manager.create_session(key.id, user.id, data_deserialized['timestamp'])
        message['data'] = jserial.session_instance_serialize(service_manager.get_session_ui_model(session))
        resp = jsonify(message)
        resp.status_code = 200
        return resp


@app.route('/api/sessions/delete/<int:session_id>', methods=['DELETE'])
def api_session_delete(session_id):
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    if service_manager.delete_session(session_id=session_id):
        message = {
            'status': 200,
            'message': 'Successfully deleted session'
        }
        resp = jsonify(message)
        resp.status_code = 200
        return resp
    else:
        message = {
            'status': 404,
            'message': 'Session not found'
        }
        resp = jsonify(message)
        resp.status_code = 200
        return resp


# </editor-fold>
