from aws_cdk import core as cdk
from aws_cdk import aws_iam
from aws_cdk import aws_eks
from aws_cdk import aws_ec2
from stacks.vpc_stack import Vpc


class EksCluster(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 env: cdk.Environment,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print(f'%%%%%%%%%%%% EksCluster - account: {env.account}, region: {env.region}')


        ### ここでVPCをつくる!!
        vpc = Vpc(self, 'VpcStage', env=env)


        # vpc = aws_ec2.Vpc.from_lookup(
        #     self,
        #     'EksClusterVPC',
        #     # 'VPC',
        #     # region=env.region,
        #     # region=environment.region,
        #     vpc_id='vpc-0be974edc7bd76d12')
        #     # vpc_name='VpcStage/VPC')
        #     # vpc_name='CdkEksPipelineBlueprintStack/VpcDev/VpcStage/VPC')
        # print(f'-----------EksCluster Stack from_lookup() vpc.vpc_id={vpc.vpc_id}')

        # Pipelineで動作しない。
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

        # eks_cluster_admin_role = aws_iam.Role(
        #     scope=self,
        #     id="EksClusterRoleAdmin",
        #     role_name='EksClusterRoleAdmin',
        #     assumed_by=aws_iam.CompositePrincipal(
        #         aws_iam.ServicePrincipal(service='eks.amazonaws.com'),
        #         aws_iam.ServicePrincipal(service='arn:aws:iam::{}:root'.format(environment.account_id))),
        #     managed_policies=[
        #         aws_iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AdministratorAccess'),
        #         aws_iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AmazonEKSClusterPolicy'),
        #         aws_iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AmazonEKSServicePolicy')]
        # )
        # eks_cluster_admin_role = aws_iam.Role(
        #     scope=self,
        #     id="EksClusterRoleAdmin",
        #     role_name='EksClusterRoleAdmin',
        #     assumed_by=aws_iam.ServicePrincipal(service='eks.amazonaws.com'),
        #     managed_policies=[
        #         aws_iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AdministratorAccess'),
        #         aws_iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AmazonEKSClusterPolicy'),
        #         aws_iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AmazonEKSServicePolicy')]
        # )

        print(f'%%%%%%%%%%%% 222 EksCluster - account: {env.account}, region: {env.region}')

        # Creating Cluster with EKS
        self.cluster = aws_eks.Cluster(
            scope=self,
            id='EksCluster',
            cluster_name='EksCluster',
            output_cluster_name=True,
            version=aws_eks.KubernetesVersion.V1_21,
            endpoint_access=aws_eks.EndpointAccess.PUBLIC,
            vpc=vpc,  # from_lookupがまだ使えないかも。なので
            # vpc='vpc-0be974edc7bd76d12',
            ### SubnetSelectionで取れない模様
            # vpc_subnets=[
            #     # aws_ec2.SubnetSelection(
            #     #     subnet_type=aws_ec2.SubnetType.PUBLIC),
            #     aws_ec2.SubnetSelection(
            #         subnet_type=aws_ec2.SubnetType.PRIVATE)
            # ],
            masters_role=owner_role,
            # masters_role=eks_cluster_admin_role,
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
