# feedyard/aws-bootstrap

Assumptions: use of AWS Organization with a master/sub-account relationship structure.  
  
## cloud-native approach

Cloud based tools built upon development practices that sustain software-defined infrastructure and loose coupling,  
while significantly accelerating cloud native adoption. (used throughout these resources. _see SaaS selection models_)  


| category                | vendor                                  |
|-------------------------|-----------------------------------------|
| source version control  | [GitHub](https://github.com)            |
| pipeline orchestration  | [CircleCI](https://circleci.com)        |
| container registry      | [Quay](https://quay.io)                 |
| terraform state storage | [Terraform Cloud](https://terraform.io) |

## minimal aws bootstrap

__assumption__ any type of bootstrap example always begins from some set of minimal assumptions.  For the feedyard aws  
bootstrap examples, it is assumed that an Organization master account with 4 member accounts has been created, and the  
individual members of the team that will be maintaining the Platform product have added to a group in the master account  
that includes a role with admin permissions in each of the member accounts, and a set of bootstrap credentials exists  
in the Master account with similar permissions in the member accounts. The role ARN is used in the configuration.   

If you are able to make use of the above SaaS offerings, then you only need the programmatic access keys from the master  
account to proceed.

## Using the bootstrap-aws examples

The CircleCI pipeline workflows in the example assume use of the in-repo encryption of keys process supported by the  
feedyard/common-pipeline-tasks circleci Orb (see orb registry page for details). The pipelines also rely on the  
feedyard/terraform orb.  

.circleci/config.yaml defines three optional workflows, depending on your situation.

*bootstrap-aws-key-value-store*  

Secrets management and non-secure configuration management are needed from the start. Definitely a chicken/egg situation.  
Hashicorp Vault and Consul are excellent, production worthy options and will be used in general throughout the feedyard  
examples. In a bootstrap situation where these are not yet available, an alternative is necessary. Even when they are  
available, there will continue to be some keys/config that must persist outside the general stores for rapid recover  
DR and rapid recovery. In this AWS example, Secrets Management Service and an S3 bucket are used to fill these requirements  
respectively. DynamoDB is another alternative for a key/store that many people find effective.

Tools to simply use of these stores within a ci/cd pipeline:  

_kvs_. Python package cli for interacting with s3 as basic key/value store.
 
 
*bootstrap-secure-state-storage*  

Creates appropriately configured s3 target for use as terraform remote state store. Required before initial terraform  
pipelines can be deployed.  


*bootstrap-pipeline-cluster*  

Creates basic EKS cluster for use as a deployment location for pipeline tool where it must be self managed in whatever  
degree. (e.g., for private agents used by BuildKite or Azure DevOps, or fully managed tools such as jenkins)  


[AWS-IAM only example](https://github.com/feedyard/baseline-aws-auth-iam-only)  
[AWS idp integration example](https://github.com/feedyard/baseline-aws-auth-idp)



### alternative tf_state situations

Without using a service such as Terraform Cloud, you will need an encrypted S3 bucket in the master account that will  
maintain much of the terraform state file storage. 


```bash
$ inv deploy.statebucket
```



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

