
#create ecr
module "ecr" {
   count = var.create_ecr_repos ? 1: 0
   resource_prefix = "my_ecr"
   source = "git::https://github.com/CBIIT/datacommons-devops.git//terraform/modules/ecr?ref=v1.15"
   project = var.stack_name
   ecr_repo_names = var.ecr_repo_names
   tags = var.tags
   #create_env_specific_repo = var.create_env_specific_repo
   env = terraform.workspace
}