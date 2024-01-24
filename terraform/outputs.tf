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
output "read_only_role_arn" {
  value = module.new_relic_metric_pipeline.*.read_only_role_arn
}
