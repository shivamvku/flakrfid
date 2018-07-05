# *********** auth ***********

from . import (
    app,
    service_manager,
    jsonify,
    request,
    Response,
    StorageManager
)
from .auth_views import (
    verify_token,
    get_request_auth
)
from .core_views import send_file


# *********** file storage ***********
# <editor-fold desc="File storage Views">

@app.route('/api/data/template', methods=['GET'])
def api_data_template():
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    file = service_manager.get_excel_template()
    return send_file(file, mimetype='text/csv', attachment_filename='data_template.xls', as_attachment=True)


@app.route('/api/data/import', methods=['POST'])
def api_data_import():
    auth_data = get_request_auth(request=request)
    if auth_data[0] == '0':
        return jsonify(auth_data[1:])
    if not verify_token(auth_data[1:]):
        return Response('Login required', status=404, mimetype='application/json')
    file = None
    files = request.files
    if 'file' in files:
        file = files['file']
    stm = StorageManager()
    file_path = stm.store_file(file=file, type=0)
    check_location = service_manager.get_excel_template(filename=file.filename)
    results = service_manager.seed_from_excel(file_location=file_path)
    if None is results:
        message = {
            'status': 404,
            'message': 'Unable to import data'
        }
    else:
        message = {
            'status': 200,
            'message': 'Successfully updated the database!'
        }
    resp = jsonify(message)
    resp.status_code = message['status']
    return resp

# </editor-fold>
