"""invoke tasks for the feedyard/bootstrap-aws resource"""
from invoke import Collection
from tasks import deploy
from tasks import delete
from tasks import gpg
from tasks import kvs

ns = Collection()
ns.add_collection(deploy)
ns.add_collection(delete)
ns.add_collection(gpg)
ns.add_collection(kvs)