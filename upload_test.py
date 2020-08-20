import config
from core.s3_api import S3Client
from core.models import Project

s3_config = config.S3Config()

s3_client = S3Client(s3_config)

filename = 'requirements.txt'
s3_client.mp_upload(target_path='test/'+filename, source_path='./'+filename)
