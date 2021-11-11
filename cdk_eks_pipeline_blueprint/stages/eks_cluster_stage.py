from aws_cdk import core as cdk
# from stacks.vpc_stack import Vpc
from stacks.eks_cluster_stack import EksCluster
from aws_cdk import aws_ec2
from env import Env

environment = Env()


class EksClusterStage(cdk.Stage):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,  # EksClusterDev/EksClusterStage/EksClusterProd
                 # vpc: aws_ec2.Vpc,
                 # env: cdk.Environment,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print(f'-----------EksClusterStage construct_id={construct_id}')

        # app_stack = EksCluster(self, 'EksClusterStage')
        # app_stack = EksCluster(self, f'{construct_id}Stage')
        app_stack = EksCluster(
            self,
            f'{construct_id}Stage',
            env=cdk.Environment(
                account=environment.account_id,
                region=environment.region
            )
        )
        # app_stack = EksCluster(
        #     self,
        #     f'{construct_id}Stage',
        #     env=cdk.Environment(
        #         account=env.account_id,
        #         region=env.region
        #     ),
        # )
