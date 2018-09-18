from invoke import task
from pathlib import Path
import sys
import boto3, botocore
import json

accounts_file = Path('./accounts.json')
platform_name = ''
account_profiles = ''

# uses project or Org name as first word followed by account name
# example: feedyard-sandbox-bootstrap-state
bucket_name = '{}-{}-bootstrap-state'
logging_bucket_name = '{}-available-logging'


@task
def init(ctx):
    ctx.run("terraform init -backend-config $CIRCLE_WORKING_DIRECTORY/backend.conf")

@task
def plan(ctx):
    cmd = 'terraform plan ' \
          '-var-file=./variables.tfvars'

    ctx.run(cmd)

@task
def apply(ctx):
    cmd = 'terraform apply ' \
          '-auto-approve ' \
          '-var-file=./variables.tfvars'

    ctx.run(cmd)

@task
def test(ctx):
    ctx.run("AWS_PROFILE=default rspec spec")

@task
def destroy(ctx):
    cmd = 'terraform destroy ' \
          '-force ' \
          '-var-file=./variables.tfvars'

    ctx.run(cmd)

@task
def enc(ctx, file='local.env', encoded_file='env.ci'):
    ctx.run("openssl aes-256-cbc -e -in {} -out {} -k $FEEDYARD_PIPELINE_KEY".format(file, encoded_file))

@task
def dec(ctx, encoded_file='env.ci', file='local.env'):
    ctx.run("openssl aes-256-cbc -d -in {} -out {} -k $FEEDYARD_PIPELINE_KEY".format(encoded_file, file))

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
    global logging_account
    global logging_profile
    global logging_account_canonical_user_id
    global bucket_name
    global logging_bucket_name
    global session

    print ('CLI: this s3 bucket creation script is intended to be used as part of a new AWS account bootstrap event and ' \
           'is therefore not expected to be used past this initial kickoff step.\n')

    load_profiles()
    for profile in account_profiles:
        bucket = bucket_name.format(platform_name, profile)
        create_s3(bucket, profile, account_profiles[profile], True, False)
    bucket = logging_bucket_name.format(platform_name)
    create_s3(bucket, logging_account, logging_profile, False, True)

@task
def deletebuckets(ctx):
    global accounts_file
    global platform_name
    global account_profiles
    global logging_account
    global logging_profile
    global bucket_name
    global logging_bucket_name
    global session

    response = input('This will destroy all the bootstrap state buckets. You must respond with YES to proceed ' \
                     '\nAre you sure?')

    if response == 'YES':
        load_profiles()
        for profile in account_profiles:
            del_bucket = bucket_name.format(platform_name, profile)
            delete_s3(del_bucket, profile, account_profiles[profile])
        del_bucket = logging_bucket_name.format(platform_name)
        delete_s3(del_bucket, logging_account, logging_profile)

def load_profiles():
    global accounts_file
    global platform_name
    global account_profiles
    global logging_account
    global logging_profile
    global logging_account_canonical_user_id

    if accounts_file.is_file():
        file_contents = json.loads(open(accounts_file).read())
        platform_name = file_contents['platform']
        account_profiles = file_contents['accounts']
        logging_account = file_contents['available_logging']['account']
        logging_profile = file_contents['available_logging']['aws_profile']
        logging_account_canonical_user_id = file_contents['available_logging']['canonical_user_id']
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

def create_s3(bucket, account, profile, version, logging):
    global platform_name
    global logging_account_canonical_user_id
    global session

    print('Create state s3 bucket {} in account:{}'.format(bucket, account))
    session = boto3.Session(profile_name=profile)
    if bucket_does_not_exist(bucket):
        # create bucket
        s3 = session.client('s3')
        s3.create_bucket(Bucket=bucket)
        s3 = session.resource('s3')
        # enable bucket versioning
        if version:
            bucket_versioning = s3.BucketVersioning(bucket)
            bucket_versioning.enable()
        # enable bucket object tagging
        bucket_tagging = s3.BucketTagging(bucket)
        bucket_tagging.put(
            Tagging={
                'TagSet': [
                    {
                        'Key': platform_name,
                        'Value': 'true'
                    },
                ]
            }
        )
        if logging:
            bucket_acl = s3.BucketAcl(bucket)
            bucket_acl.put(
                AccessControlPolicy={
                    'Grants': [
                        {
                            'Grantee': {
                                'Type': 'Group',
                                'URI': 'http://acs.amazonaws.com/groups/s3/LogDelivery'
                            },
                            'Permission': 'WRITE'
                        },
                        {
                            'Grantee': {
                                'Type': 'Group',
                                'URI': 'http://acs.amazonaws.com/groups/s3/LogDelivery'
                            },
                            'Permission': 'READ_ACP'
                        },
                        {
                            'Grantee': {
                                'Type': 'CanonicalUser',
                                'ID': logging_account_canonical_user_id
                            },
                            'Permission': 'FULL_CONTROL'
                        },
                    ],
                    'Owner': {
                        'ID': logging_account_canonical_user_id
                    }
                }
            )
    else:
        print ('{} already exists')


def delete_s3(del_bucket, account, profile):
    global session

    print('Delete s3 bucket {} in account:{}'.format(del_bucket, account))
    session = boto3.Session(profile_name=profile)
    if bucket_does_not_exist(del_bucket):
        print ('Cannot delete {}, does not exists'.format(del_bucket))
    else:
        s3 = session.resource('s3')
        bucket = s3.Bucket(del_bucket)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()