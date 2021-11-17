"""
Utility functions
"""


def check_categories(packages, categories):
    """
    Check if selected categories are available in the packages dict

    Parameters
    ----------
    packages : dict
        Dictionary with categories and their corresponding packages as lists.
    categories : tuple
        List of selected categories
    """
    invalid_categories = tuple(
        category for category in categories if category not in packages.keys()
    )
    if invalid_categories:
        invalid_categories = " ".join(invalid_categories)
        raise ValueError(
            f"Invalid categories: '{invalid_categories}'. "
            + "These categories are not present in the packages file."
        )
