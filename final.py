import boto3
from kubernetes import client, config
from botocore.exceptions import NoCredentialsError

def connect_to_eks(cluster_name):
    # Create an EKS client using boto3
    eks_client = boto3.client('eks')

    try:
        # Get the cluster details
        cluster_info = eks_client.describe_cluster(name=cluster_name)
        cluster_endpoint = cluster_info['cluster']['endpoint']
        cluster_ca = cluster_info['cluster']['certificateAuthority']['data']

        # Set up the kubeconfig
        kubeconfig = {
            'apiVersion': 'v1',
            'clusters': [
                {
                    'cluster': {
                        'server': cluster_endpoint,
                        'certificate-authority-data': cluster_ca,
                    },
                    'name': cluster_name,
                }
            ],
            'contexts': [
                {
                    'context': {
                        'cluster': cluster_name,
                        'user': cluster_name,
                    },
                    'name': cluster_name,
                }
            ],
            'current-context': cluster_name,
            'kind': 'Config',
            'preferences': {},
            'users': [
                {
                    'name': cluster_name,
                    'user': {
                        'exec': {
                            'apiVersion': 'client.authentication.k8s.io/v1beta1',
                            'command': 'aws',
                            'args': [
                                'eks',
                                'get-token',
                                '--cluster-name', cluster_name
                            ],
                        }
                    }
                }
            ],
        }

        # Write kubeconfig to a file
        with open('kubeconfig.yaml', 'w') as kubeconfig_file:
            import yaml
            yaml.dump(kubeconfig, kubeconfig_file)

        # Load the kubeconfig
        config.load_kube_config('kubeconfig.yaml')

        # Test connection by listing namespaces
        v1 = client.CoreV1Api()
        namespaces = v1.list_namespace()
        for ns in namespaces.items:
            print(f"Namespace: {ns.metadata.name}")

    except NoCredentialsError:
        print("No AWS credentials found. Make sure you have configured AWS CLI.")
    except Exception as e:
        print(f"Error connecting to EKS: {str(e)}")

# Example usage
connect_to_eks('dev-pipeline')

