terraform {
  required_version = ">= 0.11.10"
}

provider "aws" {
  version = ">= 1.41"
  region  = "${var.aws_region}"
  profile = "${var.profile}"
}

provider "random" {
  version = ">= 2.0"
}

variable "aws_region" {}
variable "profile" {}
variable "account" {}
variable "prefix" {}
variable "enable_key_rotation" { default = "True" }