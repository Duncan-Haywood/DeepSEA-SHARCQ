from aws_util.wildroot_aws_util.aws_util import AWSUtil
import os
from logging import Logger
import concurrent.futures
import psutil
import shutil


class Zip:
    def __init__(self) -> None:
        self.aws_util = AWSUtil()
        self.logger = Logger(__name__)
        self.unzipped_files_bucket_name = os.get_environ("UNZIPPED_FILES_BUCKET")
        self.dir_name = None
        self.unzipped_results_bucket_name = os.get_environ("UNZIPPED_RESULTS_BUCKET")
        self.output_bucket_name = os.get_environ("ZIPPED_RESULTS_BUCKET")
        self.unzipped_files_path = "/tmp/unzipped_files"
        self.zipped_folder_path = "/tmp/zipped_folder"

    def main(self, message):
        """ takes lambda s3n message, checks if all files have been processed from env UNZIPPED_FILES_BUCKET. zips files into folder. uploads folder to env ZIPPED_RESULTS_BUCKET."""
        is_completed = self.is_all_files_processed(message)
        if is_completed:
            self.download_files()
            self.zip_files(self.unzipped_files_path, self.zipped_folder_path)
            self.aws_util.upload_s3_object(
                self.output_bucket_name, self.dir_name, self.zipped_folder_path
            )
        else:
            self.logger.info("not all files have been processed.")

    def zip_files(self, input_folder, output_folder):
        """zips files from input_folder to output_folder."""
        shutil.make_archive(input_folder, "zip", output_folder)

    def download_files(self):
        """downloads files from unzipped results bucket and subfolder to local path unzipped_files variable"""
        os.mkdir(self.unzipped_files_path)
        keys = self.aws_util.list_files_s3(
            self.unzipped_results_bucket_name, self.dir_name
        )
        # helper function for parallel download
        def _download(key):
            try:
                self.aws_util.download_s3_object(self.unzipped_results_bucket_name, key)
            except Exception as e:
                self.logger.exception("file download failed: %s" % key)

        # parallel download
        cpus = psutil.cpu_count()
        max_workers = cpus * 5
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(_download, key) for key in keys]
            concurrent.futures.wait(futures)

    def is_all_files_processed(self, message):
        bucket_name, self.key = self.aws_util.get_s3_object_info_from_event_message(
            message
        )
        self.dir_name = os.path.dirname(self.key)

        is_completed = self.aws_util.is_two_folders_contain_same_files_s3(
            bucket_name, self.dir_name, self.unzipped_files_bucket_name, self.dir_name
        )
        return is_completed


def lambda_handler(event, context):
    Zip().main(event)
