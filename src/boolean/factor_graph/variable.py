# Import to do the typing.
from typing import TYPE_CHECKING

# If the program runs at the type checking steps:
if TYPE_CHECKING:

    # Import to do the typing.
    from src.boolean.factor_graph.factor import Factor


class Variable:
    """
        The class denotes a variable in a factor graph.

        Attributes:
            variable_id_str (str).
                The string representing the ID of this variable.
            variable_value_bool (bool).
                The Boolean value denoting the value of this variable.
            positive_literal_factors_object_set (Set[Factor]).
                The set of Boolean clauses containing the positive literal of this variable.
            negative_literal_factors_object_set (Set[Factor]).
                The set of Boolean clauses containing the negative literal of this variable.
    """

    def __init__(self, variable_id_str: str, variable_value_bool: bool = None):
        """
            Construct objects by initializing attributes.

            Arguments:
                variable_id_str (str).
                    The string representing the ID of this variable.
                variable_value_bool (bool).
                    The Boolean value denoting the value of this variable.
        """

        # Initialize attributes by assigning arguments to them.
        self.variable_id_str = variable_id_str
        self.variable_value_bool = variable_value_bool

        # Initialize the attribute as an empty set.
        self.positive_literal_factors_object_set = set()

        # Initialize the attribute as an empty set.
        self.negative_literal_factors_object_set = set()

    def add_a_factor_with_positive_literal(self, positive_literal_factor_object: "Factor"):
        """
            Add an object of Factor with the positive literal of the self object into the corresponding set.

            Arguments:
                positive_literal_factor_object (Factor).
                    The object of Factor with the positive literal of the self object.
        """

        # Add the argument object into the set of factors with positive literals of the self object.
        self.positive_literal_factors_object_set.add(positive_literal_factor_object)

    def add_a_factor_with_negative_literal(self, negative_literal_factor_object: "Factor"):
        """
            Add an object of Factor with the negative literal of the self object into the corresponding set.

            Arguments:
                negative_literal_factor_object (Factor).
                    The object of Factor with the negative literal of the self object.
        """

        # Add the argument object into the set of factors with negative literals of the self object.
        self.negative_literal_factors_object_set.add(negative_literal_factor_object)
