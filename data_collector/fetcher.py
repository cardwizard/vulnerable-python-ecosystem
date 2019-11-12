from json import dump, load, loads
from tqdm import tqdm
from joblib import Parallel, delayed, parallel_backend

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
    return loads(pypistats.overall(package, mirrors=True, format="json"))


def checkpoint(mega_meta, id):
    with open("checkpoint/meta_package_data_{}.json".format(id), "w") as f:
        dump(mega_meta, f, indent=4)


def get_package_stats(package):

    package = package.split("/")[2]

    try:
        deps = get_dependencies(package)
    except:
        deps = {"status": "Failed"}

    try:
        # stats = get_stats(package)
        stats = {}
    except:
        stats = {"status": "Failed"}

    return {"info": deps, "stats": stats}


def parallelly_process(packages, n_jobs=20):
    mega_meta = Parallel(n_jobs=n_jobs)(delayed(get_package_stats)(package) for package in packages)
    return mega_meta


if __name__ == '__main__':

    #packages = read_packages()
    packages = ['/simple/requests/']
    print(len(packages))

    chunk_size = 100

    # mega_meta = []

    for i in tqdm(range(154708, len(packages), chunk_size)):
        chunk = packages[i:i+chunk_size]
        partial_meta = parallelly_process(chunk)
        # mega_meta.extend(partial_meta)
        checkpoint(partial_meta, i)
        # break

    # checkpoint(mega_meta, "final")
