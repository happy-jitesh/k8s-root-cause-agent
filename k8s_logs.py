from kubernetes import client, config

try:
    config.load_incluster_config()
    print("Using in-cluster config")
except:
    config.load_kube_config()
    print("Using local kubeconfig")

v1 = client.CoreV1Api()


def get_logs(namespace, pod):

    return v1.read_namespaced_pod_log(
        name=pod,
        namespace=namespace,
        tail_lines=50
    )