# s3 bucket used as bootstrap and baseline-recover environment config key/value store
resource "aws_s3_bucket" "key-value-store" {
  bucket = "${local.bucket-name}"
  acl    = "private"

  versioning {
    enabled = "true"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = "${aws_kms_key.key-value-store-kms-key.arn}"
        sse_algorithm     = "aws:kms"
      }
    }
  }

  tags = {
    "pipeline"             = "bootstrap-aws/key-value-store"
    "location-of-tf-state" = "app.terraform.io/${var.prefix}/boostrap-aws-${var.environment}"
  }
}

resource "aws_s3_bucket_policy" "key-value-store-bucket-policy" {
  bucket = "${aws_s3_bucket.key-value-store.bucket}"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "key-value-store",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "${local.current-account-arn}"",
      },
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::${local.bucket-name}",
    }
  ]
}
POLICY
}

resource "aws_kms_key" "key-value-store-kms-key" {
  description             = "key managed by terraform moduile tf-aws-state-bucket"
  deletion_window_in_days = "7"
  enable_key_rotation     = "true"
}

resource "aws_kms_alias" "bucket_key_alias" {
  name          = "alias/managed-by/tf-aws-state-bucket/${random_pet.unique.id}"
  target_key_id = "${aws_kms_key.key-value-store-kms-key.id}"
}

resource "random_pet" "unique" {
  length    = 2
  separator = "-"
}

resource "aws_s3_bucket_public_access_block" "mod" {
  bucket = "${aws_s3_bucket.key-value-store.id}"

  block_public_acls   = true
  block_public_policy = true
}
