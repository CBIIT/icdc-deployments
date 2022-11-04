public_subnet_ids = []
private_subnet_ids = [
  "subnet-4f35f112",
  "subnet-409a0424"
]
vpc_id = "vpc-29a12251"
stack_name = "icdc"

tags = {
  Project = "icdc"
  CreatedWith = "Terraform"
  POC = "ye.wu@nih.gov"
  Environment = "dev"
}
region = "us-east-1"

#alb
internal_alb = true
certificate_domain_name = "*.nci.nih.gov"
domain_name = "nci.nih.gov"

#ecr
create_ecr_repos = true
ecr_repo_names = ["backend","frontend","auth","files","users"]

#ecs
add_opensearch_permission = true
application_subdomain = "caninecommons"
microservices  = {
  frontend = {
    name = "frontend"
    port = 80
    health_check_path = "/"
    priority_rule_number = 22
    image_url = "cbiitssrepo/bento-frontend:latest"
    cpu = 256
    memory = 512
    path = ["/*"]
    number_container_replicas = 1
  },
  backend = {
    name = "backend"
    port = 8080
    health_check_path = "/ping"
    priority_rule_number = 20
    image_url = "cbiitssrepo/bento-backend:latest"
    cpu = 512
    memory = 1024
    path = ["/v1/graphql/*","/version"]
    number_container_replicas = 1
  },
  auth = {
    name = "auth"
    port = 8082
    health_check_path = "/api/auth/ping"
    priority_rule_number = 21
    image_url = "cbiitssrepo/bento-auth:latest"
    cpu = 256
    memory = 512
    path = ["/api/auth/*"]
    number_container_replicas = 1
  },
  files = {
    name = "files"
    port = 8081
    health_check_path = "/api/files/ping"
    priority_rule_number = 19
    image_url = "cbiitssrepo/bento-downloader:latest"
    cpu = 256
    memory = 512
    path = ["/api/files/*"]
    number_container_replicas = 1
  },
  users = {
    name = "users"
    port = 8083
    health_check_path = "/api/users/ping"
    priority_rule_number = 18
    image_url = "cbiitssrepo/bento-auth:latest"
    cpu = 256
    memory = 512
    path = ["/api/users/*"]
    number_container_replicas = 1
  }
}

#opensearch
create_opensearch_cluster = true
opensearch_ebs_volume_size = 200
opensearch_instance_type = "t3.medium.search"
opensearch_version = "OpenSearch_1.2"
allowed_ip_blocks = ["10.208.0.0/21","10.210.0.0/24"]
create_os_service_role = false
opensearch_instance_count = 1
create_cloudwatch_log_policy = true


#neo4j db is created by cloudone
create_db_instance = false
db_instance =
neo4j_password =

#dns is managed by cloudone
create_dns_record = false

#cloud platform
cloud_platform="cloudone"
target_account_cloudone = true
create_instance_profile = true

#cloudfront
create_cloudfront = false
create_files_bucket = false
cloudfront_distribution_bucket_name = "nci-cbiit-caninedatacommons-file-test"
cloudfront_slack_channel_name = "cloudone-cloudfront-wafv2"
alarms = {
  error4xx = {
    name = "4xxErrorRate"
    threshold = 10
  }
  error5xx = {
    name = "5xxErrorRate"
    threshold = 10
  }
}
slack_secret_name = "cloudfront-slack"

#monitoring
sumologic_access_id =
sumologic_access_key =
newrelic_account_id =
newrelic_api_key =