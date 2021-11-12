import os
import glob
import yaml
from aws_cdk import aws_eks


def get_manifest_files(directory: str) -> list:
    files = glob.glob(directory+'*.yaml')
    return files


def load_docs_from_manifest_file(manifest_file):
    with open(manifest_file, 'r', encoding='utf-8') as stream:
        manifest_docs = list(
            yaml.load_all(stream, Loader=yaml.FullLoader))
    return manifest_docs


def file_name_without_extension(manifest_file_path):
    file_name = os.path.basename(manifest_file_path)
    file_name_without_ext = os.path.splitext(file_name)[0]
    return file_name_without_ext


def read_manifests_from_directory(directory: str, cluster: aws_eks.Cluster):

    manifest_files = get_manifest_files(directory)

    for manifest_file in manifest_files:
        name = file_name_without_extension(manifest_file)
        docs = load_docs_from_manifest_file(manifest_file)

        previous_k8s_resource = None
        for i, doc in enumerate(docs):
            k8s_resource = cluster.add_manifest(f'{name}_{i}', doc)
            if previous_k8s_resource:
                k8s_resource.node.add_dependency(previous_k8s_resource)
            previous_k8s_resource = k8s_resource
