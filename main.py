# Import configuration.
from src.config import BIOLOGICAL_SYSTEM_NAME, COMMAND_NAME

# Import to load Boolean networks and generate complete transitions.
from src.scripts.boolean_network_workflow import load_boolean_network_and_generate_complete_transitions

# Import to test Belief Propagation.
from src.scripts.test import test_belief_propagation

# Import to load transitions and check components.
from src.scripts.transitions_workflow import load_transitions_and_check_components, load_transitions_and_apply_strong_inhibition_inference_with_belief_propagation, load_transitions_and_apply_strong_inhibition_inference_with_full_search

# Import to compare Belief Propagation results with Full Search results.
from src.scripts.universal_operations import compare_belief_propagation_with_full_search

import math
# Call the main method:
if __name__ == "__main__":

    # Set the name of biological system.
    client_name_str = BIOLOGICAL_SYSTEM_NAME

    # If the current command loads a Boolean network as an input and generates all transitions from this Boolean network:
    if COMMAND_NAME == "Complete Transitions Generation":

        # Load Boolean networks and generate complete transitions.
        load_boolean_network_and_generate_complete_transitions(boolean_network_name_str=client_name_str)

    # If the current command loads transitions as an input and checks the structure of transitions:
    elif COMMAND_NAME == "Analyze Transitions Structure":

        # Load transitions and check components.
        load_transitions_and_check_components(transitions_name_str=f"{client_name_str}")

    # If the current command loads transitions as an input and checks if it can follow Strong Inhibition dynamics or not:
    elif COMMAND_NAME == "Strong Inhibition Inference":

        # Load transitions and apply an approximate inference based on strong inhibition with Belief Propagation.
        bp_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict, bp_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict, total_entropy_float = load_transitions_and_apply_strong_inhibition_inference_with_belief_propagation(transitions_name_str=client_name_str)

        # Load transitions and apply an approximate inference based on strong inhibition with Full Search.
        fs_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict, fs_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict, logarithm_of_number_of_solutions_float = load_transitions_and_apply_strong_inhibition_inference_with_full_search(transitions_name_str=client_name_str)
        
        # Call the method to compare Belief Propagation results with Full Search results.
        compare_belief_propagation_with_full_search(bp_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict=bp_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict, bp_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict=bp_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict, fs_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict=fs_target_boolean_variables_str_and_green_sources_str_and_probabilities_float_dict, fs_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict=fs_target_boolean_variables_str_and_red_sources_str_and_probabilities_float_dict)

    # If the current command run testcases of Belief Propagation:
    elif COMMAND_NAME == "Test Belief Propagation":

        # Run the testcase of Belief Propagation.
        test_belief_propagation()
