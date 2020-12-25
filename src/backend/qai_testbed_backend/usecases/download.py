# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask import make_response
from pathlib import Path
import mimetypes
from qlib.utils.logging import get_logger, log

from ..entities.dowmload import DownloadMapper
from ..across.exception import QAINotFoundException


logger = get_logger()


class DownloadService:
    @log(logger)
    def get(self, id_: int):
        dl = DownloadMapper.query.get(id_)
        if dl is None:
            raise QAINotFoundException('D16000', 'not found download')

        response = make_response()
        response.data = open(dl.path, "rb").read()

        path = Path(dl.path)
        response.headers['Content-Disposition'] = 'attachment; filename=' + path.name

        # MIME設定
        mime_type = mimetypes.guess_type(dl.path)[0]
        if mime_type is None:
            my_mime = {'.log': 'text/plain'}
            if path.suffix in my_mime:
                response.mime_type = my_mime[path.suffix]
            else:
                response.mime_type = 'application/octet-stream'
        else:
            response.mime_type = mime_type

        return response
