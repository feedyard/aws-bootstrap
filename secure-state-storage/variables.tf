terraform {
  required_version = ">= 0.11.8"
}

provider "aws" {
  version = ">= 1.36"
  region  = "${var.aws_region}"
  profile = "${var.profile}"
}

variable "aws_region" {}
variable "profile" {}
variable "bucket_name" {}
variable "enable_key_rotation" {}