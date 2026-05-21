# Import to visualize.
from src.visualization.values_visualization import visualize_belief_propagation_and_full_search

# Import to compute logarithms.
import numpy as np

def convert_boolean_dictionary_to_binary_string(boolean_variables_str_and_boolean_values_bool_dict, boolean_variables_str_and_ordered_indices_int_dict) -> str:
    """
        Convert a dictionary containing Boolean variables and their Boolean values to a binary string.

        Arguments:
            boolean_variables_str_and_boolean_values_bool_dict (dict[str: bool]).
                The dictionary containing key-value pairs about Boolean variables string and their corresponding Boolean values.
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.

        Returns:
            (str).
                The string denoting the converted Binary number.
    """

    # Initialize a 1-dimensional list to store the converted Binary string.
    binary_str_1d_list = ["0"] * len(boolean_variables_str_and_boolean_values_bool_dict)

    # Iterate each Boolean variable:
    for boolean_variable_str in boolean_variables_str_and_boolean_values_bool_dict:

        # Get the index of the current Boolean variable:
        order_index_int = boolean_variables_str_and_ordered_indices_int_dict[boolean_variable_str]

        # Access the Boolean value of the current Boolean variable. If it is True, then set its corresponding bit as "1"; otherwise, set its corresponding bit as "0".
        binary_str_1d_list[order_index_int] = "1" if boolean_variables_str_and_boolean_values_bool_dict[boolean_variable_str] else "0"

    # Return the converted Binary string.
    return " ".join(binary_str_1d_list)


def convert_binary_string_to_boolean_dictionary(binary_str: str, boolean_variables_str_and_ordered_indices_int_dict: dict[str: int]) -> dict[str: bool]:
    """
        Convert a binary string to a dictionary containing Boolean variables and their Boolean values.

        Arguments:
            binary_str (str).
                The string denoting the converted Binary number.
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.

        Returns:
            (dict[str: bool]).
                The dictionary containing key-value pairs about Boolean variables string and their corresponding Boolean values.
    """

    # Split the string into a 1-dimensional list.
    binary_states_str_1d_list = binary_str.split()

    # Initialize a dictionary to store key-value pairs about Boolean variables string.
    boolean_variables_str_and_boolean_values_bool_dict = {}

    # Iterate each Boolean variable and their corresponding order index:
    for boolean_variable_str, ordered_index_int in boolean_variables_str_and_ordered_indices_int_dict.items():

        # Check if the current Boolean variable has a "1" at its corresponding index. Store it with the Boolean variable True into the dictionary.
        boolean_variables_str_and_boolean_values_bool_dict[boolean_variable_str] = binary_states_str_1d_list[ordered_index_int] == "1"

    # Return the dictionary containing key-value pairs about Boolean variables string and their corresponding Boolean values.
    return boolean_variables_str_and_boolean_values_bool_dict


def boolean_str_1d_list_to_decimal_int(boolean_variables_str_1d_list: list[str], boolean_variables_str_and_ordered_indices_int_dict: dict[str: int]) -> int:
    """
        Convert a 1-dimensional list containing Boolean variables to its decimal format.

        Arguments:
            boolean_variables_str_1d_list (list[str]).
                The 1-dimensional list containing Boolean variables as string.
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.

        Returns:
            (int).
                The integer denoting the decimal format of the 1-dimensional list containing Boolean variables.
    """

    # Initialize an integer to denote the decimal format of the 1-dimensional list.
    decimal_int = 0

    # Iterate each Boolean variable in the list:
    for boolean_variable_str in boolean_variables_str_1d_list:

        # Update the decimal format.
        decimal_int |= 1 << boolean_variables_str_and_ordered_indices_int_dict[boolean_variable_str]

    # Return the integer denoting the decimal format of the 1-dimensional list containing Boolean variables.
    return decimal_int


def find(member_id_int: int, members_ids_int_and_leaders_ids_int_dict: dict[int: int]) -> int:
    """
        Given an ID of a member, find the ID of its leader.

        Arguments:
            member_id_int (int).
                The integer denoting the ID of a member.
            members_ids_int_and_leaders_ids_int_dict (dict[int: int]).
                The dictionary containing key-value pairs about IDs of members and the IDs of their corresponding leaders.

        Returns:
            (int).
                The integer denoting the ID of the leader of the member.
    """

    # If the ID of this member is not the ID of its leader:
    if members_ids_int_and_leaders_ids_int_dict[member_id_int] != member_id_int:

        # Call the recursive method to find the ID of its final leader.
        final_leader_id_int = find(members_ids_int_and_leaders_ids_int_dict[member_id_int], members_ids_int_and_leaders_ids_int_dict)

        # Update the ID of its leader as the ID of its final leader.
        members_ids_int_and_leaders_ids_int_dict[member_id_int] = final_leader_id_int

        # Return its updated group.
        return members_ids_int_and_leaders_ids_int_dict[member_id_int]

    # If the ID of this member is the ID of its leader:
    else:

        # Return its ID directly.
        return member_id_int


def union(first_member_id_int: int, second_member_id_int: int, members_ids_int_and_leaders_ids_int_dict: dict[int: int]):
    """
        Merge two members into one group.

        Arguments:
            first_member_id_int (int).
                The integer denoting the ID of the first member.
            second_member_id_int (int).
                The integer denoting the ID of the second member.
            members_ids_int_and_leaders_ids_int_dict (dict[int: int]).
                The dictionary containing key-value pairs about IDs of members and the IDs of their corresponding leaders.
    """

    # Call the method to find the ID of the final leader of the first member.
    first_final_leader_id_int = find(first_member_id_int, members_ids_int_and_leaders_ids_int_dict)

    # Call the method to find the ID of the final leader of the second member.
    second_final_leader_id_int = find(second_member_id_int, members_ids_int_and_leaders_ids_int_dict)

    # If these two final leader have different IDs:
    if first_final_leader_id_int != second_final_leader_id_int:

        # Update the final leader of the second member as the final leader of the first member.
        members_ids_int_and_leaders_ids_int_dict[second_final_leader_id_int] = first_final_leader_id_int


def compare_belief_propagation_with_full_search(bp_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict: dict[str: dict[str: float]], bp_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict: dict[str: dict[str: float]], bp_entropy_float: float, fs_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict: dict[str: dict[str: float]], fs_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict: dict[str: dict[str: float]], fs_logarithm_of_number_of_solutions_float: float):
    """
        Compare Belief Propagation results with Full Search results.

        Arguments:
            bp_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict (dict[str: dict[str: float]]).
                The dictionary containing key-value pairs about target Boolean variables and green sources Boolean variables with probabilities from Belief Propagation.
            bp_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict (dict[str: dict[str: float]]).
                The dictionary containing key-value pairs about target Boolean variables and red sources Boolean variables with probabilities from Belief Propagation.
            bp_entropy_float (float).
                The float denoting the entropy from Belief Propagation.
            fs_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict (dict[str: dict[str: float]]).
                The dictionary containing key-value pairs about target Boolean variables and green sources Boolean variables with probabilities from Full Search.
            fs_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict (dict[str: dict[str: float]]).
                The dictionary containing key-value pairs about target Boolean variables and red sources Boolean variables with probabilities from Full Search.
            fs_logarithm_of_number_of_solutions_float (float)
                The float denoting the logarithm of number of solutions from Full Search.
    """

    # Initialize an empty 1-dimensional list to store probabilities of BP.
    bp_probabilities_float_1d_list = []

    # Initialize an empty 1-dimensional list to store probabilities of FS.
    fs_probabilities_float_1d_list = []

    # Iterate each Boolean variable as the targets:
    for target_boolean_variable_str in bp_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict:

        # Iterate each Boolean variable as the sources:
        for source_boolean_variable_str in bp_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict:

            # Append the probability of the current green edge into the list of BP.
            bp_probabilities_float_1d_list.append(bp_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict[target_boolean_variable_str][source_boolean_variable_str])

            # Append the probability of the current green edge into the list of FS.
            fs_probabilities_float_1d_list.append(fs_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict[target_boolean_variable_str][source_boolean_variable_str])

    # Iterate each Boolean variable as the targets:
    for target_boolean_variable_str in bp_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict:

        # Iterate each Boolean variable as the sources:
        for source_boolean_variable_str in bp_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict:

            # Append the probability of the current red edge into the list of BP.
            bp_probabilities_float_1d_list.append(bp_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict[target_boolean_variable_str][source_boolean_variable_str])

            # Append the probability of the current red edge into the list of FS.
            fs_probabilities_float_1d_list.append(fs_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict[target_boolean_variable_str][source_boolean_variable_str])

    # Print the predicted number of solutions from Belief Propagation.
    print(f"BP predicted number of solutions: 10^{bp_entropy_float * np.log10(np.e):.2f}")

    # Print the read number of solutions from Full Search.
    print(f"Real number of solutions: 10^{fs_logarithm_of_number_of_solutions_float * np.log10(np.e):.2f}")

    # Call the method to visualize and compare Belief Propagation and Full Search.
    visualize_belief_propagation_and_full_search(bp_float_1d_list=bp_probabilities_float_1d_list, fs_float_1d_list=fs_probabilities_float_1d_list)
