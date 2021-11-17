"""
Build a CLI for hornero
"""
import click

from .yml_parser import read_yaml
from .utils import check_categories, check_cli_options


@click.command()
@click.argument("packages_yml")
@click.option(
    "-l",
    "--list-categories",
    is_flag=True,
    default=False,
    help="List available categories in PACKAGES_YML",
)
@click.option(
    "-c",
    "--categories",
    multiple=True,
    help="Select packages only from this category or categories",
)
def cli(packages_yml, list_categories, categories):
    """
    Hornero: A package selector for building your confy nest
    """
    # Check if options are valid
    check_cli_options(list_categories, categories)

    # Parse the packages YAML file
    packages = read_yaml(packages_yml)

    # List categories if list_categores is True
    if list_categories:
        click.echo("\n".join(packages.keys()))
        return 0

    # Generate categories if not passed
    if not categories:
        categories = tuple(packages.keys())
    check_categories(packages, categories)

    # Select packages from the selected categories
    packages_selection = []
    for category in categories:
        packages_selection.extend(packages[category])
    click.echo("\n".join(packages_selection))
    return 0
