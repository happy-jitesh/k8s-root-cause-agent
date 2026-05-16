import time

from analyzer import collect_metrics
from k8s_events import get_events
from k8s_logs import get_logs
from llm_brain import analyze

from kubernetes import client, config

# Load config automatically
try:
    config.load_incluster_config()
except:
    config.load_kube_config()

v1 = client.CoreV1Api()

# Config
NAMESPACE = "prod"
APP_LABEL = "app=latency-app"

CHECK_INTERVAL = 30

# Load prompt
with open("prompts/root_cause_prompt.txt") as f:
    PROMPT = f.read()


def get_target_pod():

    pods = v1.list_namespaced_pod(
        namespace=NAMESPACE,
        label_selector=APP_LABEL
    )

    if not pods.items:
        return None

    return pods.items[0].metadata.name


def controller():

    print("\n🚀 AI Root Cause Analysis Agent Started...\n")

    while True:

        try:

            print("\n================================================")
            print("🔍 Starting New Investigation Cycle")
            print("================================================\n")

            # Step 1 - Get Pod
            pod_name = get_target_pod()

            if not pod_name:
                print("❌ No application pod found")
                time.sleep(CHECK_INTERVAL)
                continue

            print(f"🎯 Target Pod: {pod_name}")

            # Step 2 - Collect Metrics
            print("\n📊 Collecting Prometheus metrics...")

            metrics = collect_metrics()

            print(f"✅ Metrics Collected: {metrics}")

            # Step 3 - Read Logs
            print("\n📄 Reading application logs...")

            logs = get_logs(NAMESPACE, pod_name)

            print("✅ Logs collected")

            # Step 4 - Read Events
            print("\n⚡ Reading Kubernetes events...")

            events = get_events(NAMESPACE)

            print("✅ Events collected")

            # Step 5 - Build Context
            print("\n🧠 Building AI investigation context...")

            context = f"""
METRICS:
{metrics}

EVENTS:
{events}

LOGS:
{logs}
"""

            # Step 6 - AI Analysis
            print("\n🤖 Sending data to Llama3 for root cause analysis...\n")

            result = analyze(context, PROMPT)

            # Step 7 - Output
            print("================================================")
            print("🧠 AI ROOT CAUSE ANALYSIS")
            print("================================================\n")

            print(result)

            print("\n✅ Investigation completed")

        except Exception as e:

            print(f"\n❌ Error during investigation: {e}")

        print(f"\n⏳ Waiting {CHECK_INTERVAL} seconds for next cycle...\n")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    controller()