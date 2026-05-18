# Import to do the typing.
from typing import TYPE_CHECKING

# Import to do the typing.
from typing import Union

# If the program runs at the type checking steps:
if TYPE_CHECKING:

    # Import to do the typing.
    from src.boolean.factor_graph.variable import Variable


class Factor:
    """
        The class denotes a factor in a factor graph.

        Attributes:
            positive_literal_variables_id_str_and_variables_object_dict (dict[int: Variable]).
                The dictionary containing key-value pairs about Boolean variables ID with positive decimals in it and their corresponding Variable objects.
            negative_literal_variables_id_str_and_variables_object_dict (dict[int: Variable]).
                The dictionary containing key-value pairs about Boolean variables ID with negative decimals in it and their corresponding Variable objects.
    """

    def __init__(self):
        """
            Construct objects by initializing attributes.
        """

        # Initialize the attribute as an empty dictionary.
        self.positive_literal_variables_id_str_and_variables_object_dict = {}

        # Initialize the attribute as an empty dictionary.
        self.negative_literal_variables_id_str_and_variables_object_dict = {}

    def add_a_variable_with_positive_literal(self, variable_object: "Variable"):
        """
            Add an object of Variable with the positive literal in the self factor into the corresponding dictionary.

            Arguments:
                variable_object (Variable).
                    The object of Variable with the positive literal in the self factor.
        """

        # If the argument Variable is not in the dictionary containing variables with positive literals in the self factor:
        if variable_object.variable_id_str not in self.positive_literal_variables_id_str_and_variables_object_dict:

            # Add the argument Variable into this dictionary.
            self.positive_literal_variables_id_str_and_variables_object_dict[variable_object.variable_id_str] = variable_object

    def add_a_variable_with_negative_literal(self, variable_object: "Variable"):
        """
            Add an object of Variable with the negative literal in the self factor into the corresponding dictionary.

            Arguments:
                variable_object (Variable).
                    The object of Variable with the negative literal in the self factor.
        """

        # If the argument Variable is not in the dictionary containing variables with negative literals in the self factor:
        if variable_object.variable_id_str not in self.negative_literal_variables_id_str_and_variables_object_dict:

            # Add the argument Variable into this dictionary.
            self.negative_literal_variables_id_str_and_variables_object_dict[variable_object.variable_id_str] = variable_object

    def compute_boolean_value_of_clause(self) -> Union[bool, None]:
        """
            Compute the Boolean value of this factor.

            Arguments:
                (Union[bool, None]).
                    The boolean value of this clause.
        """

        # Iterate each variable with the positive literal in the self factor:
        for variable_id_str in self.positive_literal_variables_id_str_and_variables_object_dict:

            # If the current variable has True Boolean value:
            if self.positive_literal_variables_id_str_and_variables_object_dict[variable_id_str].variable_value_bool is True:

                # The Boolean value of the self factor is True.
                return True

        # Iterate each variable with the negative literal in the self factor:
        for variable_id_str in self.negative_literal_variables_id_str_and_variables_object_dict:

            # If the current variable has False Boolean value:
            if self.negative_literal_variables_id_str_and_variables_object_dict[variable_id_str].variable_value_bool is False:

                # The Boolean value of the self factor is True.
                return True

        # Iterate each variable with the positive literal in the self factor:
        for variable_id_str in self.positive_literal_variables_id_str_and_variables_object_dict:

            # If the Boolean value of the current variable has not been not determined yet:
            if self.positive_literal_variables_id_str_and_variables_object_dict[variable_id_str].variable_value_bool is None:

                # The Boolean value of self factor is not determined yet.
                return None

        # Iterate each variable with the negative literal in the self factor.
        for variable_id_str in self.negative_literal_variables_id_str_and_variables_object_dict:

            # If the Boolean value of the current variable has not been not determined yet:
            if self.negative_literal_variables_id_str_and_variables_object_dict[variable_id_str].variable_value_bool is None:

                # The Boolean value of self factor is not determined yet.
                return None

        # After all four for-loops, the boolean value of this self factor is False.
        return False
