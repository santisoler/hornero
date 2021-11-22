"""
Build a CLI for hornero
"""
import click
from dialog import Dialog
from rich.console import Console

from .managers import PACKAGE_MANAGERS, get_package_manager
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
    Hornero: A package selector for building your comfy nest
    """
    # Parse the packages YAML file
    packages = get_packages(read_yaml(packages_yml))

    # Get package manager
    package_manager = get_package_manager(package_manager=package_manager)

    # Select which categories should be installed
    categories = interactive_dialog(packages.keys())
    click.clear()

    # Define rich console
    console = Console(stderr=False, highlight=False)

    # Install the selected packages
    packages_selection = select_packages(packages, categories)
    if packages_selection:
        command = package_manager.get_install_command(packages_selection)
        console.rule(
            "[bold green]Installing selected packages[/bold green]", style="green bold"
        )
        console.print()
        console.print(f"$ {command}", style="blue")
        package_manager.run(command)
    return


def interactive_dialog(categories):
    """
    Ask questions through dialog
    """
    dialog = Dialog(dialog="dialog")
    while True:
        _, selected_categories = dialog.checklist(
            "Choose categories of packages to be installed",
            choices=[(category, "", False) for category in categories],
            height=40,
            width=60,
        )
        proceed = dialog.yesno(
            "The following categories have been selected:\n\n"
            + "\n".join(selected_categories)
            + "\n\nProceed with the installation?",
            width=60,
            height=30,
        )
        if proceed:
            break
    return selected_categories
