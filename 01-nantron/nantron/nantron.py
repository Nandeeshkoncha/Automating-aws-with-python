#!/usr/bin/pthon

# -*- Coding: utf-8 -*-

"""Nantron: Deploy websites with aws."""

from pathlib import Path
import mimetypes
import boto3
import click
from botocore.exceptions import ClientError
from bucket import BucketManager


session = boto3.Session(profile_name='DNS_PythonAutomation')
bucket_manager = BucketManager(session)


@click.group()
def cli():
    """Nantron will deploy website to AWS."""
    pass


@cli.command('list-buckets')
def list_buckets():
    """List buckets of s3 bucket."""
    for buc in bucket_manager.list_buckets():
        print(buc.name)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List bucket objects."""
    for obj in bucket_manager.list_bucket_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucketname')
def setup_bucket(bucketname):
    """Create new s3 bucket."""
    s3_bucket = None
    try:
        s3_bucket = s3.create_bucket(Bucket=bucketname, CreateBucketConfiguration={'LocationConstraint': session.region_name})
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucketname)
            print(s3_bucket)
        else:
            raise e
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
     }""" % s3_bucket.name

    policy = policy.strip()
    pol = s3_bucket.Policy()
    pol.put(Policy=policy)
    bucket_website = s3_bucket.Website()
    bucket_website.put(WebsiteConfiguration={'ErrorDocument': {'Key': 'error.html'}, 'IndexDocument': {'Suffix': 'index.html'}})
    return


def upload_file(s3_bucket, path, key):
    """It is to upload file."""
    content_type = mimetypes.guess_type(key)[0] or 'text/plain'
    s3_bucket.upload_file(path, key, ExtraArgs={'ContentType': content_type})


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync directory."""
    s3_bucket = s3.Bucket(bucket)
    root = Path(pathname).expanduser().resolve()
    "this is to remove tilda's"
    def handle_dir(target):
        for p in target.iterdir():
            if p.is_dir():
                handle_dir(p)
            if p.is_file():
                upload_file(s3_bucket, str(p), str(p.relative_to(root)))
    handle_dir(root)


if __name__ == '__main__':
    cli()
