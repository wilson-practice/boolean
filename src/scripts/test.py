# Import to initialize factor graphs.
from src.boolean.factor_graph.factor_graph import FactorGraph

# Import to compute the exponentiation.
import math


def test_belief_propagation():
    """
        Initialize factor graphs by specific CNF. Run its Belief Propagation and compare them with the correct results.
    """

    # Define the test case.
    variables_str_1d_list_cnf_clauses_2d_list = [["+1", "+2", "-3"], ["-3", "-4", "+5"], ["+3", "-6", "-7"]]

    # Print the Boolean formula in the testcase.
    print("Testcase: (X1 or X2 or (not X3)) and ((not X3) or (not X4) or X5) and (X3 or (not X6) or (not X7)) \n")

    # Define the correct result.
    variables_str_and_correct_final_belief_messages_float_dict = {
        "1": 4 / 7,
        "2": 4 / 7,
        "3": 3 / 7,
        "4": 3 / 7,
        "5": 4 / 7,
        "6": 17 / 42,
        "7": 17 / 42,
    }

    # Initialize an instance of FactorGraph based on the current CNF.
    factor_graph_object = FactorGraph(variables_str_1d_list_cnf_clauses_2d_list)

    # Call the method to propagate its belief.
    variables_str_and_final_belief_messages_float_1d_list_dict, entropy_float = factor_graph_object.propagate_belief()

    # Initialize a float to denote the sum of differences between belief from BP and the real belief.
    sum_of_belief_differences_float = 0.0

    # Iterate each variable:
    for variable_str in variables_str_and_final_belief_messages_float_1d_list_dict:

        # Get the current final belief.
        final_belief_message_float = variables_str_and_final_belief_messages_float_1d_list_dict[variable_str][2]

        # Get the current correct final belief.
        correct_final_belief_message_float = variables_str_and_correct_final_belief_messages_float_dict[variable_str]

        # Compute the difference between belief from BP and the real belief.
        belief_difference_float = final_belief_message_float - correct_final_belief_message_float

        # Add the current difference into the sum.
        sum_of_belief_differences_float += belief_difference_float

        # Print the current checking.
        print(f"Variable: X{variable_str}")
        print(f"BP Belief = {final_belief_message_float}")
        print(f"Real Belief = {correct_final_belief_message_float}")
        print(f"Difference = {belief_difference_float}\n")

    # Print to denote that the following is a summary.
    print("----- Summary ------")

    # Print the sum of differences.
    print(f"Sum of differences = {sum_of_belief_differences_float}")

    # Print the entropy from the belief propagation.
    print(f"BP Entropy = {entropy_float}")

    # Print the number of solutions.
    print(f"Predicted number of solutions = {math.exp(entropy_float)}")

    # Print the number of solutions.
    print(f"Real number of solutions = 84 \n")

