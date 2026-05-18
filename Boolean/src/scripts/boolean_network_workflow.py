# Import to initialize general Boolean networks.
from src.boolean_network.general_boolean_network import GeneralBooleanNetwork

# Import to load general Boolean networks.
from src.data.input.general_boolean_network_input import load_general_boolean_network


def load_boolean_network_and_generate_complete_transitions(boolean_network_name_str: str):
    """
        Load the Boolean network from the argument. Convert it to an instance of GeneralBooleanNetwork. Generate complete transitions.

        Arguments:
            boolean_network_name_str (str).
                The string denoting the name of the Boolean network.
    """

    # Set the name of file containing general Boolean network.
    general_boolean_network_file_name_with_type_str = f"{boolean_network_name_str}.network"

    # Call the method to load the general Boolean networks.
    boolean_variables_str_and_boolean_expressions_callable_dict, boolean_variables_str_and_boolean_expressions_str_dict, boolean_variables_str_and_ordered_indices_int_dict = load_general_boolean_network(general_boolean_network_file_name_with_type_str=general_boolean_network_file_name_with_type_str)

    # Initialize an instance of GeneralBooleanNetwork by loaded arguments.
    general_boolean_network_object = GeneralBooleanNetwork(boolean_variables_str_and_boolean_expressions_callable_dict=boolean_variables_str_and_boolean_expressions_callable_dict, boolean_variables_str_and_boolean_expressions_str_dict=boolean_variables_str_and_boolean_expressions_str_dict, boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

    # Set the name of file containing complete transitions.
    complete_transitions_file_name_with_type_str = f"{boolean_network_name_str}_complete.transitions"

    # Call the method to generate complete transitions.
    general_boolean_network_object.generate_complete_transitions(complete_transitions_file_name_with_type_str=complete_transitions_file_name_with_type_str)
