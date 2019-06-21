"""invoke commands for feedyard/bootstrap-aws"""
from pathlib import Path
import sys
import json
import boto3
from invoke import task

BOOTSTRAP_CONFIG_FILE = './bootstrap.json'




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
