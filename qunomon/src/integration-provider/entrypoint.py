# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import os
from flask_script import Manager, Shell, Server

from qai_testbed_integration_provider import create_app


if 'CONTAINER_DEBUG_FLAG' in os.environ:
    try:
        import ptvsd
        ptvsd_port = 5679
        ptvsd.enable_attach(address=('0.0.0.0', ptvsd_port))
        ptvsd.wait_for_attach()
    except:
        pass

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


manager = Manager(app)


# run the app
manager.add_command(
    "startserver",
    Server(port=(os.getenv('FLASK_PORT') or 6000), host='0.0.0.0'))

if __name__ == '__main__':
    manager.run()
