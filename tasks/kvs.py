from invoke import task
import boto3

PREFIX='feedyard'
BUCKET=PREFIX+'-key-value-store'

@task
def list(ctx, svc):
    """list keys in service from bootstrap key-value-store"""
    session = boto3.Session()
    s3 = boto3.client('s3')
    #svc = ''
    for key in s3.list_objects_v2(Bucket=BUCKET, Prefix=svc + '/')['Contents']:
        print(key['Key'])

@task
def read(ctx, svc, key):
    """read key/value to bootstrap key-value-store. format: kvs.read service key"""
    aws s3 cp s3://some-bucket/hello.txt -


    # session = boto3.Session()
    # s3 = boto3.client('s3')
    # value = s3.get_object(
    #     Bucket = BUCKET,
    #     Key = f"{svc}/{key}"
    # )
    # print(value['Body'].read().decode('utf-8'))

@task
def write(ctx, svc, key, value):
    """write key/value to bootstrap key-value-store. format: kvs.write service key value"""
    cat "hello world" | aws s3 cp - s3://some-bucket/hello.txt



    # session = boto3.Session()
    # s3 = boto3.client('s3')
    # s3.put_object(
    #     Bucket = BUCKET,
    #     Key = f"{svc}/{key}",
    #     Body = value
    # )
