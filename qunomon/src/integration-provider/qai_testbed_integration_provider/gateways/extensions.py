# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_mongoengine import MongoEngine
from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

nosql_db = MongoEngine()
jwt = JWT()
sql_db = SQLAlchemy()
ma = Marshmallow()
