from aws_cdk import core as cdk
from aws_cdk import aws_ec2


class Vpc(cdk.Stack):

    def __init__(
            self,
            scope: cdk.Construct,
            construct_id: str,
            **kwargs
    ) -> None:

        super().__init__(scope, construct_id, **kwargs)

        self.vpc = aws_ec2.Vpc(
            scope=self,
            id="VPC",
            max_azs=2,
            cidr="10.10.0.0/16",
            # configuration will create 3 groups in 2 AZs = 6 subnets.
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    subnet_type=aws_ec2.SubnetType.PUBLIC,
                    name="Public",
                    cidr_mask=24),
                aws_ec2.SubnetConfiguration(
                    subnet_type=aws_ec2.SubnetType.PRIVATE,
                    name="Private",
                    cidr_mask=24),
                # aws_ec2.SubnetConfiguration(
                #     subnet_type=aws_ec2.SubnetType.ISOLATED,
                #     name="DB",
                #     cidr_mask=24)
            ],
            # nat_gateway_provider=aws_ec2.NatProvider.gateway(),
            nat_gateways=2,
        )

        # EKS Stackへ渡すため
        cdk.CfnOutput(
            scope=self,
            id='eks-cluster-vpc-id',
            export_name='eks-cluster-vpc-id',
            value=self.vpc.vpc_id)

    @property
    def get_vpc(self):
        return self.vpc

    @property
    def get_vpc_public_subnet_ids(self):
        return self.vpc.select_subnets(
            subnet_type=aws_ec2.SubnetType.PUBLIC
        ).subnet_ids

    @property
    def get_vpc_private_subnet_ids(self):
        return self.vpc.select_subnets(
            subnet_type=aws_ec2.SubnetType.PRIVATE
        ).subnet_ids
