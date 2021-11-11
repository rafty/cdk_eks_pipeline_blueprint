from aws_cdk import core as cdk
from aws_cdk import aws_iam
from aws_cdk import aws_eks
from aws_cdk import aws_ec2
from env import Env

environment = Env()


class EksCluster(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 # vpc: aws_ec2.Vpc,
                 # env: cdk.Environment,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print(f'-----------EksCluster Stack construct_id={construct_id}')

        # Import our existing VPC whose name is EKSClusterStack/VPC

        # cdk_eks_vpcAz = cdk.Fn.import_value("cdkEksVpcAz").split(",")
        # cdk_eks_vpcId = cdk.Fn.import_value("cdkEksVpcId")
        # cdk_eks_clusterName = cdk.Fn.import_value("cdkEksClusterName")
        # cdk_eks_kubectlRoleArn = cdk.Fn.import_value("cdkEksKubectlRoleArn")
        # cdk_eks_securityGroupId = cdk.Fn.import_value("cdkEksSgId")
        # cdk_eks_oidcProviderArn = cdk.Fn.import_value("cdkEksOidcProviderARN")
        #
        # vpc = aws_ec2.Vpc.from_vpc_attributes(
        #     self, "{}-vpc".format(construct_id), vpc_id=cdk_eks_vpcId, availability_zones=cdk_eks_vpcAz)

        vpc = aws_ec2.Vpc.from_lookup(
            self,
            'VPC',
            # region=env.region,
            region=environment.region,
            # vpc_name='VPC')
            vpc_name='CdkEksPipelineBlueprintStack/VpcDev/VpcStage/VPC')

        print(f'-----------EksCluster Stack from_lookup() construct_id={construct_id}')

        # vpc_id = cdk.Fn.import_value('eks-cluster-vpc-id')
        # # print(f'----------------vpc_id: {vpc_id}')
        # vpc = aws_ec2.Vpc.from_lookup(self, 'VPC', vpc_id=vpc_id)
        # print(f'----------------from_lookup - vpc.vpc_id: {vpc.vpc_id}')

        # Create owner role for EKS Cluster
        owner_role = aws_iam.Role(
            scope=self,
            id='EksClusterOwnerRole',
            role_name='EksClusterOwnerRole',
            assumed_by=aws_iam.AccountRootPrincipal()
        )

        # Creating Cluster with EKS
        self.cluster = aws_eks.Cluster(
            scope=self,
            id='EksCluster',
            cluster_name='EksCluster',
            output_cluster_name=True,
            version=aws_eks.KubernetesVersion.V1_21,
            endpoint_access=aws_eks.EndpointAccess.PUBLIC,
            vpc=vpc,
            vpc_subnets=[
                # aws_ec2.SubnetSelection(
                #     subnet_type=aws_ec2.SubnetType.PUBLIC),
                aws_ec2.SubnetSelection(
                    subnet_type=aws_ec2.SubnetType.PRIVATE)
            ],
            masters_role=owner_role,
            # default_capacity=2,
            # default_capacity_instance=aws_ec2.InstanceType.of(
            #     aws_ec2.InstanceClass.BURSTABLE2,
            #     aws_ec2.InstanceSize.MICRO),
            # default_capacity_instance=(
            #     aws_ec2.InstanceType('t2.large')
            #     if cdk.Stack.of(self).region == 'ap-northeast-1'
            #     else aws_ec2.InstanceType('t3.large')
            # )
        )

        # # Self-managed nodes
        # self.cluster.add_auto_scaling_group_capacity(
        #     id='self-managed-node-group',
        #     instance_type=aws_ec2.InstanceType('t3.large'),
        #     max_capacity=10
        # )

    @property
    def get_cluster(self):
        return self.cluster
