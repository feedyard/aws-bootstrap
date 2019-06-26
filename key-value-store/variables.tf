terraform {
  required_version = "~> 0.12"
  required_providers {
    aws = "~> 2.15"
    random = "~> 2.0"
  }
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "feedyard"
    workspaces {
      prefix = "boostrap-aws-"
    }
  }
}

# for

provider "aws" {
  region  = "${var.aws_region}"
  assume_role {
    role_arn     = "${var.aws_role}"
    session_name = "bootstrap-aws-${var.environment}"
  }
}

variable "prefix" {}
variable "environment" {}
variable "aws_role" {}
variable "aws_region" {}