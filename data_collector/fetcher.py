from pipdeptree import get_installed_distributions, build_dist_index, construct_tree
from bs4 import BeautifulSoup
from json import dump
from urllib.request import urlretrieve
from pathlib import Path

import requests
import re

def create_tree():
    pkgs = get_installed_distributions()
    dist_index = build_dist_index(pkgs)
    tree = construct_tree(dist_index)

    return tree


def get_package_list():
    """
    Helper function to retrieve package names from the Pypi URL. Save it to a json for future use.

    """
    r = requests.get("https://pypi.org/simple/")
    soup = BeautifulSoup(r.content, features='html.parser')
    data = []

    for link in soup.find_all('a', href=True):
        data.append(link["href"])

    with open("python_packages_list.json", "w") as f:
        dump(data, f)


def download(download_link, output_folder, package_name, version):
    url = download_link
    dst = Path(output_folder).joinpath("{}-{}.tar.gz".format(package_name, version))
    urlretrieve(url, dst)


def get_package(package_name):
    """
    Note that package name already starts with /simple/
    This downloader only focuses on .tar.gz files

    :param package_name:
    :return:
    """
    url = "https://pypi.org{}".format(package_name)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='html.parser')

    for id, link in enumerate(soup.find_all('a', href=True)):
        if ".tar.gz" in link["href"]:
            download(link["href"], "downloaded_packages", package_name.split("/")[-2], id)


if __name__ == '__main__':
    # get_package_list()
    get_package("/simple/aarghparse/")