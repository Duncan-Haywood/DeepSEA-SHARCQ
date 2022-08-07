import boto3
import json
from logging import Logger
import os
from typing import List


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

    def is_two_folders_contain_same_files_s3(
        self, bucket_name1, folder_name1, bucket_name2, folder_name2
    ) -> bool:
        """Returns if folder1 of bucket1 has the same files as folder2 of bucket2"""
        response1 = self.s3_client.list_objects_v2(
            Bucket=bucket_name1, Prefix=folder_name1
        )
        response2 = self.s3_client.list_objects_v2(
            Bucket=bucket_name2, Prefix=folder_name2
        )
        # creates lists of all the file names
        file_names1 = [obj["Key"] for obj in response1["Contents"]]
        file_names2 = [obj["Key"] for obj in response2["Contents"]]
        is_same_contents = file_names1.sort() == file_names2.sort()
        return is_same_contents

    def download_s3_object(self, bucket_name: str, key: str, download_path: str):
        """download fileobject at key in s3 bucket denoted by bcket name to destination path"""
        bucket = self.s3.Bucket(bucket_name)
        with open(download_path, "wb") as file:
            bucket.download_fileobj(key, file)

    def list_files_s3(self, bucket_name: str, dir_name: str) -> List[str]:
        """returns a list of keys in s3 bucket and folder."""

        response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=dir_name)
        contents = response["Contents"]
        keys = [obj["Key"] for obj in contents]

        return keys

    def upload_s3_object(self, bucket_name: str, key: str, file_path: str):
        """upload file from file_path to s3 bucket: bucket_name at key location."""
        bucket = self.s3.Bucket(bucket_name)
        with open(file_path, "rb") as fileobj:
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
                ExpiresIn=expires_in,
            )
            self.logger.info("Got presigned URL: %s", url)
        except ClientError:
            self.logger.exception(
                "Couldn't get a presigned URL for client method '%s'.", client_method
            )
            raise
        return url
