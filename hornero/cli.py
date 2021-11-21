"""
Build a CLI for hornero
"""
import click
from rich.console import Console
from rich.prompt import Prompt, Confirm

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

    # Define rich console
    console = Console(stderr=False, highlight=False)

    # Select which categories should be installed
    checklist = Checklist(
        "[bold green]Select packages to install[/bold green]",
        "[bold cyan]Packages to install[/bold cyan] "
        + "[bright_black](e.g 1 2 3)[/bright_black]",
        list(packages.keys()),
        console,
    )
    categories = checklist.ask()

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


class Checklist:
    """
    Simple interactive checklist through rich.console.Console
    """

    def __init__(self, text, prompt_text, elements, console):
        self.text = text
        self.prompt_text = prompt_text
        self.elements = elements
        self.console = console
        self.prompt = Prompt(console=console)
        self.confirm = Confirm(console=console)

    def ask(self):
        """
        Prompt the checklist and ask for selection of its elements
        """
        # Print title
        self.console.rule(self.text)
        while True:

            # Print list of elements
            self.console.print()
            list_of_elements = [
                f" [blue]{i+1:2d}[/blue] {item}" for i, item in enumerate(self.elements)
            ]
            self.console.print("\n".join(list_of_elements))
            self.console.print()

            # Ask for elements to be selected
            answer = self.prompt.ask(self.prompt_text)

            # Check if the answer contain integers
            are_integers = [is_integer(i) for i in answer.split()]
            if not all(are_integers):
                self.console.print(
                    "Invalid input: must pass a set of integers.\n", style="red"
                )
                continue

            # Get indices from the answer
            indices = [int(i) - 1 for i in answer.split()]

            # Check if answers are within the range of the number of elements
            min_index, max_index = min(indices), max(indices)
            if min_index < 0:
                self.console.print(
                    f"Invalid value '{min_index + 1}'.\n",
                    style="red",
                )
                continue
            if max_index >= len(self.elements):
                self.console.print(
                    f"Invalid value '{max_index + 1}'.\n",
                    style="red",
                )
                continue

            # Get selected categories
            selection = list(self.elements[i] for i in indices)

            # Confirm if the selected categories are OK
            self.console.print("\n[bold cyan]Your selection:[/bold cyan] ")
            self.console.print()
            list_of_elements = []
            for i, item in enumerate(self.elements):
                if item in selection:
                    style = "bold green"
                else:
                    style = "bright_black"
                list_of_elements.append(f" [{style}]{i+1:2d} {item}[/{style}]")
            self.console.print("\n".join(list_of_elements))
            self.console.print()
            answer = self.confirm.ask(
                "[bold cyan]Do you want to continue?[/bold cyan]", default=True
            )
            if answer:
                break
        return selection


def is_integer(string):
    """
    Check if a given string can be converted to an integer
    """
    try:
        int(string)
    except ValueError:
        return False
    else:
        return True
