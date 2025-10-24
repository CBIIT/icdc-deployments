#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.notify_stack import NotifyStack

app = cdk.App()

# Define environment (default to dev)
env_name = app.node.try_get_context("env") or "dev"

NotifyStack(
    app,
    f"DataRetrieverNotifyStack-{env_name}",
    env_name=env_name,
)

app.synth()
