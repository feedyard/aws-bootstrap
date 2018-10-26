module "state_bucket" {
  source = "github.com/feedyard/tf-aws-state-bucket?ref=1.0.0"

  name                = "${var.prefix}-${var.account}-tf-state"
  enable_key_rotation = "${var.enable_key_rotation}"

  tags = {
    "pipeline" = "aws-bootstrap/secure-state-store"
    "location-of-tf-state" = "tf state s3 stores created as part of bootstrap process are maintained in bootstrap repo"
  }
}
