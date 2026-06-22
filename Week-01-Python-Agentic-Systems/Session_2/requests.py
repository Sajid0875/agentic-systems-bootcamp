import requests

url = "https://api.github.com/search/repositories"

params = {
    "q": "langgraph",
    "sort": "stars"
}

headers = {
    "Accept": "application/vnd.github+json"
}

try:
    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    print("Total Repositories:", data["total_count"])

except requests.exceptions.Timeout:
    print("Request timed out")

except requests.exceptions.HTTPError as error:
    print("HTTP Error:", error)

except requests.exceptions.RequestException as error:
    print("Request Failed:", error)