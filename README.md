# feedyard/bootstrap-aws
A minimal bootstrap configuration must occur to support an IaC process for managing aws state.  

With bootstrap access keys available, and assuming the configuration tools (terraform, kops, etc) maintain aws state files,  
then the only bootstrap setup really needed is S3 buckets for state information. (see below for additional bootstrap  
config for self managed pipelines.) The bootstrap step is run from the infrastructure developer's laptop.  

By default the buckets will be created with the following names:  
<project or org name parameter>-<account name>-bootstrap-state  

_note_:  s3 unique naming requirements apply.  


## usage

Create a local file _accounts.json_ in the following format. The tasks.py file will use this information to setup the
appropriate profile information for account access. This example assumes that one account will be named 'prod' as the
production account.

```json
{
  "platform": "platform or project name to use in bucket name",
  "accounts": {
    "account1 name": "matching aws service account credential in ~/.aws/credentials",
    "account2 name": "matching aws service account credential in ~/.aws/credentials",
    "account3 name": "matching aws service account credential in ~/.aws/credentials",
    "account4 name": "matching aws service account credential in ~/.aws/credentials"
  },
  "available_logging": {
    "account": "aws account name. One of the accounts above.",
    "profile": "aws service account credential in ~/.aws/credentials",
    "canonical_user_id": "12345abcd"
  }
}
```

`$ invoke createbuckets`  
create an s3 bucket in the default region of each account following the above naming pattern.  

`$ invoke listbuckets`  
list all s3 buckets in the listed accounts.  

`$ deletebuckets`  
delete the bootstrap-state bucket from each account.  


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