import boto3
import json
from logging import Logger

class AWSUtil:
    def __init__(self) -> None:
        self.s3 = boto3.resource("s3")
        self.logger = Logger(__name__)
        self.s3_client = self.s3.Client()
    
    def get_s3_object_info_from_event_message(self, message):
        """return bucket name and key from parsed s3 json event message"""
        dict_message = json.loads(message)
        s3_info = dict_message["Records"][0]["s3"]
        bucket_name = s3_info["bucket"]["name"]
        key = s3_info["object"]["key"]
        return bucket_name, key
    
    def download_s3_object(self, bucket_name: str, key: str, download_path: str):
        """download fileobject at key in s3 bucket denoted by bcket name to destination path"""
        bucket = self.s3.Bucket(bucket_name)
        with open(download_path, 'wb') as file:
            bucket.download_fileobj(key, file)

    def upload_s3_object(self, bucket_name: str, key: str, file_path: str):
        """upload file from file_path to s3 bucket: bucket_name at key location."""
        bucket = self.s3.Bucket(bucket_name)
        with open(file_path, 'rb') as fileobj:
            bucket.upload_fileobj(fileobj, key)

    def generate_presigned_url(self, client_method, method_parameters, expires_in):
        """
        Generate a presigned Amazon S3 URL that can be used to perform an action.

        :param s3_client: A Boto3 Amazon S3 client.
        :param client_method: The name of the client method that the URL performs.
        :param method_parameters: The parameters of the specified client method.
        :param expires_in: The number of seconds the presigned URL is valid for.
        :return: The presigned URL.
        """
        try:
            url = self.s3_client.generate_presigned_url(
                ClientMethod=client_method,
                Params=method_parameters,
                ExpiresIn=expires_in
            )
            self.logger.info("Got presigned URL: %s", url)
        except ClientError:
            self.logger.exception(
                "Couldn't get a presigned URL for client method '%s'.", client_method)
            raise
        return url