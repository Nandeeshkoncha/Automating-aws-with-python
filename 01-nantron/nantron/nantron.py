#!/usr/bin/pthon

# -*- Coding: utf-8 -*-

"""Nantron: Deploy websites with aws."""


import boto3
import click
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
    s3_bucket = bucket_manager.init_bucket(bucketname)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)
    return





@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """ Sync contents to s3 bucket."""
    bucket_manager.sync(pathname, bucket)


if __name__ == '__main__':
    cli()
