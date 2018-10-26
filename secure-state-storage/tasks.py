from invoke import task
from pathlib import Path
import sys
import os
import json

BOOTSTRAP_CONFIG_FILE = '../bootstrap.json'

@task
def new(ctx):
    response = input('This is the first step after creating a bootstrap.json file with the desired aws account pipeline. ' \
                     'Terraform init will be called and a workspace created for each account name. ' \
                     'You must respond with YES to proceed ' \
                     '\nAre you sure?')

    if response == 'YES':
        ctx.run("terraform init")
        config = load_config(Path(BOOTSTRAP_CONFIG_FILE))
        for profile in config['accounts']:
            ctx.run("terraform workspace new {}".format(profile))

@task
def deploy(ctx):
    response = input('This will create aws s3 buckets for maintaining remote terraform state across all accounts listed ' \
                     'in bootstrap.json. $invoke new - must be run first. You must respond with YES to proceed ' \
                     '\nAre you sure?')

    if response == 'YES':
        config = load_config(Path(BOOTSTRAP_CONFIG_FILE))
        for profile in config['accounts']:
            ctx.run('terraform init')
            ctx.run('terraform workspace select {}'.format(profile))
            ctx.run('TF_VAR_aws_region={} TF_VAR_profile={} TF_VAR_account={} TF_VAR_prefix={} terraform plan'.format(config['region'], config['accounts'][profile], profile, config['prefix']))
            approve = input('Approve? (Y/n)')
            if approve == 'Y':
                ctx.run('TF_VAR_aws_region={} TF_VAR_profile={} TF_VAR_account={} TF_VAR_prefix={} terraform apply -auto-approve'.format(config['region'], config['accounts'][profile], profile, config['prefix']))
                os.environ['PROFILE'] = profile
                ctx.run('AWS_PROFILE={} rspec spec'.format(config['accounts'][profile]))
                approve = input('Press <Enter> to continue.')
            else:
                print('pipeline cancelled')
                sys.exit(1)

@task
def destroy(ctx):
    response = input('This will delete the aws s3 terraform state buckets for all accounts listed ' \
                     'You must respond with YES to proceed ' \
                     '\nAre you sure?')

    if response == 'YES':
        config = load_config(Path(BOOTSTRAP_CONFIG_FILE))
        for profile in config['accounts']:
            ctx.run('terraform init')
            ctx.run('terraform workspace select {}'.format(profile))
            approve = input('delete {}? (Y/n/skip)'.format(profile))
            if approve == 'Y':
                ctx.run('TF_VAR_aws_region={} TF_VAR_profile={} TF_VAR_account={} TF_VAR_prefix={} terraform destroy -force'.format(config['region'], config['accounts'][profile], profile, config['prefix']))
            elif approve == 'skip':
                print('skipping {}'.format(profile))
            else:
                print('pipeline cancelled')
                sys.exit(1)

def load_config(config_file):
    if config_file.is_file():
        return json.loads(open(config_file).read())
    else:
        print ('missing {} file.'.format(config_file))
        sys.exit(1)