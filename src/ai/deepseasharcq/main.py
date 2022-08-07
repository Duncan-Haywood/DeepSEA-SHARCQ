import argparse
import logging
from wildroot_aws_util.aws_util import AWSUtil


class DeepSeaSharcq:
    def __init__(self):
        return NotImplementedError

    def predict(self, data_path: str, result_path: str):
        return NotImplementedError

    def train(self, data_path: str):
        return NotImplementedError

    def evaluate(self, data_path: str):
        return NotImplementedError


def main():
    result_path = "./results"
    # handle arguments from command line
    my_parser = argparse.ArgumentParser(description="cli for deepseasharcq")
    my_parser.add_argument(
        "ai_action", type=str, help="experiment or train or evaluate"
    )
    my_parser.add_argument("path", help="path to data to use", type=str)
    args = my_parser.parse_args()

    # run ai program
    dss = DeepSeaSharcq()
    if args.ai_action == "train":
        dss.train(args.path)
    elif args.ai_action == "predict":
        dss.predict(args.path)
    else:
        logging.error(
            'invalid ai_action input: choose "train" or "predict" and provide "path" for data to use'
        )


def lambda_handler(event, context):
    # download file
    download_path = "/tmp/predict_file"
    results_path = "/tmp/predict_result"
    aws_util = AWSUtil()
    bucket_name, key = aws_util.get_s3_object_info_from_event_message(event)
    aws_util.download_s3_object(bucket_name, key, download_path)
    # run ai
    DeepSeaSharcq().predict(download_path, results_path)
    aws_util.upload_s3_object(bucket_name, key, results_path)
    return None


if __name__ == "__main__":
    main()
