import boto3
import os
from dotenv import load_dotenv
from time import time

load_dotenv()
AWS_CREDENTIAL_FILE = os.getenv("AWS_CREDENTIAL_FILE")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET")


class AmazonWebService:
    def __init__(self, aws_credential_path=AWS_CREDENTIAL_FILE, bucket_name=AWS_BUCKET_NAME):
        """
        함수를 실행하기 전에 terminal에서 vault-login, vault-auth 를 먼저 진행해줘서 키를 발급해야 된다.
        자세한 내용은 https://42dot.atlassian.net/wiki/spaces/sec/pages/852197381/AWS 참고
        """
        self.aws_credential_path = aws_credential_path
        self.aws_credential = {}
        self.bucket_name = bucket_name
        self._get_aws_credential_key()
        self.client = boto3.client('s3', **self.aws_credential)
        self.s3 = boto3.resource('s3', **self.aws_credential)
        self.bucket = self.s3.Bucket(self.bucket_name)

    def _get_aws_credential_key(self):
        """
        aws common 계정에 접근하기 위해서는 shell에서 vault-auth로 키를 만들어야 한다.
        키는 AWS_CREDENTIAL_FILE 위치에 생겨서, 해당 키를 읽고 credential에 접근한다.
        """
        with open(self.aws_credential_path, 'r') as file:
            for line in file.read().split('\n'):
                if line in ("[default]", ""):
                    continue
                key, value = line.split(' = ')
                if value[0] == '"':
                    value = value[1:-1]
                self.aws_credential.update({key: value})

    def s3_list_objects(self, prefix='', delimiter='', should_contain=None, should_delete=None):
        paginator = self.client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=self.bucket_name,
                                   Prefix=prefix,
                                   Delimiter=delimiter)
        try:
            object_list = [obj for page in pages for obj in page['Contents']]
        except KeyError:
            return []
        if should_contain is not None:
            object_list = [obj for obj in object_list if any([word in obj['Key'] for word in should_contain])]
        if should_delete is not None:
            object_list = [obj for obj in object_list if not any([word in obj['Key'] for word in should_delete])]
        object_name_list = [obj['Key'] for obj in object_list]
        return object_name_list

    def s3_upload_object(self, from_path, key, bucket=''):
        if not bucket:
            bucket = self.bucket_name
        self.s3.meta.client.upload_file(from_path, bucket, key)

    def s3_upload_objects(self, upload_files, keys, bucket=''):
        if not bucket:
            bucket = self.bucket_name
        t = time()
        assert len(upload_files) == len(keys), "upload_files, keys length should be same"
        length = len(upload_files)
        for i, (from_path, to_path) in enumerate(zip(upload_files, keys)):
            self.s3_upload_object(from_path, to_path, bucket)
            if not i % (length//10) or i == length-1:
                print(f"{i} 번째 uploaded :: {time() - t}")

    def create_presigned_url(self, object_name, expiration=3600):
        response = self.client.generate_presigned_url('get_object',
                                                      Params={'Bucket': self.bucket_name,
                                                              'Key': object_name},
                                                      ExpiresIn=expiration)
        return response  # url string

    def get_object(self, key):
        return self.client.get_object(Bucket=self.bucket_name, Key=key)
