from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    aws_sns_subscriptions as subs,
)
from constructs import Construct
import os

# --- Environment-specific configuration ---
ENV_CONFIG = {
    "dev": {
        "CLUSTER_ARN": "arn:aws:ecs:us-east-1:917011444075:cluster/icdc-dev-ecs",
        "TASK_FAMILY": "icdc-dev-data-retriever",
        "SLACK_SECRET_NAME": "slack/data-retriever-webhook",
    },
    "qa": {
        "CLUSTER_ARN": "arn:aws:ecs:us-east-1:917011444075:cluster/icdc-qa-ecs",
        "TASK_FAMILY": "icdc-qa-data-retriever",
        "SLACK_SECRET_NAME": "slack/data-retriever-webhook",
    },
    "stage": {
        "CLUSTER_ARN": "",
        "TASK_FAMILY": "icdc-stage-data-retriever",
        "SLACK_SECRET_NAME": "slack/data-retriever-webhook",
    },
    "prod": {
        "CLUSTER_ARN": "",
        "TASK_FAMILY": "icdc-prod-data-retriever",
        "SLACK_SECRET_NAME": "slack/data-retriever-webhook",
    },
}

# --- Global Parameters ---
PERMISSION_BOUNDARY_ARN = "arn:aws:iam::917011444075:policy/PermissionBoundary_PowerUser"
ROLE_PREFIX = "power-user"

class NotifyStack(Stack):
    def __init__(self, scope: Construct, id: str, env_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        cfg = ENV_CONFIG.get(env_name)
        if not cfg:
            raise ValueError(f"No configuration found for environment: {env_name}")

        cluster_arn = cfg["CLUSTER_ARN"]
        task_family = cfg["TASK_FAMILY"]
        slack_secret = cfg["SLACK_SECRET_NAME"]

        # --- Apply global Permission Boundary ---
        iam.PermissionsBoundary.of(self).apply(
            iam.ManagedPolicy.from_managed_policy_arn(
                self,
                "GlobalPermissionBoundary",
                PERMISSION_BOUNDARY_ARN
            )
        )

        # --- SNS topic ---
        topic = sns.Topic(
            self,
            "NotificationsTopic",
            topic_name=f"{env_name}-data-retriever-notifications"
        )

        # --- Lambda function ---
        fn = _lambda.Function(
            self,
            "SnsToSlackRelay",
            function_name=f"{env_name}-sns-to-slack-relay",
            role=_lambda.Role(
                self,
                f"{ROLE_PREFIX}-{env_name}-lambda-role",
                assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                managed_policies=[
                    iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
                ],
                permissions_boundary=iam.ManagedPolicy.from_managed_policy_arn(
                    self,
                    f"{ROLE_PREFIX}-Boundary",
                    PERMISSION_BOUNDARY_ARN
                )
            ),
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="sns_to_slack_relay.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), "lambda_src")),
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={"SLACK_SECRET_NAME": slack_secret},
        )

        # --- Lambda permissions (to read Slack secret) ---
        fn.role.add_to_policy(iam.PolicyStatement(
            actions=["secretsmanager:GetSecretValue"],
            resources=[
                f"arn:aws:secretsmanager:{self.region}:{self.account}:secret:{slack_secret}*"
            ],
        ))

        # --- SNS Subscription ---
        topic.add_subscription(subs.LambdaSubscription(fn))

        # --- EventBridge rule for ECS STOPPED events ---
        pattern = events.EventPattern(
            source=["aws.ecs"],
            detail_type=["ECS Task State Change"],
            detail={
                "clusterArn": [cluster_arn],
                "lastStatus": ["STOPPED"],
                "taskDefinitionFamily": [task_family],
            },
        )

        rule = events.Rule(
            self,
            "EcsStoppedToSns",
            rule_name=f"{env_name}-ecs-stopped-to-sns",
            event_pattern=pattern,
        )

        rule.add_target(targets.SnsTopic(topic))
        topic.grant_publish(iam.ServicePrincipal("events.amazonaws.com"))
