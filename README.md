# feedyard/bootstrap-aws
A minimal bootstrap configuration must occur to support an IaC process for managing aws state.  

With bootstrap access keys available, and assuming the configuration tools (terraform, kops, etc) maintain aws state files,  
then the only bootstrap setup really needed is S3 buckets for state information. (see below for additional bootstrap  
config for self managed pipelines.) The bootstrap step is run from the infrastructure developer's laptop.  

By default the buckets will be created with the following names:  
<project or org name parameter>-<account name>-bootstrap-state  

_note_:  s3 unique naming requirements apply.  


## usage

### CLI for bootstrap s3 buckets

Create a local file _bootstrap_vars.json_ in the following format. The tasks.py file will use this information to setup the
appropriate profile information for account access. You may list one or more accounts in which to create a state folder  
depending on your need. The feedyard/aws-bootstrap configuration assumes the use of a single bootstrap state bucket,  
along with the logging bucket. A later, logging structure pipeline will likely update these state buckets to use a  
different destination bucket.

```json
{
  "prefix": "team or product short-name",
  "accounts": {
    "profile": "name of profile in aws .credentials file for service account with appropriate permissions",
    "sandbox": "name of profile...",
    "nonprod": "name of profile...",
    "prod": "name of profile..."
  }
}
```

In addition to the credential information in ~/.aws, the createbuckets command will use the environment variable  
$CANONICAL_USER_ID to add log-delivery group permissions to the available logging bucket.

`$ invoke createbuckets`  
create an s3 bucket in the default region of each account following the above naming pattern.  

`$ invoke listbuckets`  
list all s3 buckets in the accounts.  

`$ deletebuckets`  
delete the bootstrap state and log bucket from each account.  

### secure-state-storage pipeline

### bootstrap-cluster pipeline

#### external pattern
The external pattern assumes the use of a pipeline orchestration tool already available and maintained separately from
the infrastructure team that owns this platform product. CircleCi.com is an example of a vendor provided product, or it
could be something self-managed elsewhere in the enterprise but available/appropriate to the needs of this team.

#### internal pattern
Where the bootstrap process requires aws based compute from which to run a pipeline tool...

### Requirements

#### AWS access credentials  

A bootstrap process is a means of dealing with the natural 'chicken & egg' problem in fully automating the configuration  
of IaaS resources. The _bootstrap_ examples in feedyard assume that access key ids and secret keys have been manually  
created in each account used in the infrastructure pipelines. Once the profiles and roles have been defined in  
the infrastructure bootstrap pipelines, these bootstrap service accounts can be deactivated and maintained for DR events.  

Example:  for each aws account

Create iam group 'BootstrapGroup' with AdministratorAccess
Create iam user '<organization>.<account>.bootstrap', add to the BootstrapGroup, and generate access keys 

This initial, minimal configuration of newly created AWS accounts requires the above bootstrap ids and secrets to be  
available locally in standard ~/.aws configuration files. Use of an AWS key management tool such as `aws-vault` is recommended.

#### local dependencies

python3  
  pkg: invoke, boto3, aws-cli  
  
ruby (>= 2.5.0)
  gem: awspec

run `prereqs.sh` to install local dependencies.  

