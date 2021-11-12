#!/usr/bin/env python3
import os
from aws_cdk import core as cdk
from cdk_eks_pipeline_blueprint.cdk_eks_pipeline_blueprint_stack import CdkEksPipelineBlueprintStack
from environment import Environment
from infra_stacks import vpc_stack
from infra_stacks.vpc_stack import Vpc

env = cdk.Environment(
    account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
    region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"]),
)

app = cdk.App()

# environment = Environment()

# vpc_stack = vpc.Vpc(
#     scope=app,
#     construct_id='eks-cluster-vpc',
#     env=cdk.Environment(
#         account=env.account_id,
#         region=env.region
#     )
# )

# vpc_stack = Vpc(scope=app,
#                 construct_id='VpcAppStack',
#                 env=cdk.Environment(
#                     account=env.account_id,
#                     region=env.region)
#                 )

print(f'%%%%%%%%%%%% app - account: {env.account}, region: {env.region}')


CdkEksPipelineBlueprintStack(
    scope=app,
    construct_id="CdkEksPipelineBlueprintStack",
    env=env
    # env=cdk.Environment(
    #     account=environment.account_id,
    #     region=environment.region
    # ),
    # vpc=vpc_stack.vpc
)

app.synth()
