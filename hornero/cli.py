"""
Hornero main script
"""
import click


@click.command()
@click.argument("packages_file")
def cli():
    """
    Hornero: A package selector for building your confy nest.
    """
