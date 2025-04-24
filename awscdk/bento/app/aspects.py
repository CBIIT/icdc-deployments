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
                #roleName = config['iam']['role_prefix'] + '-' + config['main']['resource_prefix'] + '-' + resolvedLogicalId
                roleName = config['iam']['role_prefix'] + '-' + resolvedLogicalId[:30] 
                node.role_name = roleName