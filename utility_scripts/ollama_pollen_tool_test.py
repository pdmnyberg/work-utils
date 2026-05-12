from ollama import chat
from ollama import ChatResponse
from functools import cache
import datetime
from geopy.distance import distance
import requests
import json


API_ROOT = "https://api.pollenrapporten.se/v1"


@cache
def api_fetch_all(endpoint, params=frozenset([]), api_root=API_ROOT):
    params = dict(params)
    url = f"{api_root}/{endpoint}"
    return list(fetch_all(url, params=params))


def fetch_all(url, params={}):
    response = requests.get(url, params=params)
    while response is not None:
        response.raise_for_status()
        data = response.json()
        for item in data["items"]:
            yield item

        next_url = next(
            (
                link["href"]
                for link in data["_links"]
                if link["rel"] == "next"
            ),
            None
        )
        response = (
            None
            if next_url is None
            else requests.get(next_url)
        )


def get_by_name(items, name):
    item = next((item for item in items if item["name"].lower() == name.lower()), None)
    return item


def get_regions():
    """Gets all the currently available regions

    Returns:
        A list of all currently available regions represented as a list of strings containing regions names
    """
    regions = api_fetch_all("regions")
    return json.dumps([
        region["name"]
        for region in regions
    ])


def get_region_info(region_name: str):
    """Gets information related to a region by name

    Args:
        region_name (str): A string with the name of a region

    Returns:
        The available information about the specified region as a dict with the keys:
        - 'name' (str): The name of the location.
        - 'longitude' (float): The longitude of the location, measured in decimal degrees.
        - 'latitude' (float): The latitude of the location, measured in decimal degrees.
    """

    regions = api_fetch_all("regions")
    return json.dumps(get_by_name(regions, region_name))


def get_pollen_types():
    """Gets all the currently available pollen types

    Returns:
        A list of all currently available pollen types represented as a list of strings containing pollen type names
    """
    pollen_types = api_fetch_all("pollen-types")
    return json.dumps([
        pollen_type["name"]
        for pollen_type in pollen_types
    ])



def get_pollen_info(pollen_name: str):
    """Gets information related to a pollen type by name

    Returns:
        The available information about the specified pollen type as a dict with the keys:
        - 'name' (str): The name of the pollen type.
        - 'thresholdLow' (int): Threshold for low impact on allergies
        - 'thresholdMedium' (int): Threshold for medium impact on allergies
        - 'thresholdHigh' (int): Threshold for high impact on allergies
        - 'thresholdVeryHigh' (int): Threshold for very high impact on allergies
    """

    pollen_types = api_fetch_all("pollen-types")
    return json.dumps(get_by_name(pollen_types, pollen_name))


def get_pollen_count(region_name: str, pollen_name: str, date: datetime.date | str):
    """Gets the pollen count for a given region, pollen and date

    Args:
        region_name (str): A string with the name of a region
        pollen_name (str): A string with the name of a pollen type
        date (datetime.date | str): A date object or an isoformated date string

    Returns:
        The pollen count for the given region, pollen and date as a dict with the keys:
        - 'pollen' (str): The pollen name
        - 'region' (str): The region name
        - 'dailyCount' (int): The number of counted pollen particles
        - 'technicalError' (boolean): Indication if there was a technical error on the specified day
        - 'date': The date as an isoformatted string

        The result is empty when there was no data measured for the given properties.
    """

    region = get_by_name(api_fetch_all("regions"), region_name)
    pollen_type = get_by_name(api_fetch_all("pollen-types"), pollen_name)

    if not region or not pollen_type:
        return None

    date_str = date if isinstance(date, str) else date.isoformat()
    pollen_count = api_fetch_all(
        "pollen-count",
        params=frozenset({
            "region_id": region["id"],
            "pollen_id": pollen_type["id"],
            "start_date": date_str,
            "end_date": date_str
        }.items())
    )
    if len(pollen_count) > 0:
        data = pollen_count[0]
        data.pop("countDescription")
        data.pop("pollenId")
        data.pop("regionId")
        data["region"] = region_name
        data["pollen"] = pollen_name
        return json.dumps(data)
    else:
        return None

def get_distance(coord_a: tuple[float, float], coord_b: tuple[float, float]):
    """Gets the distance between two geographic coordinates in meters

    Args:
        coord_a: A tuple containing longitude and latitude
        coord_b: A tuple containing longitude and latitude

    Returns:
      The distance between the input coordinates in meters
    """
    return str(distance(coord_a, coord_b).meters)


def get_date():
    """Gets the current date as an isoformat string

    Returns:
      The current date as an isoformat string
    """
    return datetime.date.today().isoformat()


def get_time():
    """Gets the current date and time as an isoformat string

    Returns:
      The current date and time as an isoformat string
    """
    return datetime.datetime.now().isoformat()


available_functions = {
  "get_date": get_date,
  "get_time": get_time,
  "get_distance": get_distance,
  "get_regions": get_regions,
  "get_region_info": get_region_info,
  "get_pollen_types": get_pollen_types,
  "get_pollen_info": get_pollen_info,
  "get_pollen_count": get_pollen_count,
}


messages = [
    {
        "role": "user",
        "content": "What was the pollen count for birch in Gävle one week ago? Only use information available in the tools. Describe the result as level of impact on allergies.",
    },
]


while True:
    stream = chat(
        model="qwen3.6",
        messages=messages,
        tools=available_functions.values(),
        think=True,
        stream=True,
    )

    thinking = ''
    content = ''
    tool_calls = []

    done_thinking = False
    # accumulate the partial fields
    for chunk in stream:
        if chunk.message.thinking:
            thinking += chunk.message.thinking
            print(chunk.message.thinking, end='', flush=True)
        if chunk.message.content:
            if not done_thinking:
                done_thinking = True
                print('\n')
            content += chunk.message.content
            print(chunk.message.content, end='', flush=True)
        if chunk.message.tool_calls:
            tool_calls.extend(chunk.message.tool_calls)
            print(chunk.message.tool_calls)

    # append accumulated fields to the messages
    if thinking or content or tool_calls:
        messages.append({'role': 'assistant', 'thinking': thinking, 'content': content, 'tool_calls': tool_calls})

    if not tool_calls:
        break

    for call in tool_calls:
        if call.function.name in available_functions:
            selected_tool = available_functions[call.function.name]
            result = selected_tool(**call.function.arguments)
        else:
            result = 'Unknown tool'
        messages.append({'role': 'tool', 'tool_name': call.function.name, 'content': result})
