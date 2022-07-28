import boto3
import json

class AWSUtil:
    def __init__(self) -> None:
        self.s3 = boto3.resource("s3")
    
    def get_object_info_from_event_message(self, message):
        """return bucket name and key from parsed s3 json event message"""
        dict_message = json.loads(message)
        s3_info = dict_message["Records"][0]["s3"]
        bucket_name = s3_info["bucket"]["name"]
        key = s3_info["object"]["key"]
        return bucket_name, key
    
    def download_s3_object(self, bucket_name: str, key: str, destination_path: str):
        """download fileobject at key in s3 bucket denoted by bcket name to destination path"""
        bucket = self.s3.Bucket(bucket_name)
        with open(destination_path, 'wb') as file:
            bucket.download_fileobj(key, file)

    def upload_s3_object(self, bucket_name: str, key: str, file_path: str):
        """upload file from file_path to s3 bucket: bucket_name at key location."""
        bucket = self.s3.Bucket(bucket_name)
        with open(file_path, 'rb') as fileobj:
            bucket.upload_fileobj(fileobj, key)
