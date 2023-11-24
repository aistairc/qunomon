# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime


SQLALCHEMY = {
    # 'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:",
    'SQLALCHEMY_DATABASE_URI': "postgresql://user:pass@localhost:5432/qai",
    'SQLALCHEMY_BINDS': {},
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_ECHO': True
}

# database connection data
DB_CONNECTION = {
    "MONGODB_DB": "development",
    "MONGODB_USERNAME": "",
    "MONGODB_PASSWORD": "",
    "MONGODB_HOST": "localhost",
    "MONGODB_PORT": 27017
}

# database uri
DATABASE_URI = ''

# flask vars
FLASK_VARS = {
    'DEBUG': True,
    'SECRET_KEY': 'aReallySecretKey',
    'JSON_AS_ASCII': False,
    'RESTFUL_JSON': {'ensure_ascii': False}
}

# flask-jwt vars
FLASK_JWT_VARS = {
    'JWT_AUTH_URL_RULE': '/api/auth',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1)
}

# another third party libs...
PASSLIB = {
    'HASH_ALGORITHM': 'SHA512',
    'HASH_SALT': 'HiMyNameIsGoku',
}
