output "key_value_store_id" {
  value = "${aws_s3_bucket.key-value-store.id}"
}

output "key_value_store_arn" {
  value = "${aws_s3_bucket.key-value-store.arn}"
}

output "key_value_store_key_id" {
  value = "${aws_kms_key.key-value-store-kms-key.key_id}"
}
