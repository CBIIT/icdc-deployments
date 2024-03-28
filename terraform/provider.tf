terraform {
  required_providers {
    aws = {
        source  = "hashicorp/aws"
        version = "4.17.1"
    }
  }
}

provider "aws" {
  region = var.region
  default_tags {
   tags = {
     EnvironmentTier = terraform.workspace
     ApplicationName = var.stack_name
     Project = var.stack_name
     CreatedBy = "NCI-fnl-datacommons-devops@mail.nih.gov"
   }
 }
}