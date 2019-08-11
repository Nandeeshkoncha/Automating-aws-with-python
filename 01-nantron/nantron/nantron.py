import boto3
import click
from botocore.exceptions import ClientError

session = boto3.Session(profile_name='DNS_PythonAutomation')
s3 = session.resource('s3')

@click.group()
def cli():
    "Nantron will deploy website to AWS"
    pass

@cli.command('list-buckets')
def list_buckets():
    "List buckets of s3 bucket"
    for buc in s3.buckets.all():
        print(buc.name)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    "List bucket objects"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)

@cli.command('setup-bucket')
@click.argument('bucketname')
def setup_bucket(bucketname):
    "Create new s3 bucket"
    s3_bucket = None
    try:
        s3_bucket = s3.create_bucket(Bucket = bucketname, CreateBucketConfiguration={'LocationConstraint': session.region_name})
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
    pol.put(Policy = policy)
    bucket_website = s3_bucket.Website()
    bucket_website.put(WebsiteConfiguration={
             'ErrorDocument': {
                 'Key': 'error.html'
             },
             'IndexDocument': {
                 'Suffix': 'index.html'
             }})
    return

if __name__ == '__main__':
    cli()
