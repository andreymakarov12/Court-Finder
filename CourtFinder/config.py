import os


class Config:

    SECRET_KEY = '1' #os.urandom(12)

    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')

    # Connection to Postgres server
    SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASS + '@192.155.88.112:3306/courtfinder'

    # Gets pwd and declares it is the root dir for the App
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    #  boto3 Keys for Object Storage
    BOTO_KEY = os.environ.get('BOTO_KEY')
    BOTO_SECRET = os.environ.get('BOTO_SECRET')

    # To suppress FSADeprecationWarning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
