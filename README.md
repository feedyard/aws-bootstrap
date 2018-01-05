# feedyard/bootstrap-aws
A minimal bootstrap configuration must occur to support an IaC process for managing aws state.  

With bootstrap access keys available, and assuming the configuration tools (terraform, kops, etc) maintain aws state files,
then the only bootstrap setup really needed is S3 buckets for state information. (see below for additional bootstrap
config for self managed pipelines.) The bootstrap step is run from the infrastructure developer's laptop.

By default the buckets will be created with the following names:  
<project or org name parameter>-<account name>-state  

_note_: routine s3, unique naming requirements apply.  

### Requirements

A bootstrap group/user has been created in each account with permissions sufficient to execute terraform
configuration plans, and this access information is maintained locally in standard ~/.aws configuration files.  

Create a local file _accounts.json_ in the following format. The tasks.py file will use this information to setup the
appropriate profile information for account access. This example assumes that one account will be named 'prod' as the
production account.

```json
{
  "platform": "platform or project name to use in bucket name",
  "accounts": {
    "account1 name": "matching aws profile name in ~/.aws/credentials",
    "account2 name": "matching aws profile name in ~/.aws/credentials",
    "account3 name": "matching aws profile name in ~/.aws/credentials",
    "account4 name": "matching aws profile name in ~/.aws/credentials"
  }
}
```

python  
  pkg: invoke, boto3


#### external pattern
The external pattern assumes the use of a pipeline orchestration tool already available and maintained separately from
the infrastructure team that owns this platform product. CircleCi.com is an example of a vendor provided product, or it
could be something self-managed elsewhere in the enterprise but available/appropriate to the needs of this team.

#### internal pattern
Where the bootstrap process requires aws based compute from which to run a pipeline tool, this repo includes
terraform to support such a self-managed environment in the production account.

the bootstrap terreform isolates a dedicated VPC/subnet location, with a pre-defined security group and IAM instance
profile to support a pipeline service that will manage the starting point for creating and maintaining the components
that enable building the management layer. It is recommended that the Bootstrap env be implemented in the AWS used for
production since this is typically the most protected account with the least potential number of IAM users.

assumes the correct bootstrap-prod credentials are in ENV