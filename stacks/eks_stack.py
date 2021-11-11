from aws_cdk import core as cdk
from aws_cdk import aws_iam
from aws_cdk import aws_eks
from aws_cdk import aws_ec2


class EksStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str,
                 vpc: aws_ec2.Vpc,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create owner role for EKS Cluster
        owner_role = aws_iam.Role(
            scope=self,
            id='ClusterOwnerRole',
            role_name='ClusterOwnerRole',
            assumed_by=aws_iam.AccountRootPrincipal()
        )

        # Creating Cluster with EKS
        self.cluster = aws_eks.Cluster(
            scope=self,
            id='EKS-cluster',
            cluster_name='EKS-cluster',
            output_cluster_name=True,
            version=aws_eks.KubernetesVersion.V1_21,
            endpoint_access=aws_eks.EndpointAccess.PUBLIC,
            vpc=vpc,
            vpc_subnets=[
                aws_ec2.SubnetSelection(
                    subnet_type=aws_ec2.SubnetType.PUBLIC),
                aws_ec2.SubnetSelection(
                    subnet_type=aws_ec2.SubnetType.PRIVATE)
            ],
            masters_role=owner_role,
            default_capacity=2,
            # default_capacity_instance=aws_ec2.InstanceType.of(
            #     aws_ec2.InstanceClass.BURSTABLE2,
            #     aws_ec2.InstanceSize.MICRO),
            default_capacity_instance=(
                aws_ec2.InstanceType('t2.large')
                if cdk.Stack.of(self).region == 'ap-northeast-1'
                else aws_ec2.InstanceType('t3.large')
            )
        )

        # Self-managed nodes
        self.cluster.add_auto_scaling_group_capacity(
            id='self-managed-node-group',
            instance_type=aws_ec2.InstanceType('t3.large'),
            max_capacity=10
        )

    @property
    def get_cluster(self):
        return self.cluster
