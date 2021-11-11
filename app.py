#!/usr/bin/env python3
from aws_cdk import core as cdk
from cdk_eks_pipeline_blueprint.cdk_eks_pipeline_blueprint_stack import CdkEksPipelineBlueprintStack
from env import Env
from stacks import vpc_stack
from stacks.vpc_stack import Vpc


app = cdk.App()
env = Env()

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

CdkEksPipelineBlueprintStack(
    scope=app,
    construct_id="CdkEksPipelineBlueprintStack",
    env=cdk.Environment(
        account=env.account_id,
        region=env.region
    ),
    # vpc=vpc_stack.vpc
)

app.synth()
