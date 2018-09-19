# backend.conf is setup at the start based on target account
terraform {
  required_version = ">= 0.11.8"

  backend "s3" {
  }
}

provider "aws" {
  version = ">= 1.36"
  region = "${var.aws_region}"
}

variable "aws_region" { default = "us-east-1" }
