module "cloudwatch_ecs_task" {
  source = "git::https://github.com/CBIIT/datacommons-devops.git//terraform/modules/ecr?ref=icdc-cloudwatch"
  resource_prefix              = "${var.stack_name}-${terraform.workspace}"
  ecs_cluster_name             = var.ecs_cluster_name
  ecs_task_definition          = var.ecs_task_definition
  slack_notification_endpoint  = var.slack_notification_endpoint
  cron_expression              = var.cron_expression
}