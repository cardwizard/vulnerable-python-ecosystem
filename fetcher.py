from pipdeptree import get_installed_distributions, build_dist_index, construct_tree
from bs4 import BeautifulSoup
from json import dump

import requests

def create_tree():
    pkgs = get_installed_distributions()
    dist_index = build_dist_index(pkgs)
    tree = construct_tree(dist_index)

    return tree


def get_data():
    r = requests.get("https://pypi.org/simple/")
    soup = BeautifulSoup(r.content, features='html.parser')
    data = []

    for link in soup.find_all('a', href=True):
        data.append(link["href"])

    with open("python_packages_list.json", "w") as f:
        f.write(data)

if __name__ == '__main__':
    get_data()