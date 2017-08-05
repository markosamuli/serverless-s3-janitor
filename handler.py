from __future__ import print_function

import json
import boto3
import logging
import os


s3 = boto3.client('s3')

logger = logging.getLogger(__name__)
logger.setLevel('INFO')


def get_s3_buckets_in_region(region):
    """
    Get all available S3 bucket names in the given region.
    """
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        assert isinstance(bucket['Name'], str)
        response = s3.get_bucket_location(
            Bucket=bucket['Name']
        )
        if response['LocationConstraint'] != region:
            continue
        yield bucket['Name']


def janitor(event, context):

    bucket_region = os.environ['BUCKET_REGION']
    target_bucket = os.environ['TARGET_BUCKET']

    logging.info('Checking buckets in %s region' % bucket_region)
    logging.info('Target bucket: %s' % target_bucket)
    for bucket in get_s3_buckets_in_region(bucket_region):
        response = s3.get_bucket_logging(
            Bucket=bucket
        )
        if 'LoggingEnabled' not in response:
            logger.info('Logging not enabled for bucket %s' % bucket)
            target_prefix = 's3/%s/' % bucket
            s3.put_bucket_logging(
                Bucket=bucket,
                BucketLoggingStatus={
                    'LoggingEnabled': {
                        'TargetBucket': target_bucket,
                        'TargetPrefix': target_prefix,
                    }
                },

            )
            logger.info('Enabled logging for S3 bucket %s' % bucket)
        response = s3.get_bucket_versioning(
            Bucket=bucket
        )
        if 'Status' not in response:
            logger.info('Versioning not enabled for bucket %s' % bucket)
            s3.put_bucket_versioning(
                Bucket=bucket,
                VersioningConfiguration={
                    'Status': 'Enabled'
                }
            )
            logger.info('Enabled versioning for S3 bucket %s' % bucket)

    body = {
        "message": "S3 bucket logging janitor executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response