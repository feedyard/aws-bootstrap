from invoke import task
from pathlib import Path
import sys
import os
import boto3, botocore
import json

BOOTSTRAP_CONFIG_FILE = './bootstrap.json'

# uses prefix and account name from bootstrap config file to construct bucket name
# example: feedyard-sandbox-state
bucket_name = '{}-{}-tf-state'

@task
def enc(ctx, file='local.env', encoded_file='env.ci'):
    ctx.run("openssl aes-256-cbc -e -in {} -out {} -k $FEEDYARD_PIPELINE_KEY".format(file, encoded_file))

@task
def dec(ctx, encoded_file='env.ci', file='local.env'):
    ctx.run("openssl aes-256-cbc -d -in {} -out {} -k $FEEDYARD_PIPELINE_KEY".format(encoded_file, file))

@task
def listbuckets(ctx):
    config = load_config(Path(BOOTSTRAP_CONFIG_FILE))
    for profile in config['accounts']:
        print('buckets in account: {}'.format(profile))
        s3 = boto3.Session(profile_name=config['accounts'][profile]).client('s3')
        buckets = [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]
        print("\t%s" % buckets)


def load_config(config_file):
    if config_file.is_file():
        return json.loads(open(config_file).read())
    else:
        print ('missing {} file.'.format(config_file))
        sys.exit(1)
