# S3 Bucket Janitor

This is Lambda function that configures logging and versioning on S3 Buckets.

## Prerequisites

You must have [Serverless Framework](https://serverless.com/) installed.

Your AWS IAM user must have permissions to create required AWS resources.

## Usage

Create new configuration file from `janitor.example.yml` replacing `example` with a Serverless stage name, e.g. your AWS region.

```
region: eu-west-1
bucket_region: eu-west-1
target_bucket: example-logs
```

- `region` is the region to deploy AWS Lambda function to
- `bucket_region` is used to filter S3 buckets to configure
- `target_bucket` is the S3 bucket to use for logging

Deploy function to the given stage:

```
sls deploy --stage example
```

## License

MIT: [LICENSE](LICENSE.txt)