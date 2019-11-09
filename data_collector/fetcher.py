from json import dump, load
from tqdm import tqdm

import requests
import pypistats


def read_packages():
    with open("python_packages_list.json", "r") as f:
        package_info = load(f)

    return package_info


def get_dependencies(package):
    url = 'https://pypi.org/pypi/{}/json'
    json = requests.get(url.format(package)).json()
    return json


def get_stats(package):
    return pypistats.overall(package, mirrors=True, format="json")


def checkpoint(mega_meta, id):
    with open("checkpoint/meta_package_data_{}.json".format(id), "w") as f:
        dump(mega_meta, f)


if __name__ == '__main__':

    packages = read_packages()
    print(len(packages))

    mega_meta = {}
    partial_meta = {}
    failures = {"deps": [], "stats": []}

    for id, package in tqdm(enumerate(packages)):
        package = package.split("/")[2]

        try:
            deps = get_dependencies(package)
        except:
            failures["deps"].append(package)
            deps = {"status": "Failed"}

        try:
            stats = get_stats(package)
        except:
            failures["stats"].append(package)
            stats = {"status": "Failed"}

        mega_meta[package] = {"info": deps, "stats": stats}
        partial_meta[package] = mega_meta[package]

        if id % 1000 == 0:
            checkpoint(partial_meta, id)
            partial_meta = {}

    checkpoint(mega_meta, "final")
