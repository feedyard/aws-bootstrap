# s3 bucket used as bootstrap and baseline-recover environment config key/value store
resource "aws_s3_bucket" "key-value-store" {
  bucket = "${local.bucket-name}"
  acl    = "private"
  policy = <<EOF
{
  "Version":"2012-10-17",
  "Statement":[
    {
      "Effect":"Allow",
      "Principal": { "AWS": ["${local.current-account-arn}"] },
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ]
      "Resource": [
        "arn:aws:s3:::${local.bucket-name}"
      ]
    }
  ]
}
EOF

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

# profile account role for accessing the bootstrap key/value store
//resource "aws_iam_role" "access-bootstrap-key-value-store-role" {
//  name               = "AccessBootstrapKeyValueStoreRole"
//  assume_role_policy = <<EOF
//{
//  "Version":"2012-10-17",
//  "Statement":[
//    {
//      "Effect":"Allow",
//      "Principal": { "AWS": ["${local.current-account-arn}"] },
//      "Action": [
//        "s3:GetObject",
//      ]
//      "Resource":"arn:aws:s3:::examplebucket/*"
//    }
//  ]
//}
//EOF
//}
//
//resource "aws_iam_policy" "access-bootstrap-key-value-store-policy" {
//  name   = "AccessBootstrapKeyValueStore"
//  path   = "/"
//  policy = "${data.aws_iam_policy_document.access-key-value-store-policy-document.json}"
//}
//
//data "aws_iam_policy_document" "access-key-value-store-policy-document" {
//  statement {
//    actions = [
//      "s3:ListBucket",
//      "s3:GetBucketLocation",
//    ]
//    resources = [
//      "arn:aws:s3:::${local.bucket-name}"
//    ]
//  }
//  statement {
//    actions = [
//      "s3:PutObject",
//      "s3:GetObject",
//      "s3:DeleteObject"
//    ]
//    resources = [
//      "arn:aws:s3:::${local.bucket-name}/*"
//    ]
//  }
//}
//
//resource "aws_iam_policy_attachment" "attach-key-value-store-access-policy-to-role" {
//  name       = "AccessBootstrapKeyValueStore"
//  roles      = ["${aws_iam_role.access-bootstrap-key-value-store-role.name}"]
//  policy_arn = "${aws_iam_policy.access-bootstrap-key-value-store-policy.arn}"
//}
