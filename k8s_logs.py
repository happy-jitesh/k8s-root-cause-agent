from kubernetes import client, config

config.load_incluster_config()

v1 = client.CoreV1Api()

def get_logs(namespace, pod):

    return v1.read_namespaced_pod_log(
        name=pod,
        namespace=namespace,
        tail_lines=20
    )