# *********** keys ***********

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


# <editor-fold desc="Keys Views">


@app.route('/api/keys', methods=['GET'])
def api_keys_get():
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    keys = service_manager.get_keys()
    if None is keys or 1 > len(keys):
        message = {
            'status': 404,
            'message': 'Not Found' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        data = jserial.key_instances_serialize(key_list=keys)
        resp = jsonify(data)  # list of keys - jsonify iterates over list
        resp.status_code = 200
        return resp


@app.route('/api/keys/register', methods=['POST'])
def api_key_register():
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    key = jserial.key_instance_deserialize(request.get_json())
    key = service_manager.create_key(tag_id=key.tag_id,
                                     room_id=key.room_id,
                                     block_name=key.block_name,
                                     sector_name=key.sector_name,
                                     floor=key.floor,
                                     room_repr=key.room_repr)
    if None is key or -1 == key.id:
        message = {
            'status': 404,
            'message': 'Not Found - unable to save the key',
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        data = jserial.key_instance_serialize(key_instance=key)
        resp = Response(data, status=200, mimetype='application/json')
        resp.status_code = 200
        return resp


@app.route('/api/keys/search/<queryset>', methods=['GET'])
def api_keys_search(queryset):
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    words = [word for word in queryset.split(' ')]
    keys = []
    for word in words:
        pattern = int(word) if word.isdigit() else word
        print('From server - keys search - keys count: %s' % len(keys))
        results = service_manager.search_key(room_id=pattern,
                                             room_repr=pattern,
                                             block_name=pattern,
                                             sector_name=pattern,
                                             floor=pattern, limit=0)
        if None is not results:
            for key in results:
                if None is not key:
                    if key.id not in [y.id for y in keys]:
                        keys.append(key)
                        print('From server - keys search - key found: %s' % key.room_id)
    if None is keys or 1 > len(keys):
        message = {
            'status': 404,
            'message': 'Not Found' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        data = jserial.key_instances_serialize(key_list=keys)
        resp = jsonify(data)  # list of keys - jsonfiy iterates over list
        resp.status_code = 200
        return resp


@app.route('/api/keys/tag/search/<tag_id>', methods=['GET'])
def api_key_tag_search(tag_id):
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    key = service_manager.search_key(tag_id=int(tag_id))
    if None is key:
        message = {
            'status': 404,
            'message': 'Not Found' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        data = jserial.key_instance_serialize(key_instance=key)
        resp = Response(data, status=200, mimetype='application/json')
        resp.status_code = 200
        return resp


@app.route('/api/key/get/<int:key_id>', methods=['GET'])
def api_key_get(key_id):
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    key_data = service_manager.search_key(key_id=key_id, exclusive=True)
    if None is key_data:
        message = {
            'status': 404,
            'message': 'Not Found' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        data = jserial.key_instance_serialize(key_data)
        resp = Response(data, status=200, mimetype='application/json')
        resp.status_code = 200
        return resp


@app.route('/api/key/delete/<int:key_id>', methods=['DELETE'])
def api_key_delete(key_id):
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    if service_manager.delete_key(key_id=key_id):
        message = {
            'status': 200,
            'message': 'Key deleted'
        }
    else:
        message = {
            'status': 404,
            'message': 'Not found'
        }
    resp = jsonify(message)
    resp.status_code = message['status']
    return resp


@app.route('/api/key/edit', methods=['PUT', 'POST'])
def key_edit():
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    key = jserial.key_instance_deserialize(request.get_json())
    key = service_manager.update_key(key_id=key.id,
                                     tag_id=key.tag_id,
                                     room_id=key.room_id,
                                     block_name=key.block_name,
                                     sector_name=key.sector_name,
                                     floor=key.floor,
                                     room_repr=key.room_repr)
    if None is key or -1 == key.id:
        message = {
            'status': 404,
            'message': 'Not found - Unable to edit key data',
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        data = jserial.key_instance_serialize(key_instance=key)
        resp = Response(data, status=200, mimetype='application/json')
        resp.status_code = 200
        return resp


# </editor-fold>
