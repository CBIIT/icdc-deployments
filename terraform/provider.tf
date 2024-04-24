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
}  
  
  /*default_tags {
    tags = {
      EnvironmentTier = terraform.workspace
      Customer        = "nci od cbiit ods"
      DevLead         = "Karan Sheth"
      CreatedBy       = "Charles Ngu"
      ResourceName    = "NCI-icdc-${terraform.workspace}"
      FISMA           = "moderate"
      ManagedBy       = "terraform"
      OpsModel        = "cbiit managed hybrid"
      Program         = "crdc"
      PII             = "yes"
      Backup          = local.level
      PatchGroup      = local.level
      ApplicationName = "Integrated Canine Data Commons"
      ProjectManager  = "Gina Kuffel"
    }
  }
}*/