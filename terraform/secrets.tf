locals {

  dynamic_secrets = {
    app = {
      secretKey = ""
      description = ""
      secretValue = {
        es_host = var.create_opensearch_cluster ? module.opensearch[0].opensearch_endpoint : ""
        sumo_collector_token_frontend = module.monitoring.sumo_source_urls.frontend[0]
        sumo_collector_token_backend  = module.monitoring.sumo_source_urls.backend[0]
        sumo_collector_token_files    = module.monitoring.sumo_source_urls.files[0]
        sumo_collector_token_interoperation  = module.monitoring.sumo_source_urls.interoperation[0]
        #mysql_host                    = module.aurora[0].cluster_endpoint
        #mysql_password                = nonsensitive(module.aurora[0].db_password)
      }
    }
  }
}
  variable "secret_values" {
  type = map(object({
    secretKey               = string
    secretValue             = map(string)
    description             = string
  }))
}


module "deepmerge" {
  source  = "Invicton-Labs/deepmerge/null"
  maps = [
    local.dynamic_secrets,
    var.secret_values
  ]
}

module "secrets" {
  source                        = "git::https://github.com/CBIIT/datacommons-devops.git//terraform/modules/secrets?ref=v1.0"
  app                           = var.stack_name
  secret_values                 = module.deepmerge.merged
}