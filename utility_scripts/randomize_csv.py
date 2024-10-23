import csv
import random


def default_itemizer(value):
    return (value,)


def default_selector(value_set):
    return (
        random.choice(tuple(value_set))
        if len(value_set) > 0
        else ""
    )


def static_selector(value):
    def _static_selector(_value_set):
        return value
    
    return _static_selector


def split_itemizer(key=","):
    def _split_itemizer(value):
        return (
            item.strip()
            for item in value.split(key)
            if item.strip()
        )
    return _split_itemizer


def multi_selector(joiner=", ", max_items=3):
    def _multi_selector(value_set):
        count = min(
            random.randrange(max_items),
            len(value_set)
        )
        return joiner.join(
            random.sample(list(value_set), count)
        ) if len(value_set) > 0 else ""
    return _multi_selector


def id_selector_generator():
    id_set = set()
    def _id_creator_selector(value_set):
        used_id = default_selector(value_set)
        id_set.add(used_id)
        return used_id
    
    def _id_selector(_value_set):
        return default_selector(id_set)
    
    return (_id_creator_selector, _id_selector)


def create_data_profile(path: str, itemizers: dict, include_empty=False):
    with open(path, "r") as file:
        reader = csv.DictReader(file)
        sets = dict()
        for row in reader:
            for header, value in row.items():
                itemizer = itemizers.get(header, default_itemizer)
                current_set = sets.get(header, set())
                items = itemizer(value)
                for item in items:
                    if item or include_empty:
                        current_set.add(item)
                sets[header] = current_set
        return sets


def generate_entry(profile: dict, selectors: dict):
    return {
        header: selectors.get(header, default_selector)(header_set)
        for header, header_set in profile.items()
    }


def generate_data(profile: dict, selectors: dict, entries=10):
    return [
        generate_entry(profile, selectors)
        for i in range(entries)
    ]
        

def write_data(path: str, data: list):
    with open(path, "w") as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for entry in data:
            writer.writerow(entry)


def tango_data(root=".", out="../example-data"):
    (id_creator_selector, id_selector) = id_selector_generator()
    generators = (
        (
            "tango_events",
            {
                "funding": split_itemizer(),
                "target_audience": split_itemizer(),
                "additional_platforms": split_itemizer(),
                "communities": split_itemizer(),
                "organising_institution": split_itemizer(),
            },
            {
                "code": id_creator_selector,
                "date_start": static_selector("2023-01-01"),
                "date_end": static_selector("2023-01-10"),
                "funding": multi_selector(),
                "target_audience": multi_selector(),
                "additional_platforms": multi_selector(),
                "communities": multi_selector(),
                "organising_institution": multi_selector(),
            },
            20
        ),
        (
            "tango_demographics",
            {"heard_from": split_itemizer()},
            {
                "event": id_selector,
                "heard_from": multi_selector()
            },
            200
        ),
        (
            "tango_impacts",
            {
                "help_work": split_itemizer(),
                "attending_led_to": split_itemizer()
            },
            {
                "event": id_selector,
                "help_work": multi_selector(),
                "attending_led_to": multi_selector()
            },
            200
        ),
        (
            "tango_qualities",
            dict(),
            {"event": id_selector},
            200
        ),
    )
    for file_id, itemizers, selectors, entries in generators:
        in_path = f"{root}/{file_id}.csv"
        out_path = f"{out}/{file_id}.csv"
        print(f"Generating {in_path} -> {out_path}")
        profile = create_data_profile(in_path, itemizers)
        data = generate_data(profile, selectors, entries)
        write_data(out_path, data)


tango_data()