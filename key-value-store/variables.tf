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
      name = "boostrap-aws_${var.environment}"
    }
  }
}

# for

provider "aws" {
  region  = "${var.aws_region}"
}


variable "environment" {}
variable "aws_region" {}
variable "prefix" {}

variable "enable_key_rotation" {
  default = "True"
}
