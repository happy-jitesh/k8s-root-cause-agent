import requests
from config import PROMETHEUS_URL

def query(query):

    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={"query": query}
    )

    return response.json()["data"]["result"]