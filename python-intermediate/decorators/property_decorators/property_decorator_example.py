class Box:
    """
    A simple class representing a box with a weight.

    This class demonstrates the use of Python properties to control
    access to a private attribute.

    Attributes
    ----------
    __weight : float
        A private attribute storing the weight of the box.
        The double underscore triggers name mangling to discourage
        direct access from outside the class.

    The class provides:
    - A getter to read the weight
    - A setter with validation (weight cannot be negative)
    - A deleter to remove the weight attribute
    """

    def __init__(self, weight):
        """
        Initialize a Box object.
        weight : float or int
            The initial weight of the box.

        The value is stored in a private variable `__weight`.
        """
        self.__weight = weight

    @property
    def weight(self):
        """
        Get the weight of the box.

        Returns
        -------
        float or int
            The current weight stored in the box.

        Explanation
        -----------
        The @property decorator allows this method to be accessed
        like a normal attribute instead of a method.

        Example
        -------
        >>> b = Box(10)
        >>> b.weight
        10
        """
        return self.__weight

    @weight.setter
    def weight(self, weight):
        """
        Set the weight of the box.

        Parameters
        ----------
        weight : float or int
            The new weight value.

        Behavior
        --------
        - Updates the weight only if it is non-negative.
        - Prevents invalid values such as negative weights.

        Example
        -------
        >>> b = Box(10)
        >>> b.weight = 20
        >>> b.weight
        20

        >>> b.weight = -5
        (Value ignored because it is negative)
        """
        if weight >= 0:
            self.__weight = weight

    @weight.deleter
    def weight(self):
        """
        Delete the weight attribute.

        Behavior
        --------
        Removes the private attribute `__weight` from the object.

        Example
        -------
        >>> b = Box(10)
        >>> del b.weight
        >>> b.weight
        AttributeError
        """
        del self.__weight


"""
class Box:
    def __init__(self, weight):
        self.__weight = weight

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight):
        if weight >= 0:
            self.__weight = weight

    @weight.deleter
    def weight(self):
        del self.__weight
"""

b = Box(5)
print(b.weight)   # getter → 5
b.weight = 15     # setter
print(b.weight)   # 15
b.weight = -3     # ignored due to validation
print(b.weight)   # still 15
del b.weight      # delete attribute

"""
Key Python Concepts Demonstrated:
- Encapsulation using __weight
- Properties using @property
- Data validation using @weight.setter
- Controlled deletion using @weight.deleter

When using the decorator, remember three rules:

    All three methods must use the same member name (ex. weight).
    The first method must be the getter and is identified using @property.
    The decorators for the setter and deleter are defined by the name of the method @property is used with.

"""