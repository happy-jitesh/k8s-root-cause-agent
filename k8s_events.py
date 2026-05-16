from kubernetes import client, config

try:
    config.load_incluster_config()
    print("Using in-cluster config")
except:
    config.load_kube_config()
    print("Using local kubeconfig")

v1 = client.CoreV1Api()


def get_events(namespace):

    events = v1.list_namespaced_event(namespace)

    output = []

    for e in events.items:
        output.append(
            f"{e.reason} - {e.message}"
        )

    return "\n".join(output[-20:])