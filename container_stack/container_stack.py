from aws_cdk import core as cdk
from aws_cdk import aws_eks
from container_stack.util.read_manifest import read_manifests_from_directory


class ContainerStack(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 cluster: aws_eks.Cluster,  # add parameter
                 **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        manifest_directory = './manifests/'
        read_manifests_from_directory(manifest_directory, cluster)

        # # Helm Chart - flux CD
        # cluster.add_helm_chart(
        #     id='flux',
        #     repository='https://charts.fluxcd.io',
        #     chart='flux',
        #     release='flux',
        #     values={
        #         'git.url': 'git@github.com:org/repo'
        #     }
        # )
