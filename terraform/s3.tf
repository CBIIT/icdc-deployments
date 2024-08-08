resource "aws_s3_bucket_policy" "alb_bucket_policy" {
  bucket = module.s3.bucket_id
  policy = data.aws_iam_policy_document.s3_alb_policy.json
}

module "s3" {
  source = "git::https://github.com/CBIIT/datacommons-devops.git//terraform/modules/s3?ref=lifecycle_s3"
  #resource_prefix     = "${var.stack_name}-${terraform.workspace}"
  bucket_name = var.bucket_name
  stack_name = var.stack_name
  create_bucket_acl = var.create_bucket_acl
  env = terraform.workspace
  tags = var.tags
  s3_force_destroy = var.s3_force_destroy
  days_for_archive_tiering = 125
  days_for_deep_archive_tiering = 180
  s3_enable_access_logging = false
  s3_access_log_bucket_id = ""
}