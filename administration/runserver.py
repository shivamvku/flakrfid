from src import app

if __name__ == '__main__':
    if app.debug == 0:
        app.run(host='172.23.24.149', port=8080, debug=False)
    else:
        app.run(host='127.0.0.1', port=5200, debug=True)
