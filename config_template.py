# Rename this file to config.py and add the values

from pydantic import BaseSettings


class S3Config(BaseSettings):
    BUCKET_NAME: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
