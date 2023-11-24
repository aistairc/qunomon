# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from . import development, development_docker, development_aws, testing, production


def set_app_config_keys(app, settings):
    """Load all flask.Flask config vars.

    :app: a flask.Flask object
    :settings: a module with config vars
    :returns: None

    """
    # create a unique dict with all config vars
    all_config_vars = dict(
        list(settings.SQLALCHEMY.items()) +
        list(settings.FLASK_VARS.items()) +
        list(settings.FLASK_JWT_VARS.items()) +
        list(settings.DB_CONNECTION.items()) +
        list(settings.PASSLIB.items())
    )

    for key, value in all_config_vars.items():
        app.config[key] = value


def development_config(app):
    """Call the function responsable by load config vars
    using 'development' settings.

    :app: a flask.Flask object
    :returns: None

    """
    set_app_config_keys(app, development)

def development_docker_config(app):
    """Call the function responsable by load config vars
    using 'development_docker' settings.

    :app: a flask.Flask object
    :returns: None

    """
    set_app_config_keys(app, development_docker)

def development_aws_config(app):
    """Call the function responsable by load config vars
    using 'development_aws' settings.

    :app: a flask.Flask object
    :returns: None

    """
    set_app_config_keys(app, development_aws)


def testing_config(app):
    """Call the function responsable by load config vars
    using 'testing' settings.

    :app: a flask.Flask object
    :returns: None

    """
    set_app_config_keys(app, testing)


def production_config(app):
    """Call the function responsable by load config vars
    using 'production' settings.

    :app: a flask.Flask object
    :returns: None

    """
    set_app_config_keys(app, production)

# Yep, I know I could use lambdas...
config = {
    'development': development_config,
    'development_docker': development_docker_config,
    'development_aws': development_aws_config,
    'testing': testing_config,
    'production': production_config,
    'default': development_config,
}



def development_db_common():
    return development.db_common
def development_docker_db_common():
    return development_docker.db_common
def development_aws_db_common():
    return development_aws.db_common
def testing_db_common():
    return testing.db_common
def production_db_common():
    return production.db_common

db_common = {
    'development': development_db_common(),
    'development_docker': development_docker_db_common(),
    'development_aws': development_aws_db_common(),
    'testing': testing_db_common(),
    'production': production_db_common(),
    'default': development_db_common(),
}