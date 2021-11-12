from aws_cdk import core as cdk
from infra_stacks.vpc_stack import Vpc


class VpcStage(cdk.Stage):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,  # VpcDev/VpcStage/VpcProd
                 env: cdk.Environment,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Vpc(self, 'VpcStage', env=env)
