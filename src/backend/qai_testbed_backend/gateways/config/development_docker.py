# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime


SQLALCHEMY = {
    # 'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:",
    'SQLALCHEMY_DATABASE_URI': "postgresql://user:pass@psql:5432/qai",
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

db_common = {
    'backend_entry_point': 'http://127.0.0.1:8888/qai-testbed/api/0.0.1',
    'ip_entry_point': 'http://ip:6000/qai-ip/api/0.0.1',
    'mount_src_path': 'testbed_mount_volume_src',
    'mount_dst_path': '/testbed_mount_volume_dst',
    'airflow_entry_point': 'http://airflow:8080',
    'docker_repository_url': 'registry:5500',
    'airflow_mount_volume_path': '/testbed_mount_volume_dst',
    'report_resource_limit': '20'
}