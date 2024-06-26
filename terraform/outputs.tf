//output "db_private_ip" {
//  value = module.neo4j.private_ip
//}
//output "opensearch_endpoint" {
//  value = module.opensearch.opensearch_endpoint
//}
output "cluster_endpoint" {
  value = module.aurora.*.cluster_endpoint
}
output "db_password" {
  value = module.aurora.*.db_password
  sensitive = true
}

/*output "eventbridge_rule_name" {
  value = module.event_scheduler.eventbridge_rule_name
  description = "Name of the EventBridge rule created for the ECS task scheduler."
}

output "eventbridge_ecs_target_id" {
  value = module.event_scheduler.eventbridge_ecs_target_id
  description = "The ID of the EventBridge ECS target."
}

output "eventbridge_lambda_target_id" {
  value = module.event_scheduler.eventbridge_lambda_target_id
  description = "The ID of the EventBridge Lambda target."
}

output "task_definition_arn" {
  value = data.aws_ecs_task_definition.latest.arn
}

output "task_definition" {
  value = data.aws_ecs_task_definition.latest.task_definition
}*/

#output "read_only_role_arn" {
 # value = module.new_relic_metric_pipeline.*.read_only_role_arn
#}
