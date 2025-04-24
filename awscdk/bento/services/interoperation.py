from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_secretsmanager as secretsmanager

class interoperationService:
  def createService(self, config):

    ### Files Service ###############################################################################################################
    service = "interoperation"

    # Set container configs
    if config.has_option(service, 'command'):
        command = [config[service]['command']]
    else:
        command = None

    environment={
            "NEW_RELIC_APP_NAME":"{}-{}-backend".format(config['main']['project'], config['main']['tier']),
            "AUTH_ENABLED":"false",
            "REDIS_AUTH_ENABLED":"false",
            "AUTH_URL":"/api/auth/authenticated",
            "AUTHORIZATION_ENABLED":"true",
            "BACKEND_URL":"/v1/graphql/",
            "DATE":"2024-04-23",
            "BENTO_BACKEND_GRAPHQL_URI":"https://clinical-qa.datacommons.cancer.gov/v1/graphql/",
            "REDIS_ENABLE":"true",
            "REDIS_AUTH_ENABLED":"true",
            "REDIS_FILTER_ENABLE":"true",
            #"REDIS_HOST":"localhost",
            "REDIS_PORT":"6379",
            "REDIS_USE_CLUSTER":"true",
            "SIGNED_URL_EXPIRY_SECONDS":"86400",
            "PROJECT":"ICDC",
            "SIGNED_URL_EXPIRY_SECONDS":"86400",
            "SESSION_TIMEOUT":"1200",
            "URL_SRC":"CLOUD_FRONT",
            "VERSION":config[service]['image'],
            "BENTO_BACKEND_GRAPHQL_URI":config[service]['bento_backend_graphql_uri'],
        }

    secrets={
            "NEW_RELIC_LICENSE_KEY":ecs.Secret.from_secrets_manager(secretsmanager.Secret.from_secret_name_v2(self, "interoperation_newrelic", secret_name='monitoring/newrelic'), 'api_key'),
            "REDIS_HOST":ecs.Secret.from_secrets_manager(self.secret, 'neo4j_ip'),
            "REDIS_PASSWORD":ecs.Secret.from_secrets_manager(self.secret, 'redis_password'),
            "CLOUDFRONT_PRIVATE_KEY":ecs.Secret.from_secrets_manager(secretsmanager.Secret.from_secret_name_v2(self, "files_cf_key", secret_name="ec2-ssh-key/{}/private".format(self.cfKeys.key_pair_name)), ''),
            "CLOUDFRONT_KEY_PAIR_ID":ecs.Secret.from_secrets_manager(self.secret, 'cf_key_pair_id'),
            "CLOUDFRONT_DOMAIN":ecs.Secret.from_secrets_manager(self.secret, 'cf_url'),
            "S3_ACCESS_KEY_ID":ecs.Secret.from_secrets_manager(self.secret, 's3_access_key_id'),
            "S3_SECRET_ACCESS_KEY":ecs.Secret.from_secrets_manager(self.secret, 's3_secret_access_key'),
            "FILE_MANIFEST_BUCKET_NAME":ecs.Secret.from_secrets_manager(self.secret, 'file_manifest_bucket_name'),
        }
    
    taskDefinition = ecs.FargateTaskDefinition(self,
        "{}-{}-taskDef".format(self.namingPrefix, service),
        cpu=config.getint(service, 'taskcpu'),
        memory_limit_mib=config.getint(service, 'taskmemory')
    )

    # Grant ECR access
    taskDefinition.add_to_execution_role_policy(
            iam.PolicyStatement(
                actions=[
                    "ecr:UploadLayerPart",
                    "ecr:PutImage",
                    "ecr:ListTagsForResource",
                    "ecr:InitiateLayerUpload",
                    "ecr:GetRepositoryPolicy",
                    "ecr:GetLifecyclePolicy",
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:DescribeRepositories",
                    "ecr:CompleteLayerUpload",
                    "ecr:BatchGetImage",
                    "ecr:BatchCheckLayerAvailability"
                ],
                effect=iam.Effect.ALLOW,
                resources=["arn:aws:ecr:us-east-1:986019062625:repository/*"]
            )
        )

    taskDefinition.add_to_execution_role_policy(
            iam.PolicyStatement(
                actions=["ecr:GetAuthorizationToken"],
                effect=iam.Effect.ALLOW,
                resources=["*"]
            )
        )
    
    # Interoperation Container
    ecr_repo = ecr.Repository.from_repository_arn(self, "{}_repo".format(service), repository_arn=config[service]['repo'])
    
    interoperation_container = taskDefinition.add_container(
        service,
        #image=ecs.ContainerImage.from_registry("{}:{}".format(config[service]['repo'], config[service]['image'])),
        image=ecs.ContainerImage.from_ecr_repository(repository=ecr_repo, tag=config[service]['image']),
        cpu=config.getint(service, 'cpu'),
        memory_limit_mib=config.getint(service, 'memory'),
        port_mappings=[ecs.PortMapping(container_port=config.getint(service, 'port'), name=service)],
        command=command,
        environment=environment,
        secrets=secrets,
        logging=ecs.LogDrivers.aws_logs(
            stream_prefix="{}-{}".format(self.namingPrefix, service)
        )
    )

    # Sumo Logic FireLens Log Router Container
    sumo_logic_container = taskDefinition.add_firelens_log_router(
        "sumologic-firelens",
        image=ecs.ContainerImage.from_registry("public.ecr.aws/aws-observability/aws-for-fluent-bit:stable"),
        firelens_config=ecs.FirelensConfig(
            type=ecs.FirelensLogRouterType.FLUENTBIT,
            options=ecs.FirelensOptions(
                enable_ecs_log_metadata=True
            )
        ),
    essential=True
    )
    
    # New Relic Container
    new_relic_container = taskDefinition.add_container(
        "newrelic-infra",
        image=ecs.ContainerImage.from_registry("newrelic/nri-ecs:1.9.2"),
        cpu=0,
        essential=True,
        secrets={"NRIA_LICENSE_KEY":ecs.Secret.from_secrets_manager(secretsmanager.Secret.from_secret_name_v2(self, "intnr_newrelic", secret_name='monitoring/newrelic'), 'api_key'),},
        environment={
            "NEW_RELIC_HOST":"gov-collector.newrelic.com",
            "NEW_RELIC_APP_NAME":"{}-{}-interoperation".format(config['main']['project'], config['main']['tier']),
            "NEW_RELIC_DISTRIBUTED_TRACING_ENABLED":"true",
            "NRIA_PASSTHROUGH_ENVIRONMENT":"ECS_CONTAINER_METADATA_URI,ECS_CONTAINER_METADATA_URI_V4,FARGATE", 
            "FARGATE":"true",
            "NRIA_CUSTOM_ATTRIBUTES":'{"nrDeployMethod":"downloadPage"}', 
            "NRIA_IS_FORWARD_ONLY":"true",
            "NRIA_OVERRIDE_HOST_ROOT": ""    
            },
    )


    ecsService = ecs.FargateService(self,
        "{}-{}-service".format(self.namingPrefix, service),
        cluster=self.ECSCluster,
        task_definition=taskDefinition,
        enable_execute_command=True,
        min_healthy_percent=50,
        max_healthy_percent=200,
        circuit_breaker=ecs.DeploymentCircuitBreaker(
            enable=True,
            rollback=True
        ),
    )
    #ecsService.connections.allow_to_default_port(self.auroraCluster)

    ecsTarget = self.listener.add_targets("ECS-{}-Target".format(service),
        port=int(config[service]['port']),
        protocol=elbv2.ApplicationProtocol.HTTP,
        health_check = elbv2.HealthCheck(
            path=config[service]['health_check_path']),
        targets=[ecsService],)

    elbv2.ApplicationListenerRule(self, id="alb-{}-rule".format(service),
        conditions=[
            elbv2.ListenerCondition.path_patterns(config[service]['path'].split(','))
        ],
        priority=int(config[service]['priority_rule_number']),
        listener=self.listener,
        target_groups=[ecsTarget])
