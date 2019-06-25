from invoke import task

@task
def kvs(ctx):
    """validate key-value-store"""
    print('validate key-value-store')
    ctx.run("mkdir -p .terraform && echo 'default' > .terraform/environment")
    ctx.run("terraform init")
    ctx.run('tflint')
    ctx.run('rm -rf .terraform')