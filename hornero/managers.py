"""
Define classes for wrapping different package managers
"""
import os
import subprocess
import click
import distro

# Define dictionary matching linux distro to package manager classname
# defined in settle/package_managers.py
DISTROS_PACKAGE_MANAGERS = {
    "manjaro linux": "pacman",
    "arch": "pacman",
    "ubuntu": "apt",
    "debian": "apt",
}

# Define list of supported package managers
PACKAGE_MANAGERS = {
    "apt": dict(
        package_manager="apt",
        update_option="update",
        upgrade_option="upgrade",
        install_option="install",
        needs_sudo=True,
    ),
    "pacman": dict(
        package_manager="pacman",
        update_option="-Sy",
        upgrade_option="-Su",
        install_option="-S",
        needs_sudo=True,
    ),
    "yay": dict(
        package_manager="yay",
        update_option="-Sy",
        upgrade_option="-Su",
        install_option="-S",
        needs_sudo=False,
    ),
}


def get_package_manager(package_manager=None):
    """
    Get the package manager class that will manage the installations

    Parameters
    ----------
    package_manager : str (optional)
        Package manager name. If None, the better suited package manager will
        be chosen based on the distro.

    Returns
    -------
    package_manager_obj : instance of :class:`PackageManager`
        Package manager instance
    """
    # Guess package manager if None
    if package_manager is None:
        package_manager = guess_package_manager()
    # Raise error if invalid package manager
    if package_manager not in PACKAGE_MANAGERS:
        raise ValueError("Invalid package manager '{}'".format(package_manager))
    # Initialize a PackageManager object and return it
    return PackageManager(**PACKAGE_MANAGERS[package_manager])


def guess_package_manager():
    """
    Guess which package manager class is suited for your Linux distribution

    Return
    ------
    package_manager : str
        Name of the package manager
    """
    distribution = distro.linux_distribution()[0]
    distribution = distribution.lower()
    if distribution not in DISTROS_PACKAGE_MANAGERS:
        raise ValueError(
            "Couldn't choose a package manager for your distro. "
            + "This may be caused because your distro is not supported or "
            + "Settle cannot identify it properly. "
            + "Try specifying the package manager you want to use through the "
            + "--package-manager option."
        )
    return DISTROS_PACKAGE_MANAGERS[distribution]


class PackageManager(object):
    """
    Class that wraps package managers

    Parameters
    ----------
    package_manager : str
        Package manager name (the name of the command to run it).
    update_option : str
        Option to pass to the package manager to update the list of packages
        from the repositories.
    upgrade_option : str
        Option to pass to the package manager to upgrade the installed
        packages.
    install_option : str
        Option to pass to the package manager to install the packages that will
        be passed as arguments.
    needs_sudo : bool
        If True, the package manager will be run with super user privileges.
        Default to True.
    """

    def __init__(
        self,
        package_manager,
        update_option,
        upgrade_option,
        install_option,
        needs_sudo=True,
    ):
        self.needs_sudo = needs_sudo
        self.package_manager = package_manager
        self.update_option = update_option
        self.upgrade_option = upgrade_option
        self.install_option = install_option
        self._lists_updated = False

    @property
    def lists_updated(self):
        return self._lists_updated

    @property
    def sudo(self):
        """
        Check if we have sudo privileges
        """
        return os.getuid() != 0

    def update(self):
        """
        Update package lists
        """
        command_line = self._build_command(self.update_option)
        try:
            self.run(command_line)
        except Exception as e:
            raise e
        else:
            self._lists_updated = True

    def upgrade(self):
        """
        Update packages
        """
        command_line = self._build_command(self.upgrade_option)
        try:
            self.run(command_line)
        except Exception as e:
            raise e

    def install(self, packages):
        """
        Install packages
        """
        command_line = self._build_command(self.upgrade_option, packages=packages)
        try:
            self.run(command_line)
        except Exception as e:
            raise e

    def run(self, command_line, verbose=True):
        """
        Run the given command line
        """
        if verbose:
            click.echo("\n :: Running:")
            click.echo(command_line)
            click.echo("")
        subprocess.run(command_line, shell=True)

    def _build_command(self, options, packages=None):
        """
        Return a command line to run the package manager from the shell

        Concatenates the package manager command with the options and the given
        packages in a single string. Adds a heading "sudo" if needed.

        Parameters
        ----------
        options : str or None
            Options for the package manager. If None, no option is appended.
        packages : list or None (optional)
            List of arguments for the command as strings. If None, no argument
            is appended.

        Returns
        -------
        full_line : str
            Concatenation of the package manager, its options and the list of
            packages, with a heading "sudo" if needed.
        """
        command_line = []

        # Append sudo if needed
        if self.needs_sudo and self.sudo:
            command_line.append("sudo")

        # Append the package manager
        command_line.append(self.package_manager)

        # Append the options
        if options is not None:
            command_line.append(options)

        # Add the packages
        if packages is not None:
            command_line += packages

        # Return the command line as a single string
        return " ".join(command_line)
