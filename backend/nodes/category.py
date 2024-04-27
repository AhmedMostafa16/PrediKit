from typing import Union


class Category:
    """
    Represents a category with its name, description, icon, color, and optional install hint.

    Attributes:
        name (str): The name of the category.
        description (str): The description of the category.
        icon (str): The icon of the category.
        color (str): The color of the category.
        install_hint (str, None): An optional install hint for the category.

    Methods:
        toDict(): Converts the category object to a dictionary.
    """

    def __init__(
        self,
        name: str,
        description: str,
        icon: str,
        color: str,
        install_hint: Union[str, None] = None,
    ):
        self.name: str = name
        self.description: str = description
        self.icon: str = icon
        self.color: str = color
        self.install_hint: Union[str, None] = install_hint

    def toDict(self):
        """
        Converts the category object to a dictionary.

        Returns:
            dict: A dictionary representation of the category object.
        """
        return {
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "color": self.color,
            "installHint": self.install_hint,
        }

    def __repr__(self):
        return str(self.toDict())

    def __iter__(self):
        yield from self.toDict().items()
