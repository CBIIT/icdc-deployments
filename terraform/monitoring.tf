#monitoring
variable "sumologic_access_id" {
  type        = string
  description = "Sumo Logic Access ID"
}
variable "sumologic_access_key" {
  type        = string
  description = "Sumo Logic Access Key"
  sensitive   = true
}

#variable "microservices" {
#  type = map(object({
#    name                      = string
#    port                      = number
#    health_check_path         = string
#    priority_rule_number      = number
#    image_url                 = string
#    cpu                       = number
#    memory                    = number
#    path                      = list(string)
#    number_container_replicas = number
#  }))
#}

module "monitoring" {
  source = "git::https://github.com/CBIIT/datacommons-devops.git//terraform/modules/monitoring?ref=v1.19"
  resource_prefix     = "${var.stack_name}-${terraform.workspace}"
  app                  = var.stack_name
  tags                 = var.tags
  sumologic_access_id  = var.sumologic_access_id
  sumologic_access_key = var.sumologic_access_key
  microservices        = var.microservices
  newrelic_account_id      = var.newrelic_account_id
  newrelic_api_key        = var.newrelic_api_key
  program              = var.program
  service              = var.service
}