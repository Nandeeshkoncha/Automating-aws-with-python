import boto3
import click

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

if __name__ == '__main__':
    cli()
