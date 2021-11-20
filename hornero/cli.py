"""
Build a CLI for hornero
"""
import click
import inquirer

from .managers import get_package_manager, PACKAGE_MANAGERS
from .utils import get_packages, read_yaml, select_packages


@click.command()
@click.argument("packages_yml")
@click.option(
    "-p",
    "--package_manager",
    help="Select the package manager to use",
    default=None,
    type=click.Choice(PACKAGE_MANAGERS.keys()),
)
def cli(packages_yml, package_manager):
    """
    Hornero: A package selector for building your confy nest
    """
    # Parse the packages YAML file
    packages = get_packages(read_yaml(packages_yml))

    # Ask interactive questions through inquirer
    answers = interactive_cli(packages)

    # Get package manager
    package_manager = get_package_manager(package_manager=package_manager)

    # Update the list of packages
    if answers["update"]:
        package_manager.update()

    # Upgrade the packages
    if answers["upgrade"]:
        package_manager.upgrade()

    # Install the selected packages
    packages_selection = select_packages(packages, answers["categories"])
    if packages_selection:
        package_manager.install(packages_selection)
    return


def interactive_cli(packages):
    """
    Ask questions through inquirer
    """
    questions = [
        inquirer.Confirm(
            "update",
            message="Update packages lists from remote repositories?",
            default=True,
        ),
        inquirer.Confirm(
            "upgrade",
            message="Upgrade installed packages to latest version?",
            default=True,
        ),
        inquirer.Checkbox(
            "categories",
            message="Choose categories of packages to be selected",
            choices=list(packages.keys()),
        ),
    ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    return answers
