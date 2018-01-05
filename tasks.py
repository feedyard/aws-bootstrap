from invoke import task
from pathlib import Path
import sys
import boto3, botocore
import json

accounts_file = Path('./accounts.json')
platform_name = ''
account_profiles = ''
prod_acct = 'prod'
prod_region = 'us-east-1'

# uses project or Org name as first word followed by account name
# example: feedyard-sandbox-state
bucket_name = '{}-{}-state'

print ('CLI: this s3 bucket creation script is intended to be used as part of a new AWS account bootstrap event and ' \
       'is therefore not expected to be used past this initial kickoff step.\n')

@task
def swarm(ctx):
    global accounts_file
    global platform_name
    global account_profiles
    global prod_acct
    global prod_region

    load_profiles()
    ctx.run("bash setup-backend.sh {0} {1} {2} {3}".format(platform_name, prod_acct, prod_region, account_profiles[prod_acct]), pty=True)
    ctx.run("terraform init -backend-config backend.conf")

@task
def listbuckets(ctx):
    global accounts_file
    global account_profiles

    load_profiles()
    for profile in account_profiles:
        print('Current buckets in account:{}'.format(profile))
        session = boto3.Session(profile_name=account_profiles[profile])
        s3 = session.client('s3')
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        print("\t%s" % buckets)

@task
def createbuckets(ctx):
    global accounts_file
    global platform_name
    global account_profiles
    global bucket_name
    global session

    load_profiles()
    for profile in account_profiles:
        bucket = bucket_name.format(platform_name, profile)
        print('Create state s3 bucket {} in account:{}'.format(bucket, profile))
        session = boto3.Session(profile_name=account_profiles[profile])
        if bucket_does_not_exist(bucket):
            # create bucket
            s3 = session.client('s3')
            s3.create_bucket(Bucket=bucket)
            # enable bucket versioning
            s3 = session.resource('s3')
            bucket_versioning = s3.BucketVersioning(bucket)
            bucket_versioning.enable()

        else:
            print ('{} already exists')

@task
def deletebuckets(ctx):
    global accounts_file
    global platform_name
    global account_profiles
    global bucket_name
    global session

    response = input('This will destroy all the bootstrap state buckets. You must respond with YES to proceed ' \
                     '\nAre you sure?')

    if response == 'YES':
        load_profiles()
        for profile in account_profiles:
            del_bucket = bucket_name.format(platform_name, profile)
            print('Delete s3 bucket {} in account:{}'.format(del_bucket, profile))
            session = boto3.Session(profile_name=account_profiles[profile])
            if bucket_does_not_exist(del_bucket):
                print ('Cannot delete {}, does not exists')
            else:
                s3 = session.resource('s3')
                bucket = s3.Bucket(del_bucket)
                for key in bucket.objects.all():
                    key.delete()
                bucket.delete()

def load_profiles():
    global accounts_file
    global platform_name
    global account_profiles

    if accounts_file.is_file():
        file_contents = json.loads(open(accounts_file).read())
        platform_name = file_contents['platform']
        account_profiles = file_contents['accounts']
    else:
        print ('{} does not exists'.format(accounts_file))
        sys.exit(1)

def bucket_does_not_exist(bucket):
    global session

    s3 = session.resource('s3')
    try:
        s3.meta.client.head_bucket(Bucket=bucket)
        return False
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = int(e.response['Error']['Code'])
        if error_code == 403:
            print("Private Bucket. Forbidden Access!")
            return False
        elif error_code == 404:
            return True
