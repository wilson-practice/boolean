# Import to load transitions from files.
from src.scripts.universal_operations import convert_binary_string_to_boolean_dictionary

# Import to store data.
import numpy as np


def load_states_transitions(transitions_file_name_with_type_str: str, boolean_variables_str_and_ordered_indices_int_dict: dict[str: int] = None) -> (list[(dict[str: bool], dict[str: bool])], dict[str: int]):
    """
        Load the file containing transitions.

        Arguments:
            transitions_file_name_with_type_str (str).
                The name of the file containing transitions with the type of the file.
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                Default value is None.
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.

        Returns:
            (list[(dict[str: bool], dict[str: bool])]).
                The 1-dimensional list containing all transitions as tuples.
                The first element in each tuple is a dictionary denoting binary states before.
                The second element in each tuple is a dictionary denoting binary states after.
            (dict[str: int]).
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.
    """

    # Get the path of this file.
    transitions_file_path_with_type_str = f"data/transitions/{transitions_file_name_with_type_str}"

    # Initialize an empty list to store transitions as tuples.
    transitions_dict_1d_tuple_1d_list = []

    # If the order of Boolean variables is not provided explicitly:
    if boolean_variables_str_and_ordered_indices_int_dict is None:

        # Initialize the dictionary containing the order as an empty dictionary.
        boolean_variables_str_and_ordered_indices_int_dict = {}

        # Initialize a Boolean variable to denote that the order indices should not be updated.
        need_boolean_variables_str_and_ordered_indices_int_dict_bool = True

    # If the order of Boolean variables is provided explicitly:
    else:

        # Initialize a Boolean variable to denote that the order indices should be updated.
        need_boolean_variables_str_and_ordered_indices_int_dict_bool = False

    # Open the file containing the transitions.
    with open(transitions_file_path_with_type_str, "r") as transitions_file:

        # If the order indices should be updated:
        if need_boolean_variables_str_and_ordered_indices_int_dict_bool:

            # Get the first transition.
            first_transition_line_str = transitions_file.readline().strip()

            # Split the first transition to get the number of Boolean variables.
            number_of_boolean_variables_int = len(first_transition_line_str.strip("\n").split("-->")[0].split(" "))

            # Iterate each index of Boolean variables:
            for boolean_variable_index_int in range(number_of_boolean_variables_int):

                # Use the index as the name of the Boolean variable and its order.
                boolean_variables_str_and_ordered_indices_int_dict[str(boolean_variable_index_int)] = boolean_variable_index_int

            # Go back to the beginning.
            transitions_file.seek(0)

        # Iterate each line of the file:
        for transition_line_str in transitions_file:

            # Split the current states before and the current states after through the arrow "-->".
            binary_states_before_str_and_binary_states_after_str_list = transition_line_str.strip("\n").split("-->")

            # The current states before are on the left side. Split it through the spaces to get a list of strings.
            binary_states_before_str_list = binary_states_before_str_and_binary_states_after_str_list[0].split(" ")

            # The current states after are on the right side. Split it through the spaces to get a list of strings.
            binary_states_after_str_list = binary_states_before_str_and_binary_states_after_str_list[1].split(" ")

            # Convert states before as Boolean variables with their Boolean assignments.
            boolean_variables_str_and_states_before_bool_dict = convert_binary_string_to_boolean_dictionary(binary_str=" ".join(binary_states_before_str_list), boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

            # Convert states after as Boolean variables with their Boolean assignments.
            boolean_variables_str_and_states_after_bool_dict = convert_binary_string_to_boolean_dictionary(binary_str=" ".join(binary_states_after_str_list), boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

            # Append the current transition as a tuple into the list.
            transitions_dict_1d_tuple_1d_list.append((boolean_variables_str_and_states_before_bool_dict, boolean_variables_str_and_states_after_bool_dict))

    # Return the 1-dimensional list containing transitions and ordered indices.
    return transitions_dict_1d_tuple_1d_list, boolean_variables_str_and_ordered_indices_int_dict


def load_states_transitions_as_processes(transitions_file_name_with_type_str: str) -> np.ndarray:
    """
        Load the file containing transitions as processes.

        Arguments:
            transitions_file_name_with_type_str (str).
                The name of the file containing transitions with the type of the file.

        Returns:
            (np.ndarray).
                The 2-dimensional array containing decimal integers of binary values.
    """

    # Get the path of this file.
    transitions_file_path_with_type_str = f"data/transitions/{transitions_file_name_with_type_str}.transitions"

    # Initialize an empty 1-dimensional list to store the process as a 2-dimensional list.
    decimal_int_2d_list = []
    last_right_decimal_int_1d_list = None

    # Open the file containing the transitions.
    with open(transitions_file_path_with_type_str, "r") as transitions_file:

        # Iterate each line:
        for file_line_str in transitions_file:

            # Split the line as the left and the right parts.
            left_str, right_str = file_line_str.strip().split("-->")

            # Split the left part using spaces and convert them to integers.
            left_decimal_int_1d_list = [int(decimal_str) for decimal_str in left_str.split()]

            # Split the right part using spaces and convert them to integers.
            right_decimal_int_1d_list = [int(decimal_str) for decimal_str in right_str.split()]

            # Append the left part into the 2-dimensional list.
            decimal_int_2d_list.append(left_decimal_int_1d_list)

            # Update the last right part.
            last_right_decimal_int_1d_list = right_decimal_int_1d_list

    # Append the last right part into the list.
    decimal_int_2d_list.append(last_right_decimal_int_1d_list)

    # Convert the 2-dimensional list into a numpy array and return it.
    return np.array(decimal_int_2d_list, dtype=int)


def load_process(decimal_int_2d_array: np.ndarray, boolean_variables_str_and_ordered_indices_int_dict: dict[str: int] = None) -> (list[(dict[str: bool], dict[str: bool])], dict[str: int]):
    """
        Load the file containing transitions.

        Arguments:
            decimal_int_2d_array (np.ndarray).
                The 2-dimensional array containing decimal integers of binary values.
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                Default value is None.
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.

        Returns:
            (list[(dict[str: bool], dict[str: bool])]).
                The 1-dimensional list containing all transitions as tuples.
                The first element in each tuple is a dictionary denoting binary states before.
                The second element in each tuple is a dictionary denoting binary states after.
            (dict[str: int]).
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.
    """

    transitions_dict_1d_tuple_1d_list = []

    # Iterate each index of rows:
    for row_index_int in range(decimal_int_2d_array.shape[0] - 1):

        # Get the states before.
        states_before_int_1d_list = decimal_int_2d_array[row_index_int]

        # Get the states after.
        states_after_int_1d_list = decimal_int_2d_array[row_index_int + 1]

        # Convert states before to a string.
        states_before_str = " ".join(map(str, states_before_int_1d_list))

        # Convert states after to a string.
        states_after_str = " ".join(map(str, states_after_int_1d_list))

        # Get states before as a dictionary.
        boolean_variables_str_and_states_before_bool_dict = convert_binary_string_to_boolean_dictionary(binary_str=states_before_str, boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

        # Get states after as a dictionary.
        boolean_variables_str_and_states_after_bool_dict = convert_binary_string_to_boolean_dictionary(binary_str=states_after_str, boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

        # Append the current transition into the list.
        transitions_dict_1d_tuple_1d_list.append((boolean_variables_str_and_states_before_bool_dict, boolean_variables_str_and_states_after_bool_dict))

    # Return transitions and ordered indices.
    return transitions_dict_1d_tuple_1d_list, boolean_variables_str_and_ordered_indices_int_dict
