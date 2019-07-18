# s3 bucket used as bootstrap terraform remote state store
resource "aws_s3_bucket" "secure-state-storage" {
  bucket = "${local.bucket-name}"
  acl    = "private"

  versioning {
    enabled = "true"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = "${aws_kms_key.secure-state-storage-kms-key.arn}"
        sse_algorithm     = "aws:kms"
      }
    }
  }

  tags = {
    "pipeline"             = "bootstrap-aws/secure-state-storage"
    "location-of-tf-state" = "app.terraform.io/${var.prefix}/boostrap-aws-state-${var.environment}"
  }
}

resource "aws_s3_bucket_policy" "secure-state-storage-bucket-policy" {
  bucket = "${aws_s3_bucket.secure-state-storage.bucket}"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "${local.current-account-id}" },
      "Action": [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ],
      "Resource": "arn:aws:s3:::${local.bucket-name}/*"
    },
    {
      "Effect": "Allow",
      "Principal": { "AWS": "${local.current-account-id}" },
      "Action": [
          "s3:ListBucket"
        ],
      "Resource": "arn:aws:s3:::${local.bucket-name}"
    }
  ]
}
POLICY
}

resource "aws_kms_key" "secure-state-storage-kms-key" {
  description             = "key managed by pipeline bootstrap-aws/secure-state-storage"
  deletion_window_in_days = "7"
  enable_key_rotation     = "true"
}

resource "aws_kms_alias" "bucket_key_alias" {
  name          = "alias/managed-by/bootstrap-aws/secure-state-storage/${random_pet.unique.id}"
  target_key_id = "${aws_kms_key.secure-state-storage-kms-key.id}"
}

resource "random_pet" "unique" {
  length    = 2
  separator = "-"
}

resource "aws_s3_bucket_public_access_block" "mod" {
  bucket = "${aws_s3_bucket.secure-state-storage.id}"

  block_public_acls   = true
  block_public_policy = true
}
