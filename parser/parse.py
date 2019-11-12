import json


def extract_params(data, param_list):
    return_object = {}

    for param in param_list:
        return_object[param] = data.get(param)

    return return_object


def parse():
    with open("../data_collector/checkpoint/meta_package_data_0.json", "r") as f:
        data = json.load(f)

    required_params = ["author_email", "maintainer_email", "name", "requires_dist", "license", "version"]

    key_splitters = ["(", "[", ";", "extra", "pytest"]

    for d in data:
        extracted_info = extract_params(d.get("info", {}).get("info", {}), required_params)
        dependencies = []

        if extracted_info.get("requires_dist") is None:
            continue

        for dependency in extracted_info.get("requires_dist"):
            for key in key_splitters:
                if key not in dependency:
                    continue

                dependency = dependency.split(key)[0].strip()

            if dependency:
                dependencies.append(dependency)

        print(extracted_info.get("requires_dist"))
        print(dependencies)
        print("----------")


if __name__ == '__main__':
    parse()
