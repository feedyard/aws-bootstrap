output "id" {
  value = "${module.state_bucket.id}"
}

output "arn" {
  value = "${module.state_bucket.arn}"
}

output "bucket_domain_name" {
  value = "${module.state_bucket.bucket_domain_name}"
}

output "region" {
  value = "${module.state_bucket.region}"
}

output "key_id" {
  value = "${module.state_bucket.key_id}"
}

output "key_arn" {
  value = "${module.state_bucket.key_arn}"
}
