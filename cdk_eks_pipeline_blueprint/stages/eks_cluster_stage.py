from aws_cdk import core as cdk
from infra_stacks.eks_cluster_stack import EksCluster


class EksClusterStage(cdk.Stage):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,  # EksClusterDev/EksClusterStage/EksClusterProd
                 # vpc: aws_ec2.Vpc,
                 env: cdk.Environment,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print(f'%%%%%%%%%%%% EksClusterStage - account: {env.account}, region: {env.region}')

        eks_cluster_stack = EksCluster(
            self,
            f'{construct_id}Stage',
            env=env
        )

        self._cluster = eks_cluster_stack.cluster

    @property
    def cluster(self):
        return self._cluster

