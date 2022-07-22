from fastapi import UploadFile
from typing import List
import boto3
import os
from joblib import Parallel, delayed
import logging

class AWSUtil:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.s3 = boto3.resource('s3')
        self.bucket_name = os.get_environ('OUTPUT_BUCKET_NAME')
        self.s3_bucket = self.s3.Bucket(self.bucket_name)

    def s3_upload_files(self, files: List[UploadFile]):
        """Uploads all 'files' to s3 environent ' S3_BUCKET' in the uploads folder with class's 'folder_path' as subfolder. Intended for initial upload of files directly from fastapi. Might be refactored for more general use later. """
        # action to take in parallel 
        def _upload_file(file: UploadFile):
            with open(file.file) as f:
                key = f'{self.folder_path}/{file.filename}'
                # below should implement parallel multipart upload in theory
                self.s3_bucket.upload_fileobj(f,key)
        # runs file uploads in parallel across all cpus
        Parallel(n_jobs=-1)(delayed(_upload_file)(file) for file in files)

    def upload_s3_file(self, file: UploadFile):
        with open(file.file) as f:
            key = f'{self.folder_path}/{file.filename}'
            self.s3_bucket.upload_fileobj(f,key)
