# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import os

from qai_testbed_backend.across.create_app import create_app, init_guideline
from distutils.util import strtobool

if 'CONTAINER_DEBUG_FLAG' in os.environ:
    try:
        import ptvsd
        ptvsd_port = 5678
        ptvsd.enable_attach(address=('0.0.0.0', ptvsd_port))
        ptvsd.wait_for_attach()
    except:
        pass


app = create_app(os.getenv('FLASK_CONFIG') or 'default',
                 is_init_db=bool(strtobool(os.getenv('QAI_TB_INIT_DB', default='True'))))

# guideline
init_guideline(app)


if __name__ == '__main__':
    app.run(port=(os.getenv('FLASK_PORT') or 5000), host='0.0.0.0', threaded=False)
