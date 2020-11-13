from sqlalchemy import table, select, literal_column
from sqlalchemy.orm import sessionmaker

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import ResourceCollector as ResColl

# ResourceCollectorの動きチェック用にお使いください。
# qai-testbed/src/storage/docker-compose.yml のdbとの連携できるようになっています。
def main():
    app = Flask('use_only_for_development')
    SQLALCHEMY = {
        'SQLALCHEMY_DATABASE_URI': "postgresql://user:pass@localhost:5432/qai",
        'SQLALCHEMY_BINDS': {},
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ECHO': True
    }
    all_config_vars = dict(
        list(SQLALCHEMY.items())
    )
    for key, value in all_config_vars.items():
        app.config[key] = value
    db = SQLAlchemy()
    db.init_app(app)
    with app.app_context():
        db.create_all()
        rc = ResColl.ResourceCollector()
        # rc.実行したい関数(db, 〇〇, 〇〇)

main()
