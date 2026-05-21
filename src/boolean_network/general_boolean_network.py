# Import to save transitions.
from src.data.output.complete_transitions_from_a_network_output import save_complete_transitions_from_a_network

# Import to do annotation.
from typing import Callable

# Import to enumerate.
import itertools


class GeneralBooleanNetwork:
    """
        This class denotes general boolean networks.

        Attributes:
            boolean_variables_str_and_boolean_expressions_callable_dict (dict[str: Callable]).
                The dictionary containing key-value pairs about Boolean variables and their corresponding Boolean expressions.
            boolean_variables_str_and_boolean_expressions_str_dict (dict[str: str]).
                The dictionary containing key-value pairs about Boolean variables and their corresponding Boolean expressions as strings.
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.
    """

    def __init__(self, boolean_variables_str_and_boolean_expressions_callable_dict: dict[str: Callable], boolean_variables_str_and_boolean_expressions_str_dict: dict[str: str], boolean_variables_str_and_ordered_indices_int_dict: dict[str: int]):
        """
            Construct objects by initializing attributes.

            Arguments:
                boolean_variables_str_and_boolean_expressions_callable_dict (dict[str: Callable]).
                    The dictionary containing key-value pairs about Boolean variables and their corresponding Boolean expressions.
                boolean_variables_str_and_boolean_expressions_str_dict (dict[str: str]).
                    The dictionary containing key-value pairs about Boolean variables and their corresponding Boolean expressions as strings.
                boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                    The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.
        """

        # Initialize attributes by assigning arguments to them.
        self.boolean_variables_str_and_boolean_expressions_callable_dict = boolean_variables_str_and_boolean_expressions_callable_dict
        self.boolean_variables_str_and_boolean_expressions_str_dict = boolean_variables_str_and_boolean_expressions_str_dict
        self.boolean_variables_str_and_ordered_indices_int_dict = boolean_variables_str_and_ordered_indices_int_dict

    def generate_complete_transitions(self, complete_transitions_file_name_with_type_str: str = None) -> (list[(dict[str: bool], dict[str: bool])]):
        """
            Generate complete transitions based on all Boolean expressions.

            Arguments:
                complete_transitions_file_name_with_type_str (str).
                    Default value is None.
                    The string denoting the file name with type to store the complete transitions.

            Returns:
                (list[(dict[str: bool], dict[str: bool])]).
                    The list containing all transitions as tuples.
                    The first element in each tuple is a dictionary denoting binary states before.
                    The second element in each tuple is a dictionary denoting binary states after.
        """

        # Initialize an empty list to store all transitions.
        transitions_dict_1d_tuple_1d_list = []

        # Iterate the permutation of assignments of Boolean variables.
        for boolean_values_bool_list in itertools.product([False, True], repeat=len(self.boolean_variables_str_and_ordered_indices_int_dict)):

            # Get the states before as a dictionary.
            current_boolean_variables_str_and_boolean_values_bool_dict = {boolean_variable_str: boolean_values_bool_list[ordered_index_int] for boolean_variable_str, ordered_index_int in self.boolean_variables_str_and_ordered_indices_int_dict.items()}

            # Get the dictionary of next binary_states.
            next_boolean_variables_str_and_boolean_values_bool_dict = {}

            # Iterate each Boolean variable and their corresponding Boolean expressions:
            for boolean_variable_str, boolean_expression_callable in self.boolean_variables_str_and_boolean_expressions_callable_dict.items():

                # Add the Boolean variable and its next Boolean value into the dictionary.
                next_boolean_variables_str_and_boolean_values_bool_dict[boolean_variable_str] = eval(boolean_expression_callable(current_boolean_variables_str_and_boolean_values_bool_dict))

            # Add the current transition as a tuple into the list.
            transitions_dict_1d_tuple_1d_list.append((current_boolean_variables_str_and_boolean_values_bool_dict, next_boolean_variables_str_and_boolean_values_bool_dict))

        # If the argument explicitly provides the file name with type to store the complete transitions:
        if complete_transitions_file_name_with_type_str is not None:

            # Call the method to save transitions.
            save_complete_transitions_from_a_network(transitions_dict_1d_tuple_1d_list=transitions_dict_1d_tuple_1d_list, boolean_variables_str_and_ordered_indices_int_dict=self.boolean_variables_str_and_ordered_indices_int_dict, transitions_file_name_and_type_str=complete_transitions_file_name_with_type_str)

        # Return the list containing all transitions as tuples.
        return transitions_dict_1d_tuple_1d_list
