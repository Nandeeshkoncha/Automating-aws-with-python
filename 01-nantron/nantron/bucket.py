# -*- coding: utf-8 -*-

""" Classes for s3 Buckets."""

class BucketManager:
    """ Manage s3 bucket"""

    def __init__(self,session):
        """ create a BucketManager object."""
        self.s3 = session.resource('s3')

    def list_buckets(self):
        """ list buckets """
        return self.s3.buckets.all()

    def list_bucket_objects(self,bucket):
        """ list bucket objects """
        return self.s3.Bucket(bucket).objects.all()
        
