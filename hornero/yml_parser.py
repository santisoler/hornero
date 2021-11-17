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
