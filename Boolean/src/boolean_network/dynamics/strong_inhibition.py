# Import GeneralBooleanNetwork to inherit it.
from src.boolean_network.general_boolean_network import GeneralBooleanNetwork

# Import to get Callable results.
from src.data.input.general_boolean_network_input import convert_boolean_expression_to_tokens_and_indices, help_function_to_return_callable

# Import to do annotations.
from typing import Callable


class StrongInhibition(GeneralBooleanNetwork):
    """
        This class inherits GeneralBooleanNetwork and denotes the dynamics of strong inhibition.

        Attributes:
            green_edges_target_str_and_sources_str_list_dict (dict[str, list[str]]).
                The dictionary containing key-value pairs about a target node and other nodes which have green edges to it.
            red_edges_target_str_and_sources_str_list_dict (dict[str, list[str]]).
                The dictionary containing key-value pairs about a target node and other nodes which have red edges to it.
    """

    def __init__(self, green_edges_target_str_and_sources_str_list_dict: dict[str, list[str]], red_edges_target_str_and_sources_str_list_dict: dict[str, list[str]], sorted_boolean_variables_str_list: list[str] = None):
        """
            Construct objects by initializing attributes.

            Arguments:
                green_edges_target_str_and_sources_str_list_dict (dict[str, list[str]]).
                    The dictionary containing key-value pairs about a target node and other nodes which have green edges to it.
                red_edges_target_str_and_sources_str_list_dict (dict[str, list[str]]).
                    The dictionary containing key-value pairs about a target node and other nodes which have red edges to it.
                sorted_boolean_variables_str_list (list[str]).
                    Default value is None.
                    The list of sorted Boolean variables.
        """

        # Initialize the attribute by assigning the argument to it.
        self.green_edges_target_str_and_sources_str_list_dict = green_edges_target_str_and_sources_str_list_dict
        self.red_edges_target_str_and_sources_str_list_dict = red_edges_target_str_and_sources_str_list_dict

        # If the argument does not provide sorted Boolean variables.
        if sorted_boolean_variables_str_list is None:

            # Initialize the attribute by sorting all Boolean variables.
            self.sorted_boolean_variables_str_list = sorted(self.green_edges_target_str_and_sources_str_list_dict.keys())

        # If the argument provides sorted Boolean variables.
        else:

            # Initialize the attribute by assigning the argument to it.
            self.sorted_boolean_variables_str_list = sorted_boolean_variables_str_list

        # Call the method to get the general Boolean network attribute.
        boolean_variables_str_and_boolean_expressions_callable_dict = self.convert_edges_to_general_boolean_network()

        # Call the parent constructor.
        super().__init__(boolean_variables_str_and_boolean_expressions_callable_dict, self.sorted_boolean_variables_str_list)

    def convert_edges_to_general_boolean_network(self) -> dict[str, Callable[..., bool]]:
        """
            Convert green and red edges into a general Boolean network.

            Returns:
                (dict[str, Callable[..., bool]]).
                    The dictionary containing key-value pairs about Boolean variables and their corresponding Boolean expressions.
        """

        # Initialize an empty set to store all Boolean variables.
        boolean_variables_str_set = set()

        # Iterate each line in the file:
        for boolean_variable_str in self.green_edges_target_str_and_sources_str_list_dict.keys():

            # Add the current Boolean variable into the set.
            boolean_variables_str_set.add(boolean_variable_str)

        # Initialize an empty dictionary to store Boolean variables and their corresponding Boolean expressions.
        boolean_variables_str_and_boolean_expressions_callable_dict = {}

        # Iterate each Boolean variable:
        for target_boolean_variable_str in self.sorted_boolean_variables_str_list:

            # Initialize an empty string to denote the part in the expression of green edges.
            green_edges_boolean_expression_part_str = ""

            # Iterate each source which have green edge to the target:
            for green_edge_source_boolean_variable_str in self.green_edges_target_str_and_sources_str_list_dict[target_boolean_variable_str]:

                # If the source is the target itself:
                if green_edge_source_boolean_variable_str == target_boolean_variable_str:

                    # Add the green self loop effect into the expression.
                    green_edges_boolean_expression_part_str += "(not " + target_boolean_variable_str + ") or "

                # If the source is not the target:
                else:

                    # Add the current target into the expression.
                    green_edges_boolean_expression_part_str += green_edge_source_boolean_variable_str + " or "

            # Initialize a Boolean variable to denote if the target has a red self loop.
            is_red_self_bool = False

            # Initialize an empty string to denote the part in the expression of red edges.
            red_edges_boolean_expression_part_str = ""

            # Iterate each source which have green edge to the target:
            for red_edge_source_boolean_variable_str in self.red_edges_target_str_and_sources_str_list_dict[target_boolean_variable_str]:

                # If the source is the target itself:
                if red_edge_source_boolean_variable_str == target_boolean_variable_str:

                    # Update the variable to denote the target has a red self loop.
                    is_red_self_bool = True

                # If the source is not the target:
                else:

                    # Add the current target into the expression.
                    red_edges_boolean_expression_part_str += "(not " + red_edge_source_boolean_variable_str + ") and "

            # Remove the last AND operation.
            red_edges_boolean_expression_part_str = red_edges_boolean_expression_part_str.removesuffix(" and ")

            # If the target does not have a red self loop:
            if not is_red_self_bool:
                
                # Add the red self loop effect into the expression.
                green_edges_boolean_expression_part_str += target_boolean_variable_str + " or "

            # Remove the last OR operation.
            green_edges_boolean_expression_part_str = green_edges_boolean_expression_part_str.removesuffix(" or ")

            # If both green edges and red edges have contents:
            if green_edges_boolean_expression_part_str and red_edges_boolean_expression_part_str:

                # Add parentheses for this part.
                green_edges_boolean_expression_part_str = "(" + green_edges_boolean_expression_part_str + ")"

                # Connect them to get the Boolean expression string.
                boolean_expression_str = green_edges_boolean_expression_part_str + " and " + red_edges_boolean_expression_part_str

            # If green edges have contents and red edges don't have contents:
            elif green_edges_boolean_expression_part_str and not red_edges_boolean_expression_part_str:

                # Get the Boolean expression string by only green edges.
                boolean_expression_str = green_edges_boolean_expression_part_str

            # If green edges doesn't have contents and red edges have contents:
            elif not green_edges_boolean_expression_part_str and red_edges_boolean_expression_part_str:

                # Get the Boolean expression string by only red edges.
                boolean_expression_str = red_edges_boolean_expression_part_str

            # If both green edges and red edges have no contents:
            else:

                # Get the Boolean expression string by always 0.
                boolean_expression_str = f"{target_boolean_variable_str} and (not {target_boolean_variable_str})"

            # Call the method to get tokens and indices of Boolean variables.
            boolean_expression_tokens_string_list, boolean_variables_string_and_indices_in_tokens_int_list_dictionary = convert_boolean_expression_to_tokens_and_indices(boolean_variables_str_set, boolean_expression_str)

            # Call the method to add the callable Boolean expression.
            boolean_variables_str_and_boolean_expressions_callable_dict[target_boolean_variable_str] = help_function_to_return_callable(boolean_expression_tokens_string_list, boolean_variables_string_and_indices_in_tokens_int_list_dictionary)

        # Return the dictionary containing key-value pairs about Boolean variables and their corresponding Boolean expressions.
        return boolean_variables_str_and_boolean_expressions_callable_dict
