# if you are not using terraform cloud then you will need at least one initial state bucket

module "state_bucket" {
  source = "github.com/feedyard/tf-aws-state-bucket?ref=1.0.0"

  name                = "${var.prefix}-${var.account}-tf-state"
  enable_key_rotation = "${var.enable_key_rotation}"

  tags = {
    "pipeline"             = "aws-bootstrap/secure-state-store"
    "location-of-tf-state" = "s3 ${var.prefix}-${var.account}-tf-state"
  }
}
