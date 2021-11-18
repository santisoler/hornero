"""
Build a CLI for hornero
"""
import click
import inquirer

from .utils import check_categories, get_packages, read_yaml


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
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    default=False,
    help="Select packages interatively",
)
def cli(packages_yml, list_categories, categories, interactive):
    """
    Hornero: A package selector for building your confy nest
    """
    # Check if options are valid
    check_cli_options(list_categories, categories, interactive)

    # Parse the packages YAML file
    packages = get_packages(read_yaml(packages_yml))

    if list_categories:
        # List categories if list_categores is True
        click.echo("\n".join(packages.keys()))
        return
    elif interactive:
        # Run interatively
        categories, outfile = interactive_cli(packages)
        packages_selection = select_packages(packages, categories)
        click.echo("\nSelected packages:")
        click.echo("==================\n")
        click.echo("\n".join(packages_selection))
        if outfile:
            with open(outfile, "w") as selection_file:
                selection_file.write("\n".join(packages_selection))
        return
    else:
        # Generate categories if not passed
        if not categories:
            categories = tuple(packages.keys())
        check_categories(packages, categories)
        packages_selection = select_packages(packages, categories)
        click.echo("\n".join(packages_selection))
        return


def interactive_cli(packages):
    """
    Build the interative cli
    """
    categories = interative_selection_categories(packages)
    outfile = interactive_save_to_file()
    return categories, outfile


def interative_selection_categories(packages):
    """
    Return chosen categories from interative checkboxes
    """
    questions = [
        inquirer.Checkbox(
            "categories",
            message="Choose categories of packages to be selected",
            choices=list(packages.keys()),
        )
    ]
    categories = ()
    while not categories:
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        categories = answers["categories"]
    return categories


def interactive_save_to_file():
    """
    Define whether to save packages list to file from interactive cli
    """
    questions = [
        inquirer.Confirm(
            "dump_to_file",
            message="Do you want me to save the list of selected packages "
            + "in a file?",
            default=False,
        ),
    ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    outfile = answers["dump_to_file"]
    if outfile:
        questions = [
            inquirer.Path(
                "outfile", message="File name to store the list of selected packages"
            ),
        ]
        answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        outfile = answers["outfile"]
    return outfile


def select_packages(packages, categories):
    """
    Select packages inside the chosen categories

    Parameters
    ----------
    packages : dict
        Dictionary with categories and their corresponding packages as lists.
    categories : list
        List containing the chosen categories

    Returns
    -------
    packages_selection : list
        List of packages that belong to the chosen categories
    """
    packages_selection = []
    for category in categories:
        packages_selection.extend(packages[category])
    return packages_selection


def check_cli_options(list_categores, categories, interactive):
    """
    Check if only a single option is passed to the cli
    """
    if (
        list_categores
        and categories
        or list_categores
        and interactive
        or categories
        and interactive
    ):
        raise ValueError(
            "Only a single option should be passed at the same time.",
        )
