import json
import pandas as pd


def extract_params(data, param_list):
    return_object = {}

    for param in param_list:
        return_object[param] = data.get(param)

    return return_object


def parse(data):

    required_params = ["author_email", "maintainer_email", "name", "requires_dist", "license", "version"]
    key_splitters = ["(", "[", ";", "extra", "pytest"]
    parsed_info = []

    for d in data:
        extracted_info = extract_params(d.get("info", {}).get("info", {}), required_params)
        dependencies = []

        if extracted_info.get("requires_dist") is None:
            parsed_info.append(cleanup(extracted_info))
            continue

        for dependency in extracted_info.get("requires_dist"):
            for key in key_splitters:
                if key not in dependency:
                    continue

                dependency = dependency.split(key)[0].strip()

            if dependency:
                dependencies.append(dependency)

        extracted_info["dependencies"] = dependencies
        parsed_info.append(cleanup(extracted_info))

    return parsed_info


def cleanup(data):
    keys = ["author_email", "maintainer_email", "name",  "license", "version", "dependencies"]

    if data.get("author_email") is None or data.get("author_email").strip() is "":
        data["author_email"] = data["maintainer_email"] if data.get("maintainer_email") else "UNKNOWN"

    if data.get("maintainer_email") is None or data.get("maintainer_email").strip() is "":
        data["maintainer_email"] = data["author_email"] if data.get("author_email") else "UNKNOWN"

    for key in keys:
        data[key] = data[key] if data.get(key) else "UNKNOWN"

    del data["requires_dist"]
    return data


if __name__ == '__main__':
    with open("../data_collector/checkpoint/meta_package_data_2000.json", "r") as f:
        data = json.load(f)

    df = pd.DataFrame(parse(data))
    print(df.author_email.value_counts())

