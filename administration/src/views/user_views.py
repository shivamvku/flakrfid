# *********** users ***********

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


# <editor-fold desc="Users Views">


@app.route('/api/users', methods=['GET'])
def api_users_get():
    auth_data = get_request_auth(request=request)
    print(auth_data)
    if auth_data[0] == '0':
        return Response(auth_data[1:], status=404, mimetype='application/json')
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    users = service_manager.get_users()
    if None is users or 1 > len(users):
        message = {
            'status': 404,
            'message': 'Not Found - no users found',
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        print('From server - users - %s' % users)
        ui_models = [service_manager.get_user_ui_model(u) for u in users]
        print('From server - users - pic_url of first user is: %s' % ui_models[0].pic_url)
        data = jserial.user_instances_serialize(user_list=ui_models)
        resp = jsonify(data)  # list of users - jsonify iterates over list
        resp.status_code = 200
        return resp


@app.route('/api/users/register', methods=['POST'])
def api_user_register():
    files = request.files
    if 'file' not in files:
        file = None
    else:
        file = files['file']
    pic_url, pic_id = service_manager.upload_image(file)
    user_dict = jserial.json_deserialize(request.form['user_json'])
    raw_password = user_dict['password']
    if raw_password is None:
        return Response(
            {'message': 'No password provided!', 'status': 404}, status=404, mimetype='application/json')
    else:
        password = service_manager.secure_password(raw_password=raw_password)  # creates secure password
    print('From server - on image upload - JSON data: %s' % user_dict)
    user_dict = jserial.create_user_dict(user_dict, pic_id)
    print('From server - user register (POST) - user json is %s' % user_dict)
    user = jserial.user_instance_deserialize(user_dict)
    print('From server - user register (POST) - user email is %s' % user.email)
    user = service_manager.create_user(tag_id=user.tag_id,
                                       first_name=user.first_name,
                                       last_name=user.last_name,
                                       email=user.email,
                                       password=password,
                                       role_id=user.role_id,
                                       pic_id=user.pic_id)
    if None is user or -1 == user.id:
        message = {
            'status': 404,
            'message': 'Not found - Unable to register user',
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        print('From server - api-user-register (post) - id of stored user is %s' % user.id)
        user_ui_model = service_manager.get_user_ui_model(user)
        data = jserial.user_instance_serialize(user_instance=user_ui_model)
        # user_data = jserial.user_instance_serialize(user_instance=user_ui_model)
        # token = service_manager.generate_token(user=user, password=password)
        # data = jserial.jwt_cookie_serialize(serialized_user_data=user_data, auth_token=token)
        # resp = Response(data, status=200, mimetype='application/json')
        resp = Response(data, status=200, mimetype='application/json')
        resp.status_code = 200
        return resp


@app.route('/api/users/search/<queryset>', defaults={'limit': 0}, methods=['GET'])
@app.route('/api/users/search/<queryset>/<limit>', methods=['GET'])
def api_users_search(queryset, limit):
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    words = [word for word in queryset.split(' ')]
    users = []
    for word in words:
        results = service_manager.search_user(first_name=word, last_name=word, email=word, limit=limit)
        if None is not results:
            map(lambda x: users.append(x) if x.id not in [y.id for y in users] else False, results)
            users = sorted(users, key=lambda x: x.id)
    if None is users or 1 > len(users):
        message = {
            'status': 404,
            'message': 'Not Found - user you are searching for is not registered'
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        ui_models = [service_manager.get_user_ui_model(u) for u in users]
        data = jserial.user_instances_serialize(user_list=ui_models)
        print('From server - users search - users returned: %s' % data)
        resp = jsonify(data)  # list of users - so jsonify iterates over list
        resp.status_code = 200
        return resp


@app.route('/api/users/tag/search/<tag_id>', methods=['GET'])
def api_user_tag_search(tag_id):
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    result = service_manager.search_user(tag_id=tag_id)
    if None is result:
        message = {
            'status': 404,
            'message': 'Not found - user you are searching for is not registered'
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        user = service_manager.get_user_ui_model(result)
        data = jserial.user_instance_serialize(user_instance=user)
        # resp = jsonify(data)
        resp = Response(data, status=200, mimetype='application/json')
        resp.status_code = 200
        return resp


@app.route('/api/user/get/<int:user_id>', methods=['GET'])
def api_user_get(user_id):
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    user_data = service_manager.search_user(user_id=user_id, exclusive=True)
    if None is user_data:
        message = {
            'status': 404,
            'message': 'Not found - user you are searching for is not registered'
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        user = service_manager.get_user_ui_model(user_data)
        data = jserial.user_instance_serialize(user)
        resp = Response(data, status=200, mimetype='application/json')
        resp.status_code = 200
        return resp


@app.route('/api/user/delete/<int:user_id>', methods=['DELETE'])
def api_user_delete(user_id):
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    if service_manager.delete_user(user_id=user_id):
        message = {
            'status': 200,
            'message': 'User deleted'
        }
    else:
        message = {
            'status': 404,
            'message': 'Not found'
        }
    resp = jsonify(message)
    resp.status_code = message['status']
    return resp


@app.route('/api/user/edit', methods=['PUT', 'POST'])
def user_edit():
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    files = request.files
    if 'file' not in files:
        file = None
    else:
        file = files['file']
    pic_url, pic_id = service_manager.upload_image(file)
    user_dict = jserial.json_deserialize(request.form['user_json'])
    user_dict = jserial.create_user_dict(user_dict, pic_id)
    user = jserial.user_instance_deserialize(user_dict)
    user = service_manager.update_user(user_id=user.id,
                                       tag_id=user.tag_id,
                                       first_name=user.first_name,
                                       last_name=user.last_name,
                                       email=user.email,
                                       role_id=user.role_id,
                                       pic_id=user.pic_id)
    if None is user or -1 == user.id:
        message = {
            'status': 404,
            'message': 'Not Found'
        }
        resp = jsonify(message)
        resp.status_code = message['status']
    else:
        data = jserial.user_instance_serialize(user_instance=user)
        resp = Response(data, status=200, mimetype='application/json')
        resp.status_code = 200
    return resp


    # </editor-fold>
