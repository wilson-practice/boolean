# Import to initialize fact graphs.
from src.boolean.factor_graph.factor_graph import FactorGraph

# Import to load transitions.
from src.data.input.states_transitions_input import load_states_transitions

# Import to initialize inferences.
from src.transitions.inference.strong_inhibition_approximate_inference import StrongInhibitionApproximateInference

# Import to initialize decomposition.
from src.transitions.inference.strong_inhibition_single_decomposition import StrongInhibitionSingleDecomposition

# Import to initialize transitions.
from src.transitions.states_transitions import StatesTransitions

# Import to compute logarithms.
import math


def load_transitions_and_check_components(transitions_name_str: str, boolean_variables_str_and_ordered_indices_int_dict: dict[str: int] = None):
    """
        Load the transitions from the argument. Convert it to an instance of StatesTransitions. Compute and print information of components.

        Arguments:
            transitions_name_str (str).
                The string denoting the name of transitions.
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                Default value is None.
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.
    """

    # Print the name of the biological system.
    print(f"Biological System: {transitions_name_str} \n")

    # Create the name of the file containing transitions.
    transitions_file_name_with_type_str = f"{transitions_name_str}.transitions"

    # Call the method to load transitions.
    transitions_dict_1d_tuple_1d_list, boolean_variables_str_and_ordered_indices_int_dict = load_states_transitions(transitions_file_name_with_type_str=transitions_file_name_with_type_str, boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

    # Initialize an instance of StatesTransitions.
    states_transitions_object = StatesTransitions(transitions_dict_1d_tuple_1d_list=transitions_dict_1d_tuple_1d_list, boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

    # Iterate each component and its index:
    for components_index_int, states_components_object in states_transitions_object.components_indices_int_and_states_components_object_dict.items():

        # Print the information of the current component.
        print(f"Component: {components_index_int}")
        print(f"Number of states: {len(states_components_object.component_decimal_states_int_and_states_nodes_object_dict)}")
        print(f"Attractor or limited cycle: {states_components_object.cycle_decimal_states_int_1d_list}")
        print()


def load_transitions_and_apply_strong_inhibition_inference_with_belief_propagation(transitions_name_str: str, boolean_variables_str_and_ordered_indices_int_dict: dict[str: int] = None) -> (dict[str: float], dict[str: float], float):
    """
        Load the transitions from the argument. Convert it to an instance of StatesTransitions. Apply an approximate inference to it based on the strong inhibition dynamics.

        Arguments:
            transitions_name_str (str).
                The string denoting the name of transitions.
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                Default value is None.
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.

        Returns:
            (dict[str: float]).
                The dictionary containing Boolean variables and probabilities of green edges to the target Boolean variable.
            (dict[str: float]).
                The dictionary containing Boolean variables and probabilities of red edges to the target Boolean variable.
            (float).
                The float denoting the final entropy.
    """

    # Call the method to load a transition.
    transitions_dict_1d_tuple_1d_list, boolean_variables_str_and_ordered_indices_int_dict = load_states_transitions(transitions_file_name_with_type_str=f"{transitions_name_str}.transitions", boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

    # Initialize an instance of StatesTransitions.
    states_transitions_object = StatesTransitions(transitions_dict_1d_tuple_1d_list=transitions_dict_1d_tuple_1d_list, boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

    # Get an inference from the strong inhibition.
    inference_object = StrongInhibitionApproximateInference(states_transitions_object=states_transitions_object, is_self_green_allowed_bool=False, is_self_red_allowed_bool=True, do_green_and_red_conflict_bool=True)

    # Initialize an empty dictionary. Each key is a Boolean variable. Each value is a dictionary containing key-value pairs about Boolean variables as string and if they have green edges to the key. Set the green self loop nonexistent.
    targets_str_and_green_sources_probabilities_dict_dict = {boolean_variable_str: {boolean_variable_str: 0.0} for boolean_variable_str in boolean_variables_str_and_ordered_indices_int_dict}

    # Initialize an empty dictionary. Each key is a Boolean variable. Each value is a dictionary containing key-value pairs about Boolean variables as string and if they have red edges to the key.
    targets_str_and_red_sources_probabilities_dict_dict = {boolean_variable_str: {} for boolean_variable_str in boolean_variables_str_and_ordered_indices_int_dict}

    # Initialize a float to denote the total entropy.
    total_entropy_float = 0.0

    # Iterate each Boolean variable:
    for target_boolean_variable_str in boolean_variables_str_and_ordered_indices_int_dict:

        # Call the method to get its CNF.
        variables_str_1d_list_cnf_clauses_2d_list = inference_object.generate_cnf_formula_for_one_boolean_variable(target_boolean_variable_str)

        # Initialize an instance of FactorGraph based on the current CNF.
        factor_graph_object = FactorGraph(variables_str_1d_list_cnf_clauses_2d_list=variables_str_1d_list_cnf_clauses_2d_list)

        # Call the method to propagate its belief.
        edges_str_and_final_belief_messages_float_1d_list_dict, current_entropy_float = factor_graph_object.propagate_belief()

        # Add the current entropy into the total one.
        total_entropy_float += current_entropy_float

        # Iterate each edge:
        for edge_str in edges_str_and_final_belief_messages_float_1d_list_dict:

            # Split the edge to its color and its source Boolean variable.
            color_str, source_boolean_variable_str = edge_str.split("_")

            # If the current edge is a green edge:
            if color_str == "G":

                # Update the current edge to add its belief into the dictionary.
                targets_str_and_green_sources_probabilities_dict_dict[target_boolean_variable_str][source_boolean_variable_str] = edges_str_and_final_belief_messages_float_1d_list_dict[edge_str][2]

            # If the current edge is a red edge:
            else:

                # Update the current edge to add its belief into the dictionary.
                targets_str_and_red_sources_probabilities_dict_dict[target_boolean_variable_str][source_boolean_variable_str] = edges_str_and_final_belief_messages_float_1d_list_dict[edge_str][2]

    # Return dictionaries to store green and red edges probabilities for different target Boolean variables.
    return targets_str_and_green_sources_probabilities_dict_dict, targets_str_and_red_sources_probabilities_dict_dict, total_entropy_float


def load_transitions_and_apply_strong_inhibition_inference_with_full_search(transitions_name_str: str, boolean_variables_str_and_ordered_indices_int_dict: dict[str: int] = None) -> (dict[str: float], dict[str: float], float):
    """
        Load the transitions from the argument. Convert it to an instance of StatesTransitions. Apply an approximate inference to it based on the strong inhibition dynamics. Enumerate all solutions.

        Arguments:
            transitions_name_str (str).
                The string denoting the name of transitions.
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                Default value is None.
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.

        Returns:
            (dict[str: float]).
                The dictionary containing Boolean variables and probabilities of green edges to the target Boolean variable.
            (dict[str: float]).
                The dictionary containing Boolean variables and probabilities of red edges to the target Boolean variable.
            (float).
                The float denoting the logarithm of number of solutions.
    """

    # Call the method to load a transition.
    transitions_dict_1d_tuple_1d_list, boolean_variables_str_and_ordered_indices_int_dict = load_states_transitions(transitions_file_name_with_type_str=f"{transitions_name_str}.transitions", boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

    # Initialize an instance of StatesTransitions.
    states_transitions_object = StatesTransitions(transitions_dict_1d_tuple_1d_list=transitions_dict_1d_tuple_1d_list, boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

    # Get an inference from the strong inhibition.
    inference_object = StrongInhibitionApproximateInference(states_transitions_object=states_transitions_object, is_self_green_allowed_bool=False, is_self_red_allowed_bool=True, do_green_and_red_conflict_bool=True)

    # Initialize a float to denote the logarithm base 10 of the number of solutions.
    logarithm_of_number_of_solutions_float = 0.0

    # Initialize dictionaries to store green and red edges probabilities for different target Boolean variables.
    target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict = {boolean_variable_str: {} for boolean_variable_str in states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}
    target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict = {boolean_variable_str: {} for boolean_variable_str in states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}

    # Initialize a Boolean variable to denote if there exists a solution or not.
    has_solutions_bool = True

    # Iterate each Boolean variable:
    for boolean_variable_str in states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict:

        # Initialize an instance of StrongInhibitionSingleDecomposition without a red self loop.
        single_decomposition_object = StrongInhibitionSingleDecomposition(inference_object=inference_object, target_boolean_variable_str=boolean_variable_str, has_green_self_bool=False, has_red_self_bool=False)

        # Call the method to check if there is a solution.
        solve_without_red_self_loop_bool = single_decomposition_object.check_if_transitions_can_fit_strong_inhibition()

        # If there exists a solution:
        if solve_without_red_self_loop_bool:

            # Initialize it again.
            single_decomposition_object = StrongInhibitionSingleDecomposition(inference_object=inference_object, target_boolean_variable_str=boolean_variable_str, has_green_self_bool=False, has_red_self_bool=False)

            # Call the method to get all solutions.
            no_red_self_solutions_dict_1d_list, no_red_self_green_sources_str_and_count_dict, no_red_self_red_sources_str_and_count_dict = single_decomposition_object.enumerate_all_solutions()

        # If there is no solution:
        else:

            # Initialize solutions as empty.
            no_red_self_solutions_dict_1d_list = []
            no_red_self_green_sources_str_and_count_dict = {current_boolean_variable_str: 0 for current_boolean_variable_str in states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}
            no_red_self_red_sources_str_and_count_dict = {current_boolean_variable_str: 0 for current_boolean_variable_str in states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}

        # Initialize an instance of StrongInhibitionSingleDecomposition with a red self loop.
        single_decomposition_object = StrongInhibitionSingleDecomposition(inference_object=inference_object, target_boolean_variable_str=boolean_variable_str, has_green_self_bool=False, has_red_self_bool=True)

        # Call the method to check if there is a solution.
        solve_with_red_self_loop_bool = single_decomposition_object.check_if_transitions_can_fit_strong_inhibition()

        # If there exists a solution:
        if solve_with_red_self_loop_bool:

            # Initialize it again.
            single_decomposition_object = StrongInhibitionSingleDecomposition(inference_object=inference_object, target_boolean_variable_str=boolean_variable_str, has_green_self_bool=False, has_red_self_bool=True)

            # Call the method to get all solutions.
            red_self_solutions_dict_1d_list, red_self_green_sources_str_and_count_dict, red_self_red_sources_str_and_count_dict = single_decomposition_object.enumerate_all_solutions()

        # If there is no solution:
        else:

            # Initialize solutions as empty.
            red_self_solutions_dict_1d_list = []
            red_self_green_sources_str_and_count_dict = {current_boolean_variable_str: 0 for current_boolean_variable_str in states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}
            red_self_red_sources_str_and_count_dict = {current_boolean_variable_str: 0 for current_boolean_variable_str in states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}

        # If there is no solution:
        if not solve_without_red_self_loop_bool and not solve_with_red_self_loop_bool:

            print("No solutions")

            # Denote that there is no solution.
            has_solutions_bool = False

            # No need to check other Boolean variables.
            break

        # If there exists a solution:
        else:

            # Get the number of solutions.
            number_of_solutions_int = len(no_red_self_solutions_dict_1d_list) + len(red_self_solutions_dict_1d_list)

            # Increment its logarithm base 10 to the total logarithm.
            logarithm_of_number_of_solutions_float += math.log(number_of_solutions_int)

            # Initialize dictionaries to store probabilities of green and red edges.
            green_sources_str_and_probabilities_float_dict = {current_boolean_variable_str: 0.0 for current_boolean_variable_str in states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}
            red_sources_str_and_probabilities_float_dict = {current_boolean_variable_str: 0.0 for current_boolean_variable_str in states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}

            # Iterate each Boolean variable:
            for current_boolean_variable_str in green_sources_str_and_probabilities_float_dict:

                # Update the probabilities of green edges.
                green_sources_str_and_probabilities_float_dict[current_boolean_variable_str] = (no_red_self_green_sources_str_and_count_dict[current_boolean_variable_str] + red_self_green_sources_str_and_count_dict[current_boolean_variable_str]) / number_of_solutions_int

                # Update the probabilities of red edges.
                red_sources_str_and_probabilities_float_dict[current_boolean_variable_str] = (no_red_self_red_sources_str_and_count_dict[current_boolean_variable_str] + red_self_red_sources_str_and_count_dict[current_boolean_variable_str]) / number_of_solutions_int

            # Update the probabilities of green and red edges for different target Boolean variables.
            target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict[boolean_variable_str] = green_sources_str_and_probabilities_float_dict
            target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict[boolean_variable_str] = red_sources_str_and_probabilities_float_dict

    # If there exists at least one solution:
    if has_solutions_bool:

        # Return dictionaries to store green and red edges probabilities for different target Boolean variables.
        return target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict, target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict, logarithm_of_number_of_solutions_float

    # If there is no solution:
    else:

        # Return all as invalid values.
        return {}, {}, 0.0
