#!/usr/bin/env python3
import os
from aws_cdk import core as cdk
from cdk_eks_pipeline_blueprint.cdk_eks_pipeline_blueprint_stack import CdkEksPipelineBlueprintStack

env = cdk.Environment(
    account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
    region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"]),
)

app = cdk.App()

CdkEksPipelineBlueprintStack(
    scope=app,
    construct_id="CdkEksPipelineBlueprintStack",
    env=env
)

app.synth()
