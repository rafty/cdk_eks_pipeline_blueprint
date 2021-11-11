from aws_cdk import core as cdk
from aws_cdk.pipelines import CodePipeline
from aws_cdk.pipelines import CodePipelineSource
from aws_cdk.pipelines import ShellStep
from stages.vpc_stage import VpcStage
from stages.eks_cluster_stage import EksClusterStage


class CdkEksPipelineBlueprintStack(cdk.Stack):
    # ----------------------------------------
    # Pipeline Stack for EKS
    # ----------------------------------------
    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 env: cdk.Environment,
                 **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        # ----------------------------------------
        # Source
        # ----------------------------------------
        repository_name = self.node.try_get_context('repository-name')
        github_action = self.node.try_get_context('github-action')

        github_connection = CodePipelineSource.connection(
            repo_string=repository_name,
            branch='master',
            connection_arn=github_action
        )

        # ----------------------------------------
        # Pipeline
        # ----------------------------------------
        pipeline_name = self.node.try_get_context('pipeline-name')

        pipeline = CodePipeline(
            scope=self,
            id='EksPipeline',
            pipeline_name=pipeline_name,
            self_mutation=True,
            synth=ShellStep(
                id='Synth',
                input=github_connection,
                commands=[
                    'npm install -g aws-cdk',
                    'python -m pip install -r requirements.txt',
                    'cdk synth'
                ],
            ),
        )

        # # ----------------------------------------
        # # VPC Stage
        # # ----------------------------------------
        # vpc_dev_stage = VpcStage(scope=self, construct_id='VpcDev')
        # pipeline.add_stage(vpc_dev_stage)
        # # TODO これをstageからappのstackに移動し、dev/stage/prodを作成する。

        # ----------------------------------------
        # EKS Cluster Stage
        # ----------------------------------------
        eks_cluster_dev_stage = EksClusterStage(scope=self, construct_id='EksClusterDev')
        pipeline.add_stage(eks_cluster_dev_stage)
