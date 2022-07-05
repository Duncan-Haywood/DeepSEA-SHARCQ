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
        self.bucket_name = os.get_environ('S3_BUCKET')
        self.s3_bucket = self.s3.Bucket(self.bucket_name)
        self.ecs = boto3.resource('ecs')

    def s3_upload_files(self, files: List[UploadFile]):
        """Uploads all 'files' to s3 environent ' S3_BUCKET' in the uploads folder with class's 'folder_path' as subfolder. Intended for initial upload of files directly from fastapi. Might be refactored for more general use later. """
        # action to take in parallel 
        def _upload_file(file, key):
            with open(file.file) as f:
                key = f'{self.folder_path}/{file.filename}'
                # below should implement parallel multipart upload in theory
                self.s3_bucket.upload_fileobj(f,key)
        # runs file uploads in parallel across all cpus - TODO hopefully it doesn't overtax the RAM (10 GB max on lambda instances) (jobs should be about 6 at max on lambda)
        Parallel(n_jobs=-1)(delayed(_upload_file)(file) for file in files)
            
    def launch_ai_ecs(self):    
        return NotImplementedError
    def exec_predict_ecs(self):
        return NotImplementedError
    def close_ai_ecs(self):
        return NotImplementedError
    def s3_send_results(self):
        return NotImplementedError

class BucketWrapper:
    def __init__(self, bucket):
        self.bucket = bucket
        self.name = bucket.name

    def generate_presigned_post(self, object_key, expires_in):
        """
        Generate a presigned Amazon S3 POST request to upload a file.
        A presigned POST can be used for a limited time to let someone without an AWS
        account upload a file to a bucket.

        :param object_key: The object key to identify the uploaded object.
        :param expires_in: The number of seconds the presigned POST is valid.
        :return: A dictionary that contains the URL and form fields that contain
                 required access data.
        """
        try:
            response = self.bucket.meta.client.generate_presigned_post(
                Bucket=self.bucket.name, Key=object_key, ExpiresIn=expires_in)
            logger.info("Got presigned POST URL: %s", response['url'])
        except ClientError:
            logger.exception(
                "Couldn't get a presigned POST URL for bucket '%s' and object '%s'",
                self.bucket.name, object_key)
            raise
        return response

