from prometheus_client import query

def collect_metrics():

    cpu_query = '''
sum(rate(container_cpu_usage_seconds_total{namespace="prod"}[1m]))
'''

    cpu = query(cpu_query)

    return {
        "cpu": cpu
    }