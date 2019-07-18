output "secure_state_storage_id" {
  value = "${aws_s3_bucket.secure-state-storage.id}"
}

output "secure_state_storage_arn" {
  value = "${aws_s3_bucket.secure-state-storage.arn}"
}

output "secure_state_storage_key_id" {
  value = "${aws_kms_key.secure-state-storage-kms-key.key_id}"
}
