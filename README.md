# feedyard/aws-bootstrap

Generally, the minimal bootstrap configuration needed to support an IaC process for managing aws infrastructure and  
services is encrypted S3 buckets for state information. (see below for additional bootstrap  
config for self managed pipelines.) The bootstrap state storage step is run from the infrastructure developer's laptop.  

## usage

Clone the repo, create a python virtual environment and confirm requirements are installed (see local dependencies  
below). Remove tf state file related names from .gitignore to store tf state with the repo.

### aws account bootstrap identity and short name

For each account used (see feedyard account structure in Documentation), the bootstrap account identity information  
(aws profile access id and secret keys) is available locally in ~/.aws/credentials. The bootstrap service account needs  
a fairly broad set of permission, but it is also an identity that is removed from the working automation early in the  
platform lifecycle.  

### bootstrap the secure s3 buckets

In the local repo, create a file _bootstrap.json_ in the following format. 

```json
{
  "prefix": "team or product short-name",
  "region": "default aws region to use",
  "accounts": {
    "<account descriptive name>": "name of profile in aws .credentials file for service account with appropriate permissions",
    "<account descriptive name>": "name of profile...",
    "<account descriptive name>": "name of profile...",
    "<account descriptive name>": "repeat for however many accounts you define in the platform architecture pipeline"
  }
}
```

You can use `$ invoke listbuckets` to confirm that you have the correct access information.  
 
By default the buckets will be created in the respective account with the following names:  
`<prefix>-<account descriptive name>-tf-state ` 

_note_:  s3 unique naming requirements apply.  

Now change to the `secure-state-storage` directory. Use the following Invoke commands to provision the s3 buckets.

`$ invoke new`  
Initialize and create terraform workspaces for each of the accounts in the bootstrap.json file. Local tfstate files  
are used for this bootstrap process. Be sure to add future work to your backlog to move these state files to a secure  
backup location. This initial bootstrap will not generally be repeated but the state file information can be used to  
automate activities if necessary.  

`$ invoke deploy`  
Creates an s3 state bucket using the above naming convention in each of the respective accounts. For each bucket, server-  
side encryption and object versioning is active.   

When needed, there is a destroy command that will fully remove the buckets using the tfstate information. See tasks.py  
for more understanding.  

### bootstrap-cluster pipeline (**work in progress**)

The recommended pattern assumes the use of a SaaS provided pipeline orchestration tool, already available and maintained  
separately from the infrastructure team that owns this platform product. CircleCi.com is an example of a vendor provided  
product.

Where the bootstrap process requires aws based compute from which to run a pipeline tool or just pipeline agents, or  
where there are opportunities to use early-deployed services to limit re-work such as Hashicorp's Vault, the  
bootstrap-cluster in this reference provides a demo of how EKS can be used for this somewhat ephemeral environment.  
Example uses circleci orchestration.  

### Requirements

#### AWS access credentials  

A bootstrap process is a means of dealing with the natural 'chicken & egg' problem in fully automating the configuration  
of IaaS resources. The _bootstrap_ examples in feedyard assume that access key ids and secret keys have been manually  
created in each account used in the bootstrap process or pipelines. Once the profiles and roles have been defined in  
the infrastructure pipelines, these bootstrap service accounts can be deactivated and maintained for DR events.  

Example:  for each aws account

Create iam group 'BootstrapGroup' with AdministratorAccess.  
Create iam user '<organization>.<account>.bootstrap', add to the BootstrapGroup, and generate access keys.  

This initial, minimal configuration of newly created AWS accounts requires the above bootstrap ids and secrets to be  
available locally in standard ~/.aws configuration files.  

#### local dependencies

terraform  

python3  
  pkg: invoke, boto3, aws-cli  
  
ruby (>= 2.5.0)  
  gem: awspec  
  
review `prereqs.sh` to install local dependencies.  

