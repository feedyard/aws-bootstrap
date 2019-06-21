"""invoke commands for feedyard/bootstrap-aws/secure-state-storage"""
from pathlib import Path
import sys
import os
import json
import boto3
from invoke import task

BOOTSTRAP_CONFIG_FILE = 'bootstrap.json'
ARGS = 'TF_VAR_aws_region={} TF_VAR_profile={} TF_VAR_account={} TF_VAR_prefix={} '

@task
def new(ctx):
    """Initialize and create workspaces"""
    response = input('Initialize terraform modules and create workspace for each account.\n\n' \
                     'Required: Create a bootstrap.json file listing the aws accounts to be managed.\n' \
                     'You must respond with YES to proceed.\n' \
                     'Are you sure?')

    if response == 'YES':
        ctx.run("terraform init")
        config = load_config(Path(BOOTSTRAP_CONFIG_FILE))
        for profile in config['accounts']:
            ctx.run("terraform workspace new {}".format(profile))

@task
def deploy(ctx):
    """Create s3 buckets"""
    response = input('Create encrypted aws s3 buckets for maintaining remote terraform state for each account.\n\n' \
                     'You must respond with YES to proceed.\n' \
                     'Are you sure?')

    if response == 'YES':
        config = load_config(Path(BOOTSTRAP_CONFIG_FILE))
        for profile in config['accounts']:
            ctx.run('terraform init')
            ctx.run('terraform workspace select {}'.format(profile))
            ctx.run((ARGS + 'terraform plan').format(config['region'],
                                                     config['accounts'][profile],
                                                     profile,
                                                     config['prefix']))
            approve = input('Approve? (Y/n)')
            if approve == 'Y':
                ctx.run((ARGS + 'terraform apply -auto-approve').format(config['region'],
                                                                        config['accounts'][profile],
                                                                        profile,
                                                                        config['prefix']))
                os.environ['PROFILE'] = profile
                ctx.run('AWS_PROFILE={} rspec spec'.format(config['accounts'][profile]))
                _approve = input('Press <Enter> to continue.')
            else:
                print('Cancelled')
                sys.exit(1)

@task
def destroy(ctx):
    """Destroy s3 buckets"""
    response = input('Delete the aws s3 terraform state buckets for each account.\n\n' \
                     'Required: terraform state files are maintained in this repo.\n'
                     'You must respond with YES to proceed.\n' \
                     'Are you sure?')

    if response == 'YES':
        config = load_config(Path(BOOTSTRAP_CONFIG_FILE))
        for profile in config['accounts']:
            ctx.run('terraform init')
            ctx.run('terraform workspace select {}'.format(profile))
            approve = input('delete {}? (Y/n/skip)'.format(profile))
            if approve == 'Y':
                ctx.run((ARGS + 'terraform destroy -force').format(config['region'],
                                                                   config['accounts'][profile],
                                                                   profile,
                                                                   config['prefix']))
            elif approve == 'skip':
                print('skipping {}'.format(profile))
            else:
                print('Cancelled')
                sys.exit(1)

@task
def listbuckets(_ctx):
    """List all s3 buckets in the aws accounts defined in bootstrap.json"""
    config = load_config(Path(BOOTSTRAP_CONFIG_FILE))
    for profile in config['accounts']:
        print('buckets in account: {}'.format(profile))
        s3 = boto3.Session(profile_name=config['accounts'][profile]).client('s3')
        buckets = [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]
        print("\t%s" % buckets)

def load_config(config_file):
    """Load bootstrap.json config file, defines aws accounts and access profiles."""
    if config_file.is_file():
        return json.loads(open(config_file).read())
    print('missing {} file.'.format(config_file))
    sys.exit(1)
