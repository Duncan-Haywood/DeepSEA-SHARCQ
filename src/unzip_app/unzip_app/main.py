from api.deepseasharcqapi import aws_util


class UnzipApp:
    def __init__(self):
        self.aws_util = AWSUtil()
        
    def main(self):
        zip_name = self.aws_util.read_sqs()
        zip_folder = self.aws_util.download_s3(zip_name)
        folder = gzip.unzip(zip_folder)
        for file in folder: 
            with open(file) as f:
                self.aws_util.upload_s3(f)

def main():
    UnzipApp().main()

if __name__=='__main__':
    main()

