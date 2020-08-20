import logging
import threading
import boto3
import os
import sys
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig
from typing import Dict

logger = logging.getLogger(__name__)


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


class S3Client:
    """ S3 Client

    """
    def __init__(self, config):
        self.bucket_name = config.BUCKET_NAME
        session = boto3.Session(
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        )
        self.s3 = session.resource('s3')
        if self.s3.Bucket(self.bucket_name).creation_date:
            pass
        else:
            logger.error(Exception('S3 Bucket *' + self.bucket_name + '* not found'))
            raise Exception('S3 Bucket *' + self.bucket_name + '* not found')

        self.mp_config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10,
                                        multipart_chunksize=1024 * 25, use_threads=True)

    def upload(self, target_path: str, source_path: str, metadata: Dict[str]):
        try:
            self.s3.meta.client.upload_file(source_path, self.bucket_name, target_path,
                                            ExtraArgs={"Metadata": metadata})
            logger.info("Upload of {} to {} complete".format(source_path, target_path))
        except ClientError as e:
            logging.error(e)

    def mp_upload(self, target_path: str, source_path: str, metadata: Dict[str]):
        try:
            self.s3.meta.client.upload_file(source_path, self.bucket_name, target_path,
                                            Config=self.mp_config,
                                            Callback=ProgressPercentage(source_path),
                                            ExtraArgs={"Metadata": metadata},
                                            )
            logger.info("Upload of {} to {} complete".format(source_path, target_path))
        except ClientError as e:
            logger.error(e)

    def download(self, source_path: str, target_path: str = '.'):
        pass

    def list(self, key: str):
        pass






