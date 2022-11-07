#secrets
variable "neo4j_password" {
  type        = string
  description = "neo4j password"
}
variable "indexd_url" {
  type        = string
  description = "indexd url"
}
variable "db_ip" {
  type        = string
  description = "name of the db instance for this tier"
}

module "secrets" {
  source                        = "git::https://github.com/CBIIT/datacommons-devops.git//terraform/modules/secrets?ref=terraform_modules"
  app                           = var.stack_name
  es_host                       = var.create_opensearch_cluster ? module.opensearch[0].opensearch_endpoint : ""
  neo4j_password                = var.neo4j_password
  db_ip                         = var.db_ip
  indexd_url                    = var.indexd_url
  sumo_collector_token_frontend = module.monitoring.frontend_source_url
  sumo_collector_token_backend  = module.monitoring.backend_source_url
  sumo_collector_token_files    = module.monitoring.files_source_url
}