# EFS
module "efs" {
  source = "git::https://github.com/CBIIT/datacommons-devops.git//terraform/modules/efs?ref=efs-module"
  project         = var.stack_name
  tags            = var.tags
  vpc_id          = var.vpc_id
  efs_subnet_ids  = var.private_subnet_ids
  env             = terraform.workspace
}