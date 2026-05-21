# Import to do annotations.
from src.transitions.states_transitions import StatesTransitions


class StrongInhibitionApproximateInference:
    """
        This class denotes a type of inference to an input which are transitions.
        The inference uses the strategy Divide and Conquer to process each Boolean variable respectively.
        The inference checks if the input transitions of each Boolean variable are compatible with the dynamics of Strong Inhibition.
        If the input transitions of each Boolean variable are compatible with the dynamics of Strong Inhibition, then convert transitions as a Boolean equation.

        Attributes:
            states_transitions_object (StatesTransitions).
                The instance of StatesTransitions containing the information of transitions in this inference.
            is_self_green_allowed_bool (bool).
                The Boolean variable verifying that if self cycles of green edges can exist or not.
            is_self_red_allowed_bool (bool).
                The Boolean variable verifying that if self cycles of red edges can exist or not.
            do_green_and_red_conflict_bool (bool).
                The Boolean variable verifying that if at most one color of edges can exist from one Boolean variable to another Boolean variable.
            active_boolean_variables_in_states_before_2d_list (list[list[str]]).
                The 2-dimensional list containing active Boolean variables in states before during each transition.
            inactive_boolean_variables_in_states_before_2d_list (list[list[str]]).
                The 2-dimensional list containing inactive Boolean variables in states before during each transition.
            boolean_variables_str_and_indices_of_transitions_with_active_in_states_after_int_list_dict (dict[str, list[int]]).
                The dictionary containing key-value pairs about Boolean variables and the list with indices of transitions when the key Boolean variable is active in the states after.
            boolean_variables_str_and_indices_of_transitions_with_inactive_in_states_after_int_list_dict (dict[str, list[int]]).
                The dictionary containing key-value pairs about Boolean variables and the list with indices of transitions when the key Boolean variable is inactive in the states after.
    """

    def __init__(self, states_transitions_object: StatesTransitions, is_self_green_allowed_bool: bool = False, is_self_red_allowed_bool: bool = True, do_green_and_red_conflict_bool: bool = True):
        """
            Construct objects by initializing attributes.

            Arguments:
                states_transitions_object (StatesTransitions).
                    The instance of StatesTransitions containing the information of transitions in this inference.
                is_self_green_allowed_bool (bool).
                    Default value is False.
                    The Boolean variable verifying that if self cycles of green edges can exist or not.
                is_self_red_allowed_bool (bool).
                    Default value is True.
                    The Boolean variable verifying that if self cycles of red edges can exist or not.
                do_green_and_red_conflict_bool (bool).
                    Default value is True.
                    The Boolean variable verifying that if at most one color of edges can exist from one Boolean variable to another Boolean variable.
        """

        # Initialize attributes by assigning targets to them.
        self.states_transitions_object = states_transitions_object
        self.is_self_green_allowed_bool = is_self_green_allowed_bool
        self.is_self_red_allowed_bool = is_self_red_allowed_bool
        self.do_green_and_red_conflict_bool = do_green_and_red_conflict_bool

        # Initialize the attribute as a list with the number of empty lists as the number of transitions.
        self.active_boolean_variables_in_states_before_2d_list = [[] for _ in self.states_transitions_object.transitions_dict_1d_tuple_1d_list]

        # Initialize the attribute as a list with the number of empty lists as the number of transitions.
        self.inactive_boolean_variables_in_states_before_2d_list = [[] for _ in self.states_transitions_object.transitions_dict_1d_tuple_1d_list]

        # Iterate each Boolean variable and add them as keys with empty lists as values:
        self.boolean_variables_str_and_indices_of_transitions_with_active_in_states_after_int_list_dict = {boolean_variable_str: [] for boolean_variable_str in self.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}

        # Iterate each Boolean variable and add them as keys with empty lists as values:
        self.boolean_variables_str_and_indices_of_transitions_with_inactive_in_states_after_int_list_dict = {boolean_variable_str: [] for boolean_variable_str in self.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}

        # Iterate each index of transitions:
        for transition_index_int in range(len(self.states_transitions_object.transitions_dict_1d_tuple_1d_list)):

            # Get the states before during the current transition.
            boolean_variables_str_and_states_before_bool_dict = self.states_transitions_object.transitions_dict_1d_tuple_1d_list[transition_index_int][0]

            # Iterate each Boolean variable:
            for boolean_variable_str in boolean_variables_str_and_states_before_bool_dict:

                # If the current Boolean variable is active in the current states before:
                if boolean_variables_str_and_states_before_bool_dict[boolean_variable_str]:

                    # Append the current Boolean variable into the list with active Boolean variables.
                    self.active_boolean_variables_in_states_before_2d_list[transition_index_int].append(boolean_variable_str)

                # If the current Boolean variable is inactive in the current states before:
                else:

                    # Append the current Boolean variable into the list with inactive Boolean variables.
                    self.inactive_boolean_variables_in_states_before_2d_list[transition_index_int].append(boolean_variable_str)

            # Get the states after during the current transition.
            boolean_variables_str_and_states_after_bool_dict = self.states_transitions_object.transitions_dict_1d_tuple_1d_list[transition_index_int][1]

            # Iterate each Boolean variable:
            for boolean_variable_str in boolean_variables_str_and_states_after_bool_dict:

                # If the current Boolean variable is active in the current states after:
                if boolean_variables_str_and_states_after_bool_dict[boolean_variable_str]:

                    # In the attribute, append the index of the current transition into the list of the current Boolean variable.
                    self.boolean_variables_str_and_indices_of_transitions_with_active_in_states_after_int_list_dict[boolean_variable_str].append(transition_index_int)

                # If the current Boolean variable is inactive in the current states after:
                else:

                    # In the attribute, append the index of the current transition into the list of the current Boolean variable.
                    self.boolean_variables_str_and_indices_of_transitions_with_inactive_in_states_after_int_list_dict[boolean_variable_str].append(transition_index_int)

    def generate_cnf_formula_for_one_boolean_variable(self, target_boolean_variable_str: str) -> list[list[str]]:
        """
            Generate the CNF formula formed by clauses.

            Arguments:
                target_boolean_variable_str (str).
                    The string denoting the Boolean variable as the target.

            Returns:
                (list[list[str]]).
                    A 2-dimensional list, and its each member is a 1-dimensional list about a clause.
                    The clause consists of some variables connected with spaces.
                    For each variable:
                        For the first prefix symbol,
                            If the first prefix symbol is +, then its corresponding edge can exist;
                            If the first prefix symbol is -, then its corresponding edge cannot exist;
                        For the second prefix symbol,
                            If the second prefix symbol is G_, then its corresponding edge is a green edge;
                            If the second prefix symbol is R_, then its corresponding edge is a red edge.
        """

        # Initialize an empty list to store all CNF clauses. Each clause is represented as a list of variables which are string.
        variables_str_1d_list_cnf_clauses_2d_list = []

        # If the argument explicitly requires that at most one color of edges can exist from one Boolean variable to another Boolean variable:
        if self.do_green_and_red_conflict_bool:

            # Iterate each Boolean variable:
            for boolean_variable_str in self.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict:

                # Append the current clause as at least one color edge should be nonexistent into the list.
                variables_str_1d_list_cnf_clauses_2d_list.append([f"-G_{boolean_variable_str}", f"-R_{boolean_variable_str}"])

        # Iterate each index of transitions:
        for transition_index_int in range(len(self.states_transitions_object.transitions_dict_1d_tuple_1d_list)):

            # Get the list containing all active Boolean variables in the states before when the target Boolean variable is inactive in states after during the current transition.
            active_boolean_variables_in_states_before_str_list = self.active_boolean_variables_in_states_before_2d_list[transition_index_int]

            # If the target Boolean variable is active in states after, then both of two cases must be true:
            # 1. This case generates only one variable:
            #       Any other active Boolean variables before cannot inhibit this Boolean variable.
            # 2. This case may generate more than one variable.
            #       It consists of three conditions, and at least one of them must be satisfied:
            #       (1) Some other active Boolean variable before may activate this Boolean variable.
            #       (2) If the target Boolean variable is inactive before, then it must have a green edge to itself.
            #       (3) If the target Boolean variable is active before, then it cannot have a red edge to itself.
            if self.states_transitions_object.transitions_dict_1d_tuple_1d_list[transition_index_int][1][target_boolean_variable_str]:

                # Initialize a variable to store the clause representing the green edges.
                # In this clause, variables are connected with OR operation.
                # This clause must be satisfied in the formula.
                green_clause_str = ""

                # Initialize a variable to store the clause representing the red edges.
                # In this clause, variables are connected with AND operation.
                # This clause must be satisfied in the formula.
                red_clause_str = ""

                # Blocks of Case 1 and Case 2.(1) begins.
                # Iterate each active Boolean variable in states before during the current transition when the target Boolean variable is inactive after:
                for active_boolean_variable_str in active_boolean_variables_in_states_before_str_list:

                    # If the active Boolean variable before is not the target Boolean variable, then it cannot have a red edge and can have a green edge to the target Boolean variable.
                    if active_boolean_variable_str != target_boolean_variable_str:

                        # Add this variable into the green clause.
                        green_clause_str += f"+G_{active_boolean_variable_str} "

                        # Add this variable into the red clause.
                        red_clause_str += f"-R_{active_boolean_variable_str} "

                # Block of Case 2.(2) and 2.(3) begins.
                # If the self green edge can exist and the target Boolean variable is inactive before, then it may have a green edge to itself in this sub-clause.
                if self.is_self_green_allowed_bool and not self.states_transitions_object.transitions_dict_1d_tuple_1d_list[transition_index_int][0][target_boolean_variable_str]:

                    # Add this variable into the green clause.
                    green_clause_str += f"+G_{target_boolean_variable_str} "

                # If the self red edge can exist and the target Boolean variable is active before, then it may not have a red edge to itself in this sub-clause:
                if self.is_self_red_allowed_bool and self.states_transitions_object.transitions_dict_1d_tuple_1d_list[transition_index_int][0][target_boolean_variable_str]:

                    # Add this variable into the green clause.
                    green_clause_str += f"-R_{target_boolean_variable_str} "

                # If the green clause is not empty:
                if green_clause_str != "":

                    # Split the current green clause to green variables through spaces.
                    green_variables_str_1d_list = green_clause_str.strip(" ").split(" ")

                    # Append the green clause into the CNF formula directly.
                    variables_str_1d_list_cnf_clauses_2d_list.append(green_variables_str_1d_list)

                # If the red clause is not empty:
                if red_clause_str != "":

                    # Split the current red clause to red variables through spaces.
                    red_variables_str_1d_list = red_clause_str.strip(" ").split(" ")

                    # Separate each red variable because each of them must be satisfied in CNF format.
                    # Iterate each red variable:
                    for red_variable_str in red_variables_str_1d_list:

                        # Append each red variable into the CNF formula.
                        variables_str_1d_list_cnf_clauses_2d_list.append([red_variable_str])

            # If the target Boolean variable is inactive in states after, then at least one of two cases must be true:
            # 3. This case may generate more than one variable:
            #     Any other active Boolean variables in states before can inhibit the target Boolean variable.
            # 4. This case generates only one variable.
            #     It consists of three conditions, and all of them must be satisfied:
            #     (1) All other active Boolean variables before cannot activate this Boolean variable.
            #     (2) If self green edges can exist, and this Boolean variable is inactive before, then it cannot have a green edge to itself.
            #     (3) If self red edges can exist, and this Boolean variable is active before, then it must have a red edge to itself.
            else:

                # Initialize a variable to store the clause representing the green edges.
                # In this clause, variables are connected with AND operation.
                green_clause_str = ""

                # Initialize a variable to store the clause representing the red edges.
                # In this clause, variables are connected with OR operation.
                red_clause_str = ""

                # For these two clauses, only one of them must be satisfied.

                # Block of Case 3 and Case 4.(1) begins.
                # Iterate each active Boolean variable in states before during the current transition when the target Boolean variable is inactive after:
                for active_boolean_variable_str in active_boolean_variables_in_states_before_str_list:

                    # If the active Boolean variable before is not the target Boolean variable, then it may have a red edge to the target Boolean variable.
                    if active_boolean_variable_str != target_boolean_variable_str:

                        # Add this variable into the green clause.
                        green_clause_str += f"-G_{active_boolean_variable_str} "

                        # Add this variable into the red clause.
                        red_clause_str += f"+R_{active_boolean_variable_str} "

                # Block of Case 4.(2) and Case 4.(3) begins.
                # If the self green edges can exist and the target Boolean variable is inactive before, then it cannot have a green edge to itself.
                if self.is_self_green_allowed_bool and not self.states_transitions_object.transitions_dict_1d_tuple_1d_list[transition_index_int][0][target_boolean_variable_str]:

                    # Add this variable into the green clause.
                    green_clause_str += f"-G_{target_boolean_variable_str} "

                # If the self red edges can exist and the target Boolean variable is active before, then it must have a red edge to itself.
                if self.is_self_red_allowed_bool and self.states_transitions_object.transitions_dict_1d_tuple_1d_list[transition_index_int][0][target_boolean_variable_str]:

                    # Add this variable into the green clause.
                    green_clause_str += f"+R_{target_boolean_variable_str} "

                # If the green clause is empty:
                if green_clause_str == "":

                    # If the red clause is not empty:
                    if red_clause_str != "":

                        # Split the current red clause to red variables through spaces.
                        red_variables_str_1d_list = red_clause_str.strip(" ").split(" ")

                        # Append the red clause into the CNF formula.
                        variables_str_1d_list_cnf_clauses_2d_list.append(red_variables_str_1d_list)

                # If the green clause is not empty:
                else:

                    # If the red clause is empty:
                    if red_clause_str == "":

                        # Split the current green clause to green variables through spaces.
                        green_variables_str_1d_list = green_clause_str.strip(" ").split(" ")

                        # Iterate each green variable:
                        for green_variable_str in green_variables_str_1d_list:

                            # Append each green variable into the CNF formula.
                            variables_str_1d_list_cnf_clauses_2d_list.append([green_variable_str])

                    # If the red clause is not empty:
                    else:

                        # Split the current green clause to green variables through spaces.
                        green_variables_str_1d_list = green_clause_str.strip(" ").split(" ")

                        # Split the current red clause to red variables through spaces.
                        red_variables_str_1d_list = red_clause_str.strip(" ").split(" ")

                        # Iterate each green variable:
                        for green_variable_str in green_variables_str_1d_list:

                            # Append each green variable with the red clause into the CNF formula.
                            variables_str_1d_list_cnf_clauses_2d_list.append([green_variable_str] + red_variables_str_1d_list)

        # Return the formula.
        return variables_str_1d_list_cnf_clauses_2d_list
