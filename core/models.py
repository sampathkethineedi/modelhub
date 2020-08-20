from typing import List, Dict, Tuple
from .s3_api import S3Client


class BaseModel:
    def __init__(self, s3_client: S3Client, name: str, author: str,
                 family: str = 'default', tags: List[str] = None):

        self.name = name
        self.author = author
        if tags:
            self.tags = tags
        else:
            self.tags = []
        self.family = family

        self.s3_client = s3_client

        self.metadata: Dict = {}
        self.target_path: str = ''

    def ready_upload(self) -> Tuple:
        metadata = {
            "tags": self.tags,
            "family": self.family
        }
        target_path = '/'.join([self.author, self.name])

        return metadata, target_path

    def upload(self, file_path: str, multi_part: bool = True):
        metadata, target_path = self.ready_upload()

        if multi_part:
            self.s3_client.mp_upload(source_path=file_path, target_path=target_path, metadata=metadata)
        else:
            self.s3_client.upload(source_path=file_path, target_path=target_path, metadata=metadata)

    def download(self):
        pass


class Project(BaseModel):
    def __init__(self, s3_client: S3Client, name: str, author: str, project: str,
                 family: str = 'default', tags: List[str] = None):
        super().__init__(s3_client, name, author)
        self.project = project