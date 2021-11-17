"""
Build a CLI for hornero
"""
import click

from .utils import check_categories, get_packages


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
    packages = get_packages(packages_yml)

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


def check_cli_options(list_categores, categories):
    """
    Check if only a single option is passed to the cli
    """
    if list_categores and categories:
        raise ValueError(
            "Only a single option should be passed at the same time.",
        )
