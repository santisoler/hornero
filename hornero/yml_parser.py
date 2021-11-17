"""
Define functions for reading packages and categories from YAML files
"""
import yaml


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


def get_packages(yaml_file):
    """
    Build a dict with categories and their packages from the packages YAML file

    Parameters
    ----------
    yaml_file : str or PathLike
        Path to the YAML file.

    Returns
    -------
    packages : dict
        Dictionary with the categories and their corresponding packages as
        lists.
    """
    packages_raw = read_yaml(yaml_file)
    packages = {category: [] for category in packages_raw}
    for category, packages_list in packages_raw.items():
        for package in packages_list:
            check_package(package)
            packages[category].append(package.strip())
    return packages


def check_package(package):
    """
    Check validity of package
    """
    if len(package.split()) > 1:
        raise ValueError(f"Invalid package '{package}' found.")
