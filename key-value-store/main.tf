# s3 bucket used as bootstrap and baseline-recover environment config key/value store
resource "aws_s3_bucket" "key-value-store" {
  bucket = "${var.prefix}-key-value-store"
  acl    = "private"
  policy = "${data.aws_iam_policy_document.key-value-store-policy-document.json}"

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

data "aws_iam_policy_document" "key-value-store-policy-document" {
  statement {
    principals {
      type        = "AWS"
      identifiers = [
        "${aws_iam_role.access-bootstrap-key-value-store.arn}",
        "${var.aws_role}"
      ]
    }
    actions = [
      "s3:s3:ListBucket",
      "s3:GetBucketLocation",
    ]
    resources = [
      "arn:aws:s3:::${aws_s3_bucket.key-value-store.arn}"
    ]
  }
  statement {
    principals {
      type        = "AWS"
      identifiers = [
        "${aws_iam_role.access-bootstrap-key-value-store.arn}",
        "${var.aws_role}"
      ]
    }
    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:DeleteObject"
    ]
    resources = [
      "arn:aws:s3:::${aws_s3_bucket.key-value-store.arn}/*"
    ]
  }
}

# profile account role for accessing the bootstrap key/value store
resource "aws_iam_role" "access-bootstrap-key-value-store" {
  name               = "AccessBootstrapKeyValueStore"
  assume_role_policy = "${data.aws_iam_policy_document.access-key-value-store-policy-document.json}"
}

data "aws_iam_policy_document" "access-key-value-store-policy-document" {
  statement {
    actions = [
      "s3:s3:ListBucket",
      "s3:GetBucketLocation",
    ]
    resources = [
      "arn:aws:s3:::${aws_s3_bucket.key-value-store.arn}"
    ]
  }
  statement {
    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:DeleteObject"
    ]
    resources = [
      "arn:aws:s3:::${aws_s3_bucket.key-value-store.arn}/*"
    ]
  }
}