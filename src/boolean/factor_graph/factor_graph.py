# Import to do the typing.
from src.boolean.factor_graph.factor import Factor

# Import to do the typing.
from src.boolean.factor_graph.variable import Variable

# Import to compute logarithms.
import math

# Import to generate the random order.
import numpy as np


class FactorGraph:
    """
        The class denotes the factor graph converted by the CNF.

        Attributes:
            variables_str_1d_list_cnf_clauses_2d_list (list[str]).
                A 2-dimensional list, and its each member is a 1-dimensional list about a clause.
                The clause consists of some variables connected with spaces.
                For each variable:
                    For the first prefix symbol,
                        If the first prefix symbol is +, then its corresponding edge can exist;
                        If the first prefix symbol is -, then its corresponding edge cannot exist;
                    For the second prefix symbol,
                        If the second prefix symbol is G_, then its corresponding edge is a green edge;
                        If the second prefix symbol is R_, then its corresponding edge is a red edge.
            variables_id_str_and_variables_object_dict (dict[str: Variable]).
                The dictionary containing key-value pairs about Boolean variables ID and their corresponding Variable objects.
            variables_object_to_factors_object_edges_tuple_1d_list (list[(Variable, Factor)]).
                The 1-dimensional list containing tuples denoting edges in the factor graph.
                Each tuple has two elements:
                    The first element is an object of Variable.
                    The second element is an object of Factor
                    The variable is a member of the clause denoted by the factor.
            variables_object_to_factors_object_edges_tuple_and_indices_int_dict (dict[(Variable, Factor):int]).
                The dictionary containing key-value pairs about edges and their corresponding indices.
                Each key is the tuple denoting an edge between a variable to a factor.
                Each value is the index of this edge.
            factor_object_set (set[Factor]).
                The set containing instances of Factor.
    """

    def __init__(self, variables_str_1d_list_cnf_clauses_2d_list: list[list[str]]):
        """
            Construct objects by initializing attributes.

            Arguments:
                variables_str_1d_list_cnf_clauses_2d_list (list[str]).
                    If it is None, then it means that there exists contradiction and there is no solution.
                    If it is empty, then this formula has been satisfied. Otherwise:
                        It is a 2-dimensional list.
                        Each list is a 1-dimensional list about a clause containing elements as string.
                        Each string denotes a variable:
                            For the first prefix symbol,
                                If the first prefix symbol is +, then its corresponding edge can exist;
                                If the first prefix symbol is -, then its corresponding edge cannot exist;
                            For the second prefix symbol,
                                If the second prefix symbol is G_, then its corresponding edge is a green edge;
                                If the second prefix symbol is R_, then its corresponding edge is a red edge.
        """

        # Initialize attributes by assigning arguments to them.
        self.variables_str_1d_list_cnf_clauses_2d_list = variables_str_1d_list_cnf_clauses_2d_list

        # Initialize the attribute as an empty dictionary.
        self.variables_id_str_and_variables_object_dict = {}

        # Initialize the attribute as an empty list.
        self.variables_object_to_factors_object_edges_tuple_1d_list = []

        # Initialize the attribute as an empty dictionary.
        self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict = {}

        # Initialize the attribute as an empty set.
        self.factor_object_set = set()

        # Call the method to initialize the factor graph.
        self.initialize_factor_graph()

    def initialize_factor_graph(self):
        """
            Construct the factor graph.
        """

        # Iterate each clause:
        for variables_str_1d_list in self.variables_str_1d_list_cnf_clauses_2d_list:

            # Initialize the current clause as an object of Factor.
            factor_object = Factor()

            # Iterate each Boolean variable in the current clause:
            for variable_str in variables_str_1d_list:

                # Extract the ID of this Boolean variable.
                variable_id_str = variable_str[1:]

                # If the ID is not in the attribute dictionary:
                if variable_id_str not in self.variables_id_str_and_variables_object_dict:

                    # Initialize and add the current object of Variable into the attribute dictionary.
                    self.variables_id_str_and_variables_object_dict[variable_id_str] = Variable(variable_id_str)

                # Get the object of Variable from the attribute dictionary.
                variable_object = self.variables_id_str_and_variables_object_dict[variable_id_str]

                # If the current variable has a positive literal in the current clause:
                if variable_str[0] == "+":

                    # Add the current variable as a member with the positive literal of the current factor.
                    factor_object.add_a_variable_with_positive_literal(variable_object)

                    # Add the current factor as a member with the positive literal of the current variable.
                    variable_object.add_a_factor_with_positive_literal(factor_object)

                # If the current clause has a negative literal in the current variable:
                else:

                    # Add the current variable as a member with the negative literal of the current factor.
                    factor_object.add_a_variable_with_negative_literal(variable_object)

                    # Add the current factor as a member with the negative literal of the current variable.
                    variable_object.add_a_factor_with_negative_literal(factor_object)

            # Add the current Factor into the attribute set.
            self.factor_object_set.add(factor_object)

        # Iterate each variable:
        for variable_id_str in self.variables_id_str_and_variables_object_dict:

            # Get the current object of Variable.
            variable_object = self.variables_id_str_and_variables_object_dict[variable_id_str]

            # Iterate each factor with the variable in it which has the positive literal:
            for positive_literal_factor_object in variable_object.positive_literal_factors_object_set:

                # Append the tuple to the end of the attribute list as an edge.
                self.variables_object_to_factors_object_edges_tuple_1d_list.append((variable_object, positive_literal_factor_object))

            # Iterate each factor with the variable in it which has the negative literal:
            for negative_literal_factor_object in variable_object.negative_literal_factors_object_set:

                # Append the tuple to the end of the attribute list as an edge.
                self.variables_object_to_factors_object_edges_tuple_1d_list.append((variable_object, negative_literal_factor_object))

        # Iterate each index of factor edges:
        for edge_index_int in range(len(self.variables_object_to_factors_object_edges_tuple_1d_list)):

            # Map the current index to the current edge tuple.
            self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[self.variables_object_to_factors_object_edges_tuple_1d_list[edge_index_int]] = edge_index_int

    def propagate_belief_(self, precision_float: float = 0.0001, number_of_iterations_int: int = 1000) -> (dict[int: list[float]], float):
        """
            Propagate messages in the factor graph.

            Arguments:
                precision_float (float).
                    Default is 0.0001.
                    The float denoting the required precision before the iteration ends.
                number_of_iterations_int (int).
                    Default is 1000.
                    The integer denoting the maximum number of iterations.

            Returns:
                (dict[str: list[float]]).
                    The dictionary containing key-value pairs about Boolean variables and their corresponding marginal probabilities.
                    Each key is a string denoting a Boolean variable.
                    Each value is a list with 3 float numbers. The last one is its marginal probability.
                (float).
                    The float denoting the entropy.
        """

        # Create a list to store belief messages of all edges. Initialize all belief messages randomly.
        belief_messages_before_float_1d_array = np.random.rand(len(self.variables_object_to_factors_object_edges_tuple_1d_list))

        # DeepCopy the list of all belief messages to create a list to update messages.
        belief_messages_current_float_1d_array = belief_messages_before_float_1d_array.copy()

        # For each iteration:
        for _ in range(number_of_iterations_int):

            # Create a 1-dimensional array to store all indices of edges in the factor graph.
            indices_of_edges_1d_array = np.arange(len(self.variables_object_to_factors_object_edges_tuple_1d_list))

            # Shuffle indices of edges in the factor graph.
            np.random.shuffle(indices_of_edges_1d_array)

            # Iterate each index of edges in the factor graph:
            for edge_index_int in indices_of_edges_1d_array:

                # Get the variable and the factor from the current edge.
                current_variable_object, current_factor_object = self.variables_object_to_factors_object_edges_tuple_1d_list[edge_index_int]

                # Create a float to store the new belief message of this edge. Initialize it as 1.0.
                edge_new_belief_message_float = 1.0

                # Iterate each variable with the positive literal in the current factor:
                for other_variable_object in current_factor_object.positive_literal_variables_id_str_and_variables_object_dict.values():

                    # Only if this is not the current variable:
                    if other_variable_object != current_variable_object:

                        # Create a float to store the product of negative belief messages from friendly factors. Initialize it as 1.0.
                        p_u_float = 1.0

                        # Create a float to store the product of negative belief messages from opposite factors. Initialize it as 1.0.
                        p_s_float = 1.0

                        # Iterate each factor with this variable which has the positive literal:
                        for other_factor_object in other_variable_object.positive_literal_factors_object_set:

                            # Because this variable has the positive literal in the current factor, only if this factor is not the current factor:
                            if other_factor_object != current_factor_object:

                                # With this variable and this clause, get the index of this edge.
                                belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(other_variable_object, other_factor_object)]

                                # Multiply the product of negative belief messages from friendly factors by the negative belief message of this edge.
                                p_u_float *= (1 - belief_messages_current_float_1d_array[belief_message_index_int])

                        # Iterate each factor with this variable which has the negative literal:
                        for other_factor_object in other_variable_object.negative_literal_factors_object_set:

                            # With this variable and this clause, get the index of this edge.
                            belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(other_variable_object, other_factor_object)]

                            # Multiply the product of negative belief messages from opposite factors by the negative belief message of this edge.
                            p_s_float *= (1 - belief_messages_current_float_1d_array[belief_message_index_int])

                        # Multiply the new belief message of this edge by the fraction.
                        edge_new_belief_message_float *= p_u_float / (p_u_float + p_s_float)

                # Iterate each variable with the negative literal in the current factor:
                for other_variable_object in current_factor_object.negative_literal_variables_id_str_and_variables_object_dict.values():

                    # Only if this is not the current variable:
                    if other_variable_object != current_variable_object:

                        # Create a float to store the product of negative belief messages from friendly factors. Initialize it as 1.0.
                        p_u_float = 1

                        # Create a float to store the product of negative belief messages from opposite factors. Initialize it as 1.0.
                        p_s_float = 1

                        # Iterate each factor with this variable which has the positive literal:
                        for other_factor_object in other_variable_object.positive_literal_factors_object_set:

                            # With this variable and this clause, get the index of this edge.
                            belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(other_variable_object, other_factor_object)]

                            # Multiply the product of negative belief messages from opposite factors by the negative belief message of this edge.
                            p_s_float *= (1 - belief_messages_current_float_1d_array[belief_message_index_int])

                        # Iterate each factor with this variable which has the negative literal:
                        for other_factor_object in other_variable_object.negative_literal_factors_object_set:

                            # Because this variable is negative in the current factor, only if this factor is not the current factor:
                            if other_factor_object != current_factor_object:

                                # With this variable and this factor, get the index of this edge.
                                belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(other_variable_object, other_factor_object)]

                                # Multiply the product of negative belief messages from friendly factors by the negative belief message of this edge.
                                p_u_float *= (1 - belief_messages_current_float_1d_array[belief_message_index_int])

                        # Multiply the new belief message of this edge by the fraction.
                        edge_new_belief_message_float *= p_u_float / (p_u_float + p_s_float)

                # Update the new belief message of the current edge as the result.
                belief_messages_current_float_1d_array[edge_index_int] = edge_new_belief_message_float

            # Create a Boolean variable to check if the result is converged or not.
            is_converged_bool = True

            # Iterate each index of edges in the factor graph:
            for belief_message_index_int in range(len(belief_messages_before_float_1d_array)):

                # If the change of the belief message of the current edge exceeds the precision:
                if abs(belief_messages_before_float_1d_array[belief_message_index_int] - belief_messages_current_float_1d_array[belief_message_index_int]) > precision_float:

                    # The result is not converged. Set the Boolean variable to False.
                    is_converged_bool = False

                    # Break the loop.
                    break

            # If the result is converged:
            if is_converged_bool:

                # Break the loop because there is no need to iterate.
                break

            # If the result is not converged:
            else:

                # DeepCopy the current belief messages as the belief messages before for the next iteration.
                belief_messages_before_float_1d_array = belief_messages_current_float_1d_array.copy()

        # Create a dictionary to store the final belief messages of all variables in the factor graph.
        variables_id_str_and_final_belief_messages_float_1d_list_dict = {}

        # Iterate each variable in the factor graph:
        for variable_id_str in self.variables_id_str_and_variables_object_dict:

            # Initialize the final belief messages of the current variable.
            # [0] is the product of belief messages from factors which has positive literals of the current Boolean variable. Initialize it as 1.
            # [1] is the product of belief messages from factors which has negative literals of the current Boolean variable. Initialize it as 1.
            # [2] is the final belief message of the current variable. Initialize it as 0.
            variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str] = [1.0, 1.0, 0.0]

        # Iterate each index of edges in the factor graph:
        for belief_message_index_int in range(len(belief_messages_current_float_1d_array)):

            # Get the variable and the factor from the current edge.
            current_variable_object, current_factor_object = self.variables_object_to_factors_object_edges_tuple_1d_list[belief_message_index_int]

            # If the current variable has positive literal in the current factor:
            if current_factor_object in current_variable_object.positive_literal_factors_object_set:

                # Multiply the product of belief messages from friendly factors by the belief message of this edge.
                variables_id_str_and_final_belief_messages_float_1d_list_dict[current_variable_object.variable_id_str][0] *= (1 - belief_messages_current_float_1d_array[belief_message_index_int])

            # If the current variable has negative literal in the current factor:
            else:

                # Multiply the product of belief messages from opposite factors by the belief message of this edge.
                variables_id_str_and_final_belief_messages_float_1d_list_dict[current_variable_object.variable_id_str][1] *= (1 - belief_messages_current_float_1d_array[belief_message_index_int])

        # Iterate each variable in the factor graph:
        for variable_id_str in self.variables_id_str_and_variables_object_dict:

            # Compute and store the final belief message of the current variable.
            variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str][2] = variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str][1] / (variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str][0] + variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str][1])

        # Initialize a float to denote the first part of the entropy.
        entropy_first_part_float = 0.0

        # Iterate each factor:
        for factor_object in self.factor_object_set:

            # Initialize a float to denote the sub part 1 in the first part of the entropy.
            entropy_first_sub_part_1_float = 1.0

            # Initialize a float to denote the sub part 2 in the first part of the entropy.
            entropy_first_sub_part_2_float = 1.0

            # Iterate each variable in the factor graph:
            for variable_id_str in self.variables_id_str_and_variables_object_dict:

                # Create a float to store the product of belief messages from friendly factors. Initialize it as 1.0.
                vs_float = 1.0

                # Create a float to store the product of belief messages from opposite factors. Initialize it as 1.0.
                vu_float = 1.0

                # Get the current variable object.
                variable_object = self.variables_id_str_and_variables_object_dict[variable_id_str]

                # If the current factor has a positive literal of the current variable:
                if factor_object in variable_object.positive_literal_factors_object_set:

                    # Iterate each friendly factor:
                    for other_factor_object in variable_object.positive_literal_factors_object_set:

                        # Only if this is not the current factor:
                        if factor_object != other_factor_object:

                            # Get the index of the edge.
                            belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(variable_object, other_factor_object)]

                            # Multiply the product of negative belief messages from friendly factors by the negative belief message of this edge.
                            vs_float *= (1 - belief_messages_current_float_1d_array[belief_message_index_int])

                    # Iterate each opposite factor:
                    for other_factor_object in variable_object.negative_literal_factors_object_set:

                        # Get the index of the edge.
                        belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(variable_object, other_factor_object)]

                        # Multiply the product of negative belief messages from opposite factors by the negative belief message of this edge.
                        vu_float *= (1 - belief_messages_current_float_1d_array[belief_message_index_int])

                    # Update two sub parts.
                    entropy_first_sub_part_1_float *= (vs_float + vu_float)
                    entropy_first_sub_part_2_float *= vu_float

                # If the current factor has a negative literal of the current variable:
                elif factor_object in variable_object.negative_literal_factors_object_set:

                    # Iterate each opposite factor:
                    for other_factor_object in variable_object.positive_literal_factors_object_set:

                        # Get the index of the edge.
                        belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(variable_object, other_factor_object)]

                        # Multiply the product of negative belief messages from opposite factors by the negative belief message of this edge.
                        vu_float *= (1 - belief_messages_current_float_1d_array[belief_message_index_int])

                    # Iterate each friendly factor:
                    for other_factor_object in variable_object.negative_literal_factors_object_set:

                        # Only if this is not the current factor:
                        if factor_object != other_factor_object:

                            # Get the index of the edge.
                            belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(variable_object, other_factor_object)]

                            # Multiply the product of negative belief messages from friendly factors by the negative belief message of this edge.
                            vs_float *= (1 - belief_messages_current_float_1d_array[belief_message_index_int])

                    # Update two sub parts.
                    entropy_first_sub_part_1_float *= (vs_float + vu_float)
                    entropy_first_sub_part_2_float *= vu_float

            # Add the sum as the first part.
            entropy_first_part_float += math.log((entropy_first_sub_part_1_float - entropy_first_sub_part_2_float))

        # Initialize a float to denote the second part of the entropy.
        entropy_second_part_float = 0.0

        # Iterate each variable in the factor graph:
        for variable_id_str in self.variables_id_str_and_variables_object_dict:

            # Get the current variable object.
            variable_object = self.variables_id_str_and_variables_object_dict[variable_id_str]

            # Get its degree.
            degree_int = len(variable_object.positive_literal_factors_object_set) + len(variable_object.negative_literal_factors_object_set)

            # Update the entropy using the information of the current variable.
            entropy_second_part_float += (1 - degree_int) * math.log(variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str][0] + variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str][1])

        # Return final belief messages and entropy.
        return variables_id_str_and_final_belief_messages_float_1d_list_dict, entropy_first_part_float + entropy_second_part_float

    def propagate_belief(self, precision_float: float = 0.0001, number_of_iterations_int: int = 1000) -> (dict[int: list[float]], float):
        """
            Propagate messages in the factor graph.

            Arguments:
                precision_float (float).
                    Default is 0.0001.
                    The float denoting the required precision before the iteration ends.
                number_of_iterations_int (int).
                    Default is 1000.
                    The integer denoting the maximum number of iterations.

            Returns:
                (dict[str: list[float]]).
                    The dictionary containing key-value pairs about Boolean variables and their corresponding marginal probabilities.
                    Each key is a string denoting a Boolean variable.
                    Each value is a list with 3 float numbers. The last one is its marginal probability.
                (float).
                    The float denoting the entropy.
        """

        # Create a list to store belief messages from factors to variables. Initialize all belief messages randomly.
        factors_to_variables_belief_messages_float_1d_array = np.random.rand(len(self.variables_object_to_factors_object_edges_tuple_1d_list))

        # For each iteration:
        for _ in range(number_of_iterations_int):

            # Create a 1-dimensional array to store all indices of edges in the factor graph.
            indices_of_edges_1d_array = np.arange(len(self.variables_object_to_factors_object_edges_tuple_1d_list))

            # Shuffle indices of edges in the factor graph.
            np.random.shuffle(indices_of_edges_1d_array)

            # Create a list to store new belief messages from factors to variables. Initialize all belief messages randomly.
            new_factors_to_variables_belief_messages_float_1d_array = np.random.rand(len(self.variables_object_to_factors_object_edges_tuple_1d_list))

            # Iterate each index of edges in the factor graph:
            for edge_index_int in indices_of_edges_1d_array:

                # Get the variable and the factor from the current edge.
                current_variable_object, current_factor_object = self.variables_object_to_factors_object_edges_tuple_1d_list[edge_index_int]

                # Create a float to store the new belief message from the current factor to the current variable of this edge. Initialize it as 1.0.
                current_factor_to_current_variable_new_belief_message_float = 1.0

                # Iterate each variable with the positive literal in the current factor:
                for other_variable_object in current_factor_object.positive_literal_variables_id_str_and_variables_object_dict.values():

                    # Only if this is not the current variable:
                    if other_variable_object != current_variable_object:

                        # Create a float to store the product of negative belief messages from friendly factors. Initialize it as 1.0.
                        p_u_float = 1.0

                        # Create a float to store the product of negative belief messages from opposite factors. Initialize it as 1.0.
                        p_s_float = 1.0

                        # Iterate each factor with this variable which has the positive literal:
                        for other_factor_object in other_variable_object.positive_literal_factors_object_set:

                            # Because this variable has the positive literal in the current factor, only if this factor is not the current factor:
                            if other_factor_object != current_factor_object:

                                # With this variable and this clause, get the index of this edge.
                                belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(other_variable_object, other_factor_object)]

                                # Multiply the product of negative belief messages from friendly factors by the negative belief message of this edge.
                                p_u_float *= (1 - factors_to_variables_belief_messages_float_1d_array[belief_message_index_int])

                        # Iterate each factor with this variable which has the negative literal:
                        for other_factor_object in other_variable_object.negative_literal_factors_object_set:

                            # With this variable and this clause, get the index of this edge.
                            belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(other_variable_object, other_factor_object)]

                            # Multiply the product of negative belief messages from opposite factors by the negative belief message of this edge.
                            p_s_float *= (1 - factors_to_variables_belief_messages_float_1d_array[belief_message_index_int])

                        # Multiply the new belief message from the current factor to the current variable of this edge by the fraction.
                        current_factor_to_current_variable_new_belief_message_float *= p_u_float / (p_u_float + p_s_float)

                # Iterate each variable with the negative literal in the current factor:
                for other_variable_object in current_factor_object.negative_literal_variables_id_str_and_variables_object_dict.values():

                    # Only if this is not the current variable:
                    if other_variable_object != current_variable_object:

                        # Create a float to store the product of negative belief messages from friendly factors. Initialize it as 1.0.
                        p_u_float = 1

                        # Create a float to store the product of negative belief messages from opposite factors. Initialize it as 1.0.
                        p_s_float = 1

                        # Iterate each factor with this variable which has the positive literal:
                        for other_factor_object in other_variable_object.positive_literal_factors_object_set:

                            # With this variable and this clause, get the index of this edge.
                            belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(other_variable_object, other_factor_object)]

                            # Multiply the product of negative belief messages from opposite factors by the negative belief message of this edge.
                            p_s_float *= (1 - factors_to_variables_belief_messages_float_1d_array[belief_message_index_int])

                        # Iterate each factor with this variable which has the negative literal:
                        for other_factor_object in other_variable_object.negative_literal_factors_object_set:

                            # Because this variable is negative in the current factor, only if this factor is not the current factor:
                            if other_factor_object != current_factor_object:

                                # With this variable and this factor, get the index of this edge.
                                belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(other_variable_object, other_factor_object)]

                                # Multiply the product of negative belief messages from friendly factors by the negative belief message of this edge.
                                p_u_float *= (1 - factors_to_variables_belief_messages_float_1d_array[belief_message_index_int])

                        # Multiply the new belief message from the current factor to the current variable of this edge by the fraction.
                        current_factor_to_current_variable_new_belief_message_float *= p_u_float / (p_u_float + p_s_float)

                # Update the new belief message from the factor to the variable of the current edge as the result.
                new_factors_to_variables_belief_messages_float_1d_array[edge_index_int] = current_factor_to_current_variable_new_belief_message_float

            # Create a Boolean variable to check if the result is converged or not.
            is_converged_bool = True

            # Iterate each index of edges in the factor graph:
            for edge_index_int in range(len(factors_to_variables_belief_messages_float_1d_array)):

                # If the change of the belief message of the current edge exceeds the precision:
                if abs(factors_to_variables_belief_messages_float_1d_array[edge_index_int] - new_factors_to_variables_belief_messages_float_1d_array[edge_index_int]) > precision_float:

                    # The result is not converged. Set the Boolean variable to False.
                    is_converged_bool = False

                    # Break the loop.
                    break

            # Update belief messages from factors to variables as the new one.
            factors_to_variables_belief_messages_float_1d_array = new_factors_to_variables_belief_messages_float_1d_array

            # If the result is converged:
            if is_converged_bool:

                # Break the loop because there is no need to iterate.
                break

        # Create a dictionary to store the final belief messages of all variables in the factor graph.
        variables_id_str_and_final_belief_messages_float_1d_list_dict = {}

        # Iterate each variable in the factor graph:
        for variable_id_str in self.variables_id_str_and_variables_object_dict:

            # Initialize the final belief messages of the current variable.
            # [0] is the product of belief messages from factors which has positive literals of the current Boolean variable. Initialize it as 1.
            # [1] is the product of belief messages from factors which has negative literals of the current Boolean variable. Initialize it as 1.
            # [2] is the final belief message of the current variable. Initialize it as 0.
            variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str] = [1.0, 1.0, 0.0]

        # Iterate each index of edges in the factor graph:
        for belief_message_index_int in range(len(factors_to_variables_belief_messages_float_1d_array)):

            # Get the variable and the factor from the current edge.
            current_variable_object, current_factor_object = self.variables_object_to_factors_object_edges_tuple_1d_list[belief_message_index_int]

            # If the current variable has positive literal in the current factor:
            if current_factor_object in current_variable_object.positive_literal_factors_object_set:

                # Multiply the product of belief messages from friendly factors by the belief message of this edge.
                variables_id_str_and_final_belief_messages_float_1d_list_dict[current_variable_object.variable_id_str][0] *= (1 - factors_to_variables_belief_messages_float_1d_array[belief_message_index_int])

            # If the current variable has negative literal in the current factor:
            else:

                # Multiply the product of belief messages from opposite factors by the belief message of this edge.
                variables_id_str_and_final_belief_messages_float_1d_list_dict[current_variable_object.variable_id_str][1] *= (1 - factors_to_variables_belief_messages_float_1d_array[belief_message_index_int])

        # Iterate each variable in the factor graph:
        for variable_id_str in self.variables_id_str_and_variables_object_dict:

            # Compute and store the final belief message of the current variable.
            variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str][2] = variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str][1] / (variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str][0] + variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str][1])

        # Initialize a float to denote the first part of the entropy.
        entropy_first_part_float = 0.0

        # Iterate each factor:
        for factor_object in self.factor_object_set:

            # Initialize a float to denote the first product.
            product_1_float = 1.0

            # Initialize a float to denote the second product.
            product_2_float = 1.0

            # Iterate each variable with the positive literal in the current factor:
            for variable_object in factor_object.positive_literal_variables_id_str_and_variables_object_dict.values():

                # Create a float to store the product of negative belief messages from friendly factors. Initialize it as 1.0.
                p_u_float = 1.0

                # Create a float to store the product of positive belief messages from opposite factors. Initialize it as 1.0.
                p_s_float = 1.0

                # Iterate each factor with this variable which has the positive literal:
                for other_factor_object in variable_object.positive_literal_factors_object_set:

                    # Because this variable has the positive literal in the current factor, only if this factor is not the current factor:
                    if other_factor_object != factor_object:

                        # With this variable and this clause, get the index of this edge.
                        belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(variable_object, other_factor_object)]

                        # Multiply the product of negative belief messages from friendly factors by the negative belief message of this edge.
                        p_u_float *= (1 - factors_to_variables_belief_messages_float_1d_array[belief_message_index_int])

                # Iterate each factor with this variable which has the negative literal:
                for other_factor_object in variable_object.negative_literal_factors_object_set:

                    # With this variable and this clause, get the index of this edge.
                    belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(variable_object, other_factor_object)]

                    # Multiply the product of negative belief messages from opposite factors by the negative belief message of this edge.
                    p_s_float *= (1 - factors_to_variables_belief_messages_float_1d_array[belief_message_index_int])

                # Update the first product.
                product_1_float *= p_u_float / (p_u_float + p_s_float)

                # Update the second product.
                product_2_float *= p_u_float + p_s_float

            # Iterate each variable with the negative literal in the current factor:
            for variable_object in factor_object.negative_literal_variables_id_str_and_variables_object_dict.values():

                # Create a float to store the product of negative belief messages from friendly factors. Initialize it as 1.0.
                p_u_float = 1

                # Create a float to store the product of negative belief messages from opposite factors. Initialize it as 1.0.
                p_s_float = 1

                # Iterate each factor with this variable which has the positive literal:
                for other_factor_object in variable_object.positive_literal_factors_object_set:

                    # With this variable and this clause, get the index of this edge.
                    belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(variable_object, other_factor_object)]

                    # Multiply the product of negative belief messages from opposite factors by the negative belief message of this edge.
                    p_s_float *= (1 - factors_to_variables_belief_messages_float_1d_array[belief_message_index_int])

                # Iterate each factor with this variable which has the negative literal:
                for other_factor_object in variable_object.negative_literal_factors_object_set:

                    # Because this variable is negative in the current factor, only if this factor is not the current factor:
                    if other_factor_object != factor_object:

                        # With this variable and this factor, get the index of this edge.
                        belief_message_index_int = self.variables_object_to_factors_object_edges_tuple_and_indices_int_dict[(variable_object, other_factor_object)]

                        # Multiply the product of negative belief messages from friendly factors by the negative belief message of this edge.
                        p_u_float *= (1 - factors_to_variables_belief_messages_float_1d_array[belief_message_index_int])

                # Update the first product.
                product_1_float *= (p_u_float / (p_u_float + p_s_float))

                # Update the second product.
                product_2_float *= (p_u_float + p_s_float)

            # Add the current factor to the first part of the entropy.
            entropy_first_part_float += math.log((1 - product_1_float) * product_2_float)

        # Initialize a float to denote the second part of the entropy.
        entropy_second_part_float = 0.0

        # Iterate each variable in the factor graph:
        for variable_id_str in self.variables_id_str_and_variables_object_dict:

            # Get the current variable object.
            variable_object = self.variables_id_str_and_variables_object_dict[variable_id_str]

            # Get its degree.
            degree_int = len(variable_object.positive_literal_factors_object_set) + len(variable_object.negative_literal_factors_object_set)

            # Update the entropy using the information of the current variable.
            entropy_second_part_float += (1 - degree_int) * math.log(variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str][0] + variables_id_str_and_final_belief_messages_float_1d_list_dict[variable_id_str][1])

        # Return final belief messages and entropy.
        return variables_id_str_and_final_belief_messages_float_1d_list_dict, entropy_first_part_float + entropy_second_part_float
