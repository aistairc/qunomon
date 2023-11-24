# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

SQLALCHEMY = {
    'SQLALCHEMY_DATABASE_URI': '',
    'SQLALCHEMY_BINDS': {},
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
}

# database connection data
DB_CONNECTION = {
    "MONGODB_DB": "",
    "MONGODB_USERNAME": "",
    "MONGODB_PASSWORD": "",
    "MONGODB_HOST": "",
    "MONGODB_PORT": None
}

# database uri
DATABASE_URI = ''

# flask vars
FLASK_VARS = {
    'SECRET_KEY': '',
}

# flask-jwt vars
FLASK_JWT_VARS = {
    'JWT_AUTH_URL_RULE': '/api/auth',
    'JWT_COOKIE_CSRF_PROTECT': False,
    'JWT_COOKIE_SECURE': False
}

# another third party libs...
PASSLIB = {
    'HASH_ALGORITHM': 'SHA512',
}

db_common = {
    'backend_entry_point': '',
    'ip_entry_point': '',
    'mount_src_path': '',
    'mount_dst_path': '',
    'airflow_entry_point': ''
}