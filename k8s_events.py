from kubernetes import client, config

try:
    config.load_incluster_config()
except:
    config.load_kube_config()

v1 = client.CoreV1Api()


IGNORE_EVENTS = [
    "Pulled",
    "Created",
    "Started",
    "Scheduled"
]


def get_events(namespace):

    events = v1.list_namespaced_event(namespace)

    output = []

    for e in events.items:

        if e.reason in IGNORE_EVENTS:
            continue

        output.append(
            f"{e.reason} - {e.message}"
        )

    return "\n".join(output[-10:])