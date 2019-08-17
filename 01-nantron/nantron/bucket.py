# -*- coding: utf-8 -*-
import mimetypes
from botocore.exceptions import ClientError
from pathlib import Path

"""Classes for s3 Buckets."""

class BucketManager:
    """Manage s3 bucket."""

    def __init__(self,session):
        """Create a BucketManager object."""
        self.session = session
        self.s3 = session.resource('s3')

    def list_buckets(self):
        """List buckets"""
        return self.s3.buckets.all()

    def list_bucket_objects(self,bucket):
        """List bucket objects"""
        return self.s3.Bucket(bucket).objects.all()

    def init_bucket(self,bucket_name):
        s3_bucket = None
        try:
            s3_bucket = self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': self.session.region_name})
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.s3.Bucket(bucket_name)
            else:
                raise e
        return s3_bucket

    def set_policy(self, bucket):
        policy = """
         {
         "Version":"2012-10-17",
          "Statement":[{
          "Sid":"PublicReadGetObject",
          "Effect":"Allow",
          "Principal": "*",
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::%s/*"]
          }]
         }""" % bucket.name
        policy = policy.strip()
        pol = bucket.Policy()
        pol.put(Policy=policy)

    def configure_website(self, bucket):
        bucket.Website().put(WebsiteConfiguration={'ErrorDocument': {'Key': 'error.html'}, 'IndexDocument': {'Suffix': 'index.html'}})
        
    @staticmethod
    def upload_file(bucket, path, key):
        """ static Method because of no need of self."""

        """It is to upload file."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        return bucket.upload_file(path, key, ExtraArgs={'ContentType': content_type})

    def sync(self, pathname, bucket_name):
        """Sync directory."""
        bucket = self.s3.Bucket(bucket_name)

        root = Path(pathname).expanduser().resolve()
        """this is to remove tilda's"""

        def handle_dir(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_dir(p)
                if p.is_file():
                    self.upload_file(bucket, str(p), str(p.relative_to(root)))
        handle_dir(root)
