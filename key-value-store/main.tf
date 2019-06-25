# s3 bucket used and bootstrap and baseline-recover environment config key/value store
module "key_value_store" {
  source = "github.com/feedyard/tf-aws-state-bucket?ref=1.0.0"

  name                = "${var.prefix}-key-value-store"
  enable_key_rotation = "${var.enable_key_rotation}"

  tags = {
    "pipeline"             = "bootstrap-aws/key-value-store"
    "location-of-tf-state" = "app.terraform.io/${var.prefix}/boostrap-aws-${var.environment}"
  }
}
