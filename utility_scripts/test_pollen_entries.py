import csv
import json
import sys
from contextlib import contextmanager
from collections import OrderedDict, defaultdict
import requests
import datetime
import re


def fetch_all(url: str):
    next_url = url
    while next_url:
        response = requests.get(next_url)
        data = response.json()
        print(f"fetch: {next_url}: {data['_meta']['offset']}/{data['_meta']['totalRecords']}")
        for item in data["items"]:
            yield item

        if len(data["items"]) > 0:
            print(data["items"][0].get("date"), data["items"][-1].get("date"))

        next_link = next((
            link
            for link in data["_links"]
            if link["rel"] == "next"
        ), None)
        next_url = next_link["href"] if next_link else None


def date_key(d):
    return d["date"]


def get_base_url(url):
    return re.match(r"(http(s:|:)//.+/v1)/.*", url)[1]


def check_context(url):
    base_url = get_base_url(url)
    regions = list(fetch_all(f"{base_url}/regions"))
    region_names = {
        region["id"]: region["name"]
        for region in regions
    }
    pollen_types = list(fetch_all(f"{base_url}/pollen-types"))
    pollen_names = {
        pollen["id"]: pollen["name"]
        for pollen in pollen_types
    }
    data = list(fetch_all(url))
    acc = OrderedDict()
    for d in sorted(data, key=date_key):
        key = (d["regionId"], d["date"])
        acc[key] = acc.get(key, 0) + 1
        #acc[key].append((d["pollenId"], d["dailyCount"]))

    check = dict()
    errors = dict()
    for (region, date_str), value in acc.items():
        region_name = region_names[region]
        date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        key = (region_name, region, date.year)
        check_value = check.get(key)
        if check_value is None:
            check[key] = value
        elif not check_value == value:
            error = errors.get(key, [])
            errors[key] = error
            error.append((date_str, value))
    
    for key, error in errors.items():
        #print(key, error)
        pass
    
    value_dict = {
        (d["regionId"], d["date"], d["pollenId"]): d["dailyCount"]
        for d in data
    }
    #print(value_dict)
    region_dates = defaultdict(set)
    for region, date_str, _p in value_dict.keys():
        region_dates[region].update({date_str})

    region_pollen = defaultdict(set)
    for region, _d, pollen in value_dict.keys():
        region_pollen[region].update({pollen})

    region_date_values = defaultdict(lambda: defaultdict(int))
    for (region, date_str, pollen), value in value_dict.items():
        region_date_values[(region, date_str)][pollen] = value

    all_counts = set()
    for region, date_set in region_dates.items():
        pollen_set = region_pollen[region]
        print(region_names[region], region, len(date_set), len(pollen_set))
        region_counts = defaultdict(set)
        for date_str in sorted(date_set):
            (year, *_date) = date_str.split("-")
            pollen_list = [
                pollen_names[p]
                for p in region_date_values[(region, date_str)].keys()
            ]
            region_counts[year].update({len(pollen_list)})
            all_counts.update({len(pollen_list)})
            #print(f"  - {date_str} {len(pollen_list)}")
        print(f"  - region counts: {region_counts}")
        for pollen in pollen_set:
            print(f"  - {pollen_names[pollen]}")

    print(all_counts)

    region_set = set(
        region
        for region, _d, _p in value_dict.keys()
    )
    return

    for region in region_set:
        pollen_set = region_pollen[region]
        print(region_names[region])
        print(",".join([
            "datum",
            *[
                pollen_names[pollen]
                for pollen in pollen_set
            ]
        ]))
        date_set = region_dates[region]
        for d in date_set:
            print(",".join([
                d,
                *[
                    str(value_dict.get((region, d, pollen), "-"))
                    for pollen in pollen_set
                ]
            ]))


def first_report(url):
    base_url = get_base_url(url)
    regions = list(fetch_all(f"{base_url}/regions"))
    region_names = {
        region["id"]: region["name"]
        for region in regions
    }
    pollen_types = list(fetch_all(f"{base_url}/pollen-types"))
    pollen_names = {
        pollen["id"]: pollen["name"]
        for pollen in pollen_types
    }
    data = list(fetch_all(url))

    non_zero_entries = {
        (
            region_names.get(forecast["regionId"], forecast["regionId"]),
            pollen_names.get(entry["pollenId"], entry["pollenId"]),
            datetime.datetime.strptime(entry["time"], "%Y-%m-%dT%H:%M:%S")
        )
        for forecast in data
        for entry in forecast["levelSeries"]
        if entry["level"] > 0
    }

    non_zero_regions = {region for (region, _p, _d) in non_zero_entries}
    non_zero_pollen = {pollen for (_r, pollen, _d) in non_zero_entries}
    non_zero_years = {date.year for (_r, _p, date) in non_zero_entries}
    for year in non_zero_years:
        for region in non_zero_regions:
            print(f"{region}: {year}")
            for pollen in non_zero_pollen:
                non_zero_dates = [
                    date
                    for (r, p, date) in non_zero_entries
                    if r == region and p == pollen and date.year == year
                ]
                if len(non_zero_dates) > 0:
                    print(f" - {pollen}: {min(non_zero_dates)} - {max(non_zero_dates)}")
                else:
                    print(f" - {pollen}: No data")





def main(command, *argv):
    actions = {
        "check-context": check_context,
        "first-report": first_report
    }
    action = actions[command]
    action(*argv)


main(*sys.argv[1:])
