"""invoke commands for feedyard/bootstrap-aws"""
from pathlib import Path
import sys
import json
import boto3
from invoke import task

BOOTSTRAP_CONFIG_FILE = './bootstrap.json'

@task
def listbuckets(_ctx):
    """List all s3 buckets in the aws accounts defined in bootstrap.json"""
    config = load_config(Path(BOOTSTRAP_CONFIG_FILE))
    for profile in config['accounts']:
        print('buckets in account: {}'.format(profile))
        s3 = boto3.Session(profile_name=config['accounts'][profile]).client('s3')
        buckets = [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]
        print("\t%s" % buckets)


@task
def validate(ctx):
    """style and lint tests"""
    ctx.run('yamllint .')
    ctx.run('terraform fmt -check .')
    ctx.run('rubocop')
    ctx.run('pylint tasks.py')
    ctx.run('pylint secure-state-storage/tasks.py')

def load_config(config_file):
    """Load bootstrap.json config file, defines aws accounts and access profiles."""
    if config_file.is_file():
        return json.loads(open(config_file).read())
    print('missing {} file.'.format(config_file))
    sys.exit(1)
