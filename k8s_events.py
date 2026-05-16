from kubernetes import client, config

config.load_incluster_config()

v1 = client.CoreV1Api()

def get_events(namespace):

    events = v1.list_namespaced_event(namespace)

    output = []

    for e in events.items:
        output.append(
            f"{e.reason} - {e.message}"
        )

    return "\n".join(output[-20:])