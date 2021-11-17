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


def check_categories(packages, categories):
    """
    Check if selected categories are available in the packages dict

    Parameters
    ----------
    packages : dict
        Dictionary with categories and their corresponding packages as lists.
    categories : tuple
        List of selected categories
    """
    invalid_categories = tuple(
        category for category in categories if category not in packages.keys()
    )
    if invalid_categories:
        invalid_categories = " ".join(invalid_categories)
        raise ValueError(
            f"Invalid categories: '{invalid_categories}'. "
            + "These categories are not present in the packages file."
        )
