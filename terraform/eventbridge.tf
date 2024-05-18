module "event_scheduler" {
  source              = "git::https://github.com/CBIIT/datacommons-devops.git//terraform/modules/eventbridge?ref=eventbridge_new"
  resource_prefix     = "${var.stack_name}-${terraform.workspace}"
  eventbridge_name    = var.eventbridge_name
  schedule_expression = var.schedule_expression // Scheduled expression for every day at 9 AM,
  target_type         = var.target_type
  role_arn            = module.ecs.ecs_task_execution_role_arn
  target_arn          = var.task_definition_arn
  ecs_cluster_arn     = var.ecs_cluster_arn 
  task_definition_arn = var.task_definition_arn
  private_subnet_ids  = var.private_subnet_ids
  ecs_security_groups = var.ecs_security_groups
  assign_public_ip    = var.assign_public_ip
  target_account_cloudone = var.target_account_cloudone
}
  /*input               = jsonencode({
    "containerOverrides": [
      {
        "name": "container-name",
        "environment": [
          {"name": "KEY", "value": "VALUE"}
        ]
      }
    ]
  })
}*/
