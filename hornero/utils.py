"""
Utility functions for Hornero
"""
import yaml


def get_packages(packages_raw):
    """
    Build a dict with categories and their packages

    Parameters
    ----------
    packages_raw : dict
        Dictionary with the content of the packages YAML file.

    Returns
    -------
    packages : dict
        Dictionary with the categories and their corresponding packages as
        lists.
    """
    packages = {category: [] for category in packages_raw}
    for category, packages_list in packages_raw.items():
        for package in packages_list:
            check_package(package)
            packages[category].append(package.strip())
    return packages


def select_packages(packages, categories):
    """
    Select packages inside the chosen categories

    Parameters
    ----------
    packages : dict
        Dictionary with categories and their corresponding packages as lists.
    categories : list
        List containing the chosen categories

    Returns
    -------
    packages_selection : list
        List of packages that belong to the chosen categories
    """
    packages_selection = []
    for category in categories:
        packages_selection.extend(packages[category])
    return packages_selection


def read_yaml(yaml_file):
    """
    Read a YAML file

    Parameters
    ----------
    yaml_file : str or PathLike
        Path to the YAML file.

    Returns
    -------
    content : dict
        Dictionary with the content of the YAML file.
    """
    with open(yaml_file, "r") as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
    return content


def check_package(package):
    """
    Check validity of package
    """
    if len(package.split()) > 1:
        raise ValueError(f"Invalid package '{package}' found.")
