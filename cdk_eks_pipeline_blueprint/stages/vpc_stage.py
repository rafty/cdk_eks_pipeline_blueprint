from aws_cdk import core as cdk
from stacks.vpc_stack import Vpc


class VpcStage(cdk.Stage):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,  # VpcDev/VpcStage/VpcProd
                 env: cdk.Environment,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print(f'-----------MyAppStage construct_id={construct_id}')

        app_stack = Vpc(self, 'VpcStage')
