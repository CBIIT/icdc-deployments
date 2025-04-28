import aws_cdk as cdk
import jsii
from constructs import Construct, IConstruct
from configparser import ConfigParser
from aws_cdk import aws_iam as iam

@jsii.implements(cdk.IAspect)
class MyAspect:
    def visit(self, node):
        # Read config file
        config = ConfigParser()
        config.read('config.ini')

        if isinstance(node, iam.CfnRole):
            if config.has_option('iam', 'role_prefix'):
                resolvedLogicalId = cdk.Stack.of(node).resolve(node.logical_id)
                base_role_name = config['iam']['role_prefix'] + '-' + resolvedLogicalId

                # IAM role name must be <= 64 characters
                if len(base_role_name) > 64:
                    max_logical_id_length = 64 - len(config['iam']['role_prefix']) - 1 
                    resolvedLogicalId_truncated = resolvedLogicalId[:max_logical_id_length]
                    base_role_name = config['iam']['role_prefix'] + '-' + resolvedLogicalId_truncated

                node.role_name = base_role_name
