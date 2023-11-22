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
}

# another third party libs...
PASSLIB = {
    'HASH_ALGORITHM': 'SHA512',
}
