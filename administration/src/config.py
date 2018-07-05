import os

DEBUG_MODE = 0 if not os.environ.has_key('FLASK_DEBUG') else int(os.environ['FLASK_DEBUG'])

DATA_DIR_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')

UPLOAD_URI = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images')

TEST_DATABASE_URI = os.path.join(DATA_DIR_PATH, 'test-db.sqlite')
DEV_DATABASE_URI = os.path.join(DATA_DIR_PATH, 'dev-db.sqlite')
PROD_DATABASE_URI = os.path.join(DATA_DIR_PATH, 'rfid-db.sqlite')

if DEBUG_MODE == 1:
    DATABASE_URI = DEV_DATABASE_URI
elif DEBUG_MODE == 2:
    DATABASE_URI = TEST_DATABASE_URI
else:
    # DATABASE_URI = PROD_DATABASE_URI
    DATABASE_URI = TEST_DATABASE_URI

DATA_EXCEL_PATH = os.path.join(DATA_DIR_PATH, 'seed_data')

SECRET_KEY = os.environ['SECRET_KEY'] if os.environ.has_key('SECRET_KEY') else 'the_secret_key'
