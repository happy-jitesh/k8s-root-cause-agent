from analyzer import collect_metrics
from k8s_events import get_events
from k8s_logs import get_logs
from llm_brain import analyze

from kubernetes import client, config

config.load_incluster_config()

v1 = client.CoreV1Api()

with open("prompts/root_cause_prompt.txt") as f:
    PROMPT = f.read()

namespace = "prod"

pods = v1.list_namespaced_pod(
    namespace,
    label_selector="app=latency-app"
)

pod_name = pods.items[0].metadata.name

metrics = collect_metrics()

logs = get_logs(namespace, pod_name)

events = get_events(namespace)

context = f"""
METRICS:
{metrics}

EVENTS:
{events}

LOGS:
{logs}
"""

result = analyze(context, PROMPT)

print("\n🧠 ROOT CAUSE ANALYSIS\n")
print(result)