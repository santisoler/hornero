"""
Build a CLI for hornero
"""
import sys
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
    defaults = [False for category in categories]
    while True:
        # Ask for categories selection
        code, selected_categories = dialog.checklist(
            "Choose categories of packages to be installed",
            choices=[
                (category, "", default)
                for category, default in zip(categories, defaults)
            ],
            height=40,
            width=60,
        )
        # If cancel, ask the user if they want to quit
        if code == dialog.CANCEL:
            quit = dialog.yesno("Do you want to quit?")
            if quit == dialog.OK:
                sys.exit()
            else:
                continue
        # Update the defaults in case the user wants to edit their selection
        defaults = [category in selected_categories for category in categories]
        # Ask if the user wants to proceed with the installation
        proceed = dialog.yesno(
            "The following categories have been selected:\n\n"
            + "\n".join(selected_categories)
            + "\n\nProceed with the installation?",
            width=60,
            height=30,
        )
        if proceed == dialog.OK:
            break
    return selected_categories
