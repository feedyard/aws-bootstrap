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
account to proceed. (knowledge of use of above tools is assumed)

## Using the bootstrap-aws examples

The CircleCI pipeline workflows in the example assume use of the in-repo encryption of keys process supported by the  
feedyard/common-pipeline-tasks circleci Orb (see orb registry page for details). The pipelines also rely on the  
feedyard/terraform orb.  

environment.bin.enc to include:
```text
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_ROLE_PROFILE=
export TERRAFORM_CLOUD_TOKEN=
```

.circleci/config.yaml defines three optional workflows, depending on your situation.

*bootstrap-aws-key-value-store*  

Secrets management and non-secure configuration management are needed from the start. Definitely a chicken/egg situation.  
Hashicorp Vault and Consul are excellent, production worthy options and will be used in general throughout the feedyard  
examples. In a bootstrap situation where these are not yet available, an alternative is necessary. Even when they are  
available, there will continue to be some keys/config that must persist outside the general stores for rapid recover  
DR and rapid recovery. In this AWS example, Secrets Management Service and an S3 bucket are used to fill these requirements  
respectively. DynamoDB is another alternative for a key/store that many people find effective.  

Modify profile.json to provide unique bucket name, region, and an environment designation.

Tools to simplify use of this store within a ci/cd pipeline:  

_kvs_. Python package cli for interacting with s3 as basic key/value store.

*bootstrap-secure-state-storage*  

Creates appropriately configured s3 target for use as terraform remote state store. Required before initial terraform  
pipelines can be deployed.  


*bootstrap-pipeline-cluster*  

Creates basic EKS cluster for use as a deployment location for pipeline tool where it must be self managed in whatever  
degree. (e.g., for private agents used by BuildKite or Azure DevOps, or fully managed tools such as jenkins)  


## next steps
[AWS-IAM only example](https://github.com/feedyard/baseline-aws-auth-iam-only)  
[AWS idp integration example](https://github.com/feedyard/baseline-aws-auth-idp)
