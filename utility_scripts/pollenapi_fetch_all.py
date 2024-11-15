import requests
import json
import sys

def fetch_all(url: str):
    next_url = url
    while next_url:
        response = requests.get(next_url)
        data = response.json()
        for item in data["items"]:
            yield item

        next_link = next((
            link
            for link in data["_links"]
            if link["rel"] == "next"
        ), None)
        next_url = next_link["href"] if next_link else None


if __name__ == "__main__":
    try:
        url = sys.argv[1]
        all_items = list(fetch_all(url))
        print(json.dumps(all_items))
    except IndexError:
        print("Provide a PollenAPI URL as the first argument")