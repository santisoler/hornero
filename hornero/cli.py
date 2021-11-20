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
    Hornero: A package selector for building your confy nest
    """
    # Parse the packages YAML file
    packages = get_packages(read_yaml(packages_yml))

    # Ask interactive questions through dialog
    answers = interactive_dialog(packages)
    click.clear()

    # Get package manager
    package_manager = get_package_manager(package_manager=package_manager)

    console = Console(stderr=False, highlight=False)

    # Update the list of packages
    if answers["update"]:
        command = package_manager.get_update_command()
        print_section_heading(console, "Updating packages list", command)
        package_manager.run(command)

    # Upgrade the packages
    if answers["upgrade"]:
        command = package_manager.get_upgrade_command()
        print_section_heading(console, "Upgrading packages", command, add_new_line=True)
        package_manager.run(command)

    # Install the selected packages
    packages_selection = select_packages(packages, answers["categories"])
    if packages_selection:
        command = package_manager.get_install_command(packages_selection)
        print_section_heading(
            console, "Installing selected packages", command, add_new_line=True
        )
        package_manager.run(command)
    return


def interactive_dialog(packages):
    """
    Ask questions through dialog
    """
    height, width = 8, 60
    answers = {}
    dialog = Dialog(dialog="dialog")
    code = dialog.yesno(
        "Update packages lists from remote repositories?", height=height, width=width
    )
    answers["update"] = code == dialog.OK
    code = dialog.yesno(
        "Upgrade installed packages to latest version?", height=height, width=width
    )
    answers["upgrade"] = code == dialog.OK
    _, tags = dialog.checklist(
        "Choose categories of packages to be selected",
        choices=[(pkg, "", False) for pkg in packages.keys()],
    )
    answers["categories"] = tags
    return answers


def print_section_heading(console, title, command, add_new_line=False):
    """
    Use rich console to print a title for each section
    """
    if add_new_line:
        console.print()
    console.rule(f"{title}", style="green bold", characters="=")
    console.print()
    console.print(f"$ {command}", style="blue")
