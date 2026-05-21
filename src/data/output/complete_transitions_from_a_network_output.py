# Import to convert Boolean values to a Binary string.
from src.scripts.universal_operations import convert_boolean_dictionary_to_binary_string

# Import to create directories.
import os


def save_complete_transitions_from_a_network(transitions_dict_1d_tuple_1d_list: list[(dict[str: bool], dict[str: bool])], boolean_variables_str_and_ordered_indices_int_dict: dict[str: int], transitions_file_name_and_type_str: str):
    """
        Save all Boolean maps to a file in the format 000->011.

        Arguments:
            transitions_dict_1d_tuple_1d_list (list[(dict[str: bool], dict[str: bool])]).
                The 1-dimensional list containing all transitions as tuples.
                The first element in each tuple is a dictionary denoting binary states before.
                The second element in each tuple is a dictionary denoting binary states after.
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.
            transitions_file_name_and_type_str (str).
                The file name to save the transitions.
    """

    # Get the path of the project.
    project_directory_path_str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    # Get the path of the file containing a general boolean network.
    transitions_path_with_name_and_type_str = os.path.join(project_directory_path_str, "data/transitions", transitions_file_name_and_type_str)

    # Ensure the directory exists.
    os.makedirs(os.path.dirname(transitions_path_with_name_and_type_str), exist_ok=True)

    # Open the output path:
    with open(transitions_path_with_name_and_type_str, "w") as f:

        # Iterate each transition:
        for transitions_tuple in transitions_dict_1d_tuple_1d_list:

            # Get states before.
            states_before_boolean_variables_str_and_boolean_values_bool_dict = transitions_tuple[0]

            # Get states after.
            states_after_boolean_variables_str_and_boolean_values_bool_dict = transitions_tuple[1]

            # Get the bits of binary_states before.
            binary_states_before_str = convert_boolean_dictionary_to_binary_string(boolean_variables_str_and_boolean_values_bool_dict=states_before_boolean_variables_str_and_boolean_values_bool_dict, boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

            # Get the bits of binary_states after.
            binary_states_after_str = convert_boolean_dictionary_to_binary_string(boolean_variables_str_and_boolean_values_bool_dict=states_after_boolean_variables_str_and_boolean_values_bool_dict, boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

            # Write the transition into the file.
            f.write(f"{binary_states_before_str}-->{binary_states_after_str}\n")
