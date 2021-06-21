# Trigger ETL Lambda

A lambda function that takes the data extracted from the [getJIRAData](https://github.com/Dazza65/getJIRAData) project, transforms it using AWS Glue and writes the output to an S3 bucket to be picked up by a subsequent job to ingest into AWS QuickSight for visualisation.

## Build and deploy

1. Clone the repository
1. Install the following dependencies
    1. [jq](https://stedolan.github.io/jq/)
    1. AWS CLI (v2.0.62)
1. Create CloudFormation stack
1. ./sh package.sh
1. ./sh upload.sh
1. ./sh upload-etl.sh

## The following AWS resources are created

1. Lambda function
1. Glue
    1. Crawler
    1. Classifier
    1. Database
    1. Job
1. Role - the execution role associated with the Lambda function to provide access to XRay, SSM, S3 and CF
1. S3 buckets
    1. source for the retrieved JIRA issues.
    1. output for transformed data
    1. ETL script

