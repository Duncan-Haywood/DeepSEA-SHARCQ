from wildroot_aws_util.aws_util import AWSUtil
import shutil
from logging import Logger
import os
import concurrent
import psutil


class Unzip:
    def __init__(self):
        self.aws_util = AWSUtil()
        self.download_path = "/tmp/download"
        self.unzipped_path = "/tmp/unzipped"
        self.logger = Logger(__name__)

    def main(self, event):
        self.download(event)
        self.unzip()
        self.concurrent_upload()

    def concurrent_upload(self):
        def _upload(file):
            """upload logic to be run concurrrently."""
            file_key = f"{self.key}/file"
            file_path = f"{self.unzipped_path}/{file}"
            self.aws_util.upload_s3_object(self.bucket_name, file_key, file_path)

        # files to upload
        files = os.listdir(self.unzipped_path)
        # run the uploads concurrently
        cpu_count = psutil.cpu_count()
        thread_count = cpu_count * 3
        with concurrent.futures.ThreadPoolExecutor(thread_count) as executor:
            futures = [executor.submit(_upload, file) for file in files]
            concurrent.futures.wait(futures)

    def download(self, event):
        (
            self.bucket_name,
            self.key,
        ) = self.aws_util.get_s3_object_info_from_event_message(event)
        self.aws_util.download_s3_object(self.bucket_name, self.key, self.download_path)

    def unzip(self):
        try:
            shutil.unpack_archive(self.download_path, self.unzipped_path)
        except ValueError as e:
            self.logger.exception("unzipping failed: possibly wrong zip type")
            # TODO set up notification to frontend of the error
            raise e
        else:
            pass


def lambda_handler(event, context):
    Unzip().main(event)
