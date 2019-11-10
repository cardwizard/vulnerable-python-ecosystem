from pipdeptree import get_installed_distributions, build_dist_index, construct_tree
from bs4 import BeautifulSoup
from json import dump, load
from urllib.request import urlretrieve
from pathlib import Path
from unittest import mock
from pkginfo import SDist
from johnnydep.cli import JohnnyDist

import requests
import setuptools
import tarfile


def read_packages():
    with open("python_packages_list.json", "r") as f:
        package_info = load(f)

    return package_info


def download(download_link, output_folder, package_name, version):
    url = download_link
    dst = Path(output_folder).joinpath("{}_{}.tar.gz".format(package_name, version))
    urlretrieve(url, dst)


def get_packages(package_name):
    """
    Note that package name already starts with /simple/
    This downloader only focuses on .tar.gz files

    :param package_name:
    :return:
    """
    url = "https://pypi.org{}".format(package_name)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='html.parser')
    tar = 0

    for id, link in enumerate(soup.find_all('a', href=True)):
        if ".tar.gz" in link["href"]:
            download(link["href"], "downloaded_packages/tar", package_name.split("/")[-2], id)
            tar += 1

    return {"tar": tar}


def extract_info_from_setup():
    with mock.patch.object(setuptools, 'setup') as mock_setup:
        import data_collector.downloaded_packages.setup

    args, kwargs = mock_setup.call_args
    print(kwargs)


def unpack(package_name):
    with tarfile.open(package_name, mode="r:gz") as tf:
        tf.extractall()


def parse(pkg_info):
    mypackage = SDist(pkg_info)

    return PackageInfo(version=mypackage.version, author=mypackage.author_email,
                       license=mypackage.license,
                       name=mypackage.name,
                       maintainer=mypackage.maintainer_email, additional_details=mypackage.__dict__)


def get_dependencies(package):
    url = 'https://pypi.org/pypi/{}/json'
    json = requests.get(url.format(package)).json()
    print(json.keys())
    # return json


def get_johnny_dep(package):
    dist = JohnnyDist(package, index_url=None, env=None, extra_index_url=None)
    return dist.serialise(fields=["name", "requires", "required_by", "project_name", "versions_available"], format=None, recurse=True)


if __name__ == '__main__':
    # get_package_list()
    # get_packages("/simple/jupyter/")
    # unpack("downloaded_packages/tar/jupyter_1.tar.gz")
    # extract_info_from_setup()
    # print(parse("downloaded_packages/tar/jupyter_1.tar.gz").dump_details())
    # print(pkg_resources.get_distribution("downloaded_packages/tar/jupyter_1.tar.gz"))
    print(get_dependencies("pandas"))
    # print(get_johnny_dep("ipython"))

