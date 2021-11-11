from aws_cdk import core as cdk
from aws_cdk.pipelines import CodePipeline
from aws_cdk.pipelines import CodePipelineSource
from aws_cdk.pipelines import ShellStep
from stages.vpc_stage import VpcStage


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
        # Source
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

        vpc_dev_stage = VpcStage(scope=self,
                                 construct_id='VpcDev',
                                 # env=env
                                 )

        pipeline.add_stage(vpc_dev_stage)

