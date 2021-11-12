from aws_cdk import core as cdk
from aws_cdk import aws_iam
from aws_cdk import aws_eks
from infra_stacks.vpc_stack import Vpc


class EksCluster(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 env: cdk.Environment,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print(f'%%%%%%%%%%%% EksCluster - account: {env.account}, region: {env.region}')

        # Pipelineで動作しない。
        # vpc_id = cdk.Fn.import_value('eks-cluster-vpc-id')
        # # print(f'----------------vpc_id: {vpc_id}')

        # Pipelineで動作しない。
        # vpc = aws_ec2.Vpc.from_lookup(self, 'VPC', vpc_id=vpc_id)
        # print(f'----------------from_lookup - vpc.vpc_id: {vpc.vpc_id}')

        # 上記が動作しないのでここでVPCをつくる!!
        vpc = Vpc(self, 'VpcStage', env=env)

        # Create owner role for EKS Cluster
        owner_role = aws_iam.Role(
            scope=self,
            id='EksClusterOwnerRole',
            role_name='EksClusterOwnerRole',
            assumed_by=aws_iam.AccountRootPrincipal()
        )

        # Creating Cluster with EKS
        self._cluster = aws_eks.Cluster(
            scope=self,
            id='EksCluster',
            cluster_name='EksCluster',
            output_cluster_name=True,
            version=aws_eks.KubernetesVersion.V1_21,
            endpoint_access=aws_eks.EndpointAccess.PUBLIC,
            vpc=vpc.vpc,  # from_lookupがまだ使えないかも。なので
            ### SubnetSelectionで取れない模様
            # vpc_subnets=[
            #     # aws_ec2.SubnetSelection(
            #     #     subnet_type=aws_ec2.SubnetType.PUBLIC),
            #     aws_ec2.SubnetSelection(
            #         subnet_type=aws_ec2.SubnetType.PRIVATE)
            # ],
            vpc_subnets=vpc.private_subnets,
            masters_role=owner_role,
            # default_capacity=2,
        )

    @property
    def cluster(self):
        return self._cluster
