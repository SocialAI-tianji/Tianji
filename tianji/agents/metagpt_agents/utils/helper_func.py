from tianji import TIANJI_PATH
import json
import os


def load_json(file_name):
    with open(
        os.path.join(
            TIANJI_PATH, "tianji", "agents", "metagpt_agents", "utils", file_name
        ),
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def extract_all_types(json_data):
    scene_types = json_data.get("scene_types", {})
    types = [scene_types[key]["type"] for key in scene_types]
    return types


def extract_single_type_attributes_and_examples(json_data, type_number):
    scene_types = json_data.get("scene_types", {})
    for key, value in scene_types.items():
        if value["type"].startswith(type_number + "："):
            return value["type"], value["attributes"], value["example"]
    return None, None, None


def extract_all_types_and_examples(json_data):
    scene_types = json_data.get("scene_types", {})
    types_and_examples = {
        value["type"]: value["example"] for key, value in scene_types.items()
    }
    return types_and_examples


def extract_attribute_descriptions(json_data, attributes):
    attribute_descriptions = json_data.get("attribute_descriptions", {})
    descriptions = {attr: attribute_descriptions.get(attr) for attr in attributes}
    return descriptions


def has_empty_values(dict):
    for value in dict.values():
        if value == "" or value is None:
            return True
    return False


def is_number_in_types(json_data, number):
    scene_types = json_data.get("scene_types", {})
    for key, value in scene_types.items():
        if value.get("type", "").startswith(str(number) + "："):
            return True
