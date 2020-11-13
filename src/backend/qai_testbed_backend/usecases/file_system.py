# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from ..controllers.dto import Result
from ..controllers.dto.file_system import GetFileSystemsRes
from ..entities.file_system import FileSystemMapper


class FileSystemService:
    def get_file_system(self) -> GetFileSystemsRes:
        file_systems = FileSystemMapper.query.all()

        return GetFileSystemsRes(
            result=Result(code='I92000', message="get list success."),
            file_systems=[f.to_dto() for f in file_systems]
        )
