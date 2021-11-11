from aws_cdk import core as cdk
# from stacks.vpc_stack import Vpc
from stacks.eks_cluster_stack import EksCluster
from aws_cdk import aws_ec2


class EksClusterStage(cdk.Stage):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,  # EksClusterDev/EksClusterStage/EksClusterProd
                 # vpc: aws_ec2.Vpc,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print(f'-----------EksClusterStage construct_id={construct_id}')

        app_stack = EksCluster(self, 'EksClusterStage')
