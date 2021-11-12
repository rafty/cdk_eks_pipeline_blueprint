from aws_cdk import core as cdk
from aws_cdk import aws_eks
from container_stack.container_stack import ContainerStack


class ContainerStage(cdk.Stage):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,  # EksClusterDev/EksClusterStage/EksClusterProd
                 env: cdk.Environment,
                 cluster: aws_eks.Cluster,
                 **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        print(f'%%%%%%%%%%%% ContainerStage - account: {env.account}, region: {env.region}')

        ContainerStack(
            self,
            'ContainerStage',
            env=env,
            cluster=cluster
        )
