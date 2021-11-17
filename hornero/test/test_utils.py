"""
Test functions for hornero/utils.py
"""
import os
import pytest
from pathlib import Path

from ..utils import read_yaml, get_packages, check_package, check_categories

MODULE_DIR = Path(os.path.dirname(__file__))


@pytest.fixture(
    name="yaml_file", params=(True, False), ids=("path_as_string", "path_as_object")
)
def fixture_yaml_file(request):
    """
    Return the path to a sample YAML file
    """
    yaml_file = MODULE_DIR / "data" / "sample_packages.yml"
    if request.param:
        yaml_file = str(yaml_file)
    return yaml_file


@pytest.fixture(name="sample_packages")
def fixture_sample_packages():
    """
    A sample packages dictionary
    """
    packages = {
        "basic": ["package-one", "package-two"],
        "complex": ["package-three", "package-four", "package-five"],
    }
    return packages


@pytest.fixture(name="packages_with_trailing_spaces")
def fixture_packages_with_trailing_spaces():
    """
    A packages dictionary with trailing spaces on some items
    """
    packages = {
        "basic": ["package-one ", "package-two"],
        "complex": ["package-three", "package-four", "package-five"],
    }
    return packages


def test_read_yml(yaml_file):
    """
    Test read_yml function
    """
    content = read_yaml(yaml_file)
    expected_content = {
        "basic": ["package-one", "package-two"],
        "complex": ["package-three", "package-four", "package-five"],
    }
    assert content == expected_content


def test_get_packages(sample_packages, packages_with_trailing_spaces):
    """
    Test get_packages function
    """
    packages = get_packages(packages_with_trailing_spaces)
    assert packages == sample_packages


def test_check_package():
    """
    Check if check_package raise an error on invalid package
    """
    with pytest.raises(ValueError):
        check_package("package with multiple words")


@pytest.mark.parametrize("categories", (["basic"], ["complex"], ["basic", "complex"]))
def test_check_categories_valid(categories, sample_packages):
    """
    Test the check_categories function with valid categories
    """
    check_categories(sample_packages, categories)


@pytest.mark.parametrize(
    "categories", (["bla"], ["basic", "bla"], ["basic", "complex", "bla"])
)
def test_check_categories_invalid(categories, sample_packages):
    """
    Test the check_categories function with invalid categories
    """
    with pytest.raises(ValueError):
        check_categories(sample_packages, categories)
