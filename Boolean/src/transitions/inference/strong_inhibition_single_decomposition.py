# Import to initialize its objects.
from src.boolean.boolean_variables_sets import BooleanVariablesSets

# Import to store its objects.
from src.transitions.inference.strong_inhibition_approximate_inference import StrongInhibitionApproximateInference

# Import itertools to enumerate.
import itertools


class StrongInhibitionSingleDecomposition:
    """
        This class decomposes the solution space of transitions for one Boolean variable based on strong inhibition dynamics.

        Attributes:
            inference_object (StrongInhibitionApproximateInference).
                The instance of StrongInhibitionApproximateInference containing the information of transitions.
            target_boolean_variable_str (str).
                The string denoting the name of the Boolean variable as the target.
            has_green_self_bool (bool).
                The Boolean variable to denote that if the argument Boolean variable has a green self loop or not.
            has_red_self_bool (bool).
                The Boolean variable to denote that if the argument Boolean variable has a red self loop or not.
            boolean_variables_str_and_if_it_is_a_green_source_bool_dict (dict[str: bool]).
                The dictionary containing key-value pairs about Boolean variables and if they have green edges to the argument Boolean variable or not.
            boolean_variables_str_and_if_it_is_a_red_source_bool_dict (dict[str: bool]).
                The dictionary containing key-value pairs about Boolean variables and if they have red edges to the argument Boolean variable or not.
            remaining_boolean_variables_str_set (set[int]).
                The set containing all Boolean variables except the argument Boolean variable at the beginning. Boolean variables may move out during the decomposition.
            invalid_green_and_valid_red_sources_str_set (set[int]).
                The set containing Boolean variables which have invalid green edges and valid red edges to the argument Boolean variable.
            valid_green_and_no_red_sources_str_set (set[int]).
                The set containing Boolean variables which have valid green edges and no red edges to the argument Boolean variable.
            no_green_and_valid_red_sources_str_set (set[int]).
                The set containing Boolean variables which have no green edges and valid red edges to the argument Boolean variable.
            determined_green_sources_str_set (set[int]).
                The set containing Boolean variables which must have green edges to the argument Boolean variable.
            determined_red_sources_str_set (set[int]).
                The set containing Boolean variables which must have red edges to the argument Boolean variable.
            no_green_and_no_red_sources_str_set (set[int]).
                The set containing Boolean variables which cannot have green or red edges to the argument Boolean variable.
            necessary_green_sources_str_sets_object (BooleanVariablesSets)
                The object of BooleanVariablesSets, which is the group of sets containing Boolean variables which have necessary green edges to the argument Boolean variable.
            necessary_red_sources_str_sets_object (BooleanVariablesSets)
                The object of BooleanVariablesSets, which is the group of sets containing Boolean variables which have necessary red edges to the argument Boolean variable.
            conjugated_sources_str_sets_object (BooleanVariablesSets)
                The object of BooleanVariablesSets, which is the group of sets containing Boolean variables which have conjugated edges to the argument Boolean variable.
    """

    def __init__(self, inference_object: StrongInhibitionApproximateInference, target_boolean_variable_str: str, has_green_self_bool: bool, has_red_self_bool: bool):
        """
            Construct objects by initializing attributes.

            Arguments:
                inference_object (StrongInhibitionApproximateInference).
                    The instance of StrongInhibitionApproximateInference containing the information of transitions.
                target_boolean_variable_str (str).
                    The string denoting the name of the Boolean variable as the target.
                has_green_self_bool (bool).
                    The Boolean variable to denote that if the argument Boolean variable has a green self loop or not.
                has_red_self_bool (bool).
                    The Boolean variable to denote that if the argument Boolean variable has a red self loop or not.
       """

        # Initialize attributes by assigning argument to them.
        self.inference_object = inference_object
        self.target_boolean_variable_str = target_boolean_variable_str
        self.has_green_self_bool = False
        self.has_red_self_bool = has_red_self_bool

        # Initialize the attribute list of green edge pointing to the target Boolean variable.
        self.boolean_variables_str_and_if_it_is_a_green_source_bool_dict = {boolean_variable_str: -1 for boolean_variable_str in self.inference_object.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}

        # If the target Boolean variable has a green self loop edge:
        if self.has_green_self_bool:

            # The target Boolean variable has the self cycle of the green edge.
            self.boolean_variables_str_and_if_it_is_a_green_source_bool_dict[self.target_boolean_variable_str] = 1

        # If the target Boolean variable does not have a green self loop edge:
        else:

            # The target Boolean variable does not have the self cycle of the green edge.
            self.boolean_variables_str_and_if_it_is_a_green_source_bool_dict[self.target_boolean_variable_str] = 0

        # Initialize the attribute list of red edge pointing to the target Boolean variable.
        self.boolean_variables_str_and_if_it_is_a_red_source_bool_dict = {boolean_variable_str: -1 for boolean_variable_str in self.inference_object.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}

        # If the target Boolean variable has a red self loop edge:
        if self.has_red_self_bool:

            # The target Boolean variable has the self cycle of the red edge.
            self.boolean_variables_str_and_if_it_is_a_red_source_bool_dict[self.target_boolean_variable_str] = 1

        # If the target Boolean variable does not have a red self loop edge:
        else:

            # The target Boolean variable has the self cycle of the red edge.
            self.boolean_variables_str_and_if_it_is_a_red_source_bool_dict[self.target_boolean_variable_str] = 0

        # Initialize the set containing all Boolean variables except the argument Boolean variable.
        self.remaining_boolean_variables_str_set = set([boolean_variable_str for boolean_variable_str in self.inference_object.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict if boolean_variable_str != self.target_boolean_variable_str])

        # Initialize the set containing Boolean variables which have free green edges and free red edges to the target Boolean variable.
        self.free_green_and_free_red_sources_str_set = set()

        # Call the method to update the attribute set of Boolean variables which have free green edges and free red edges to the target Boolean variable.
        self.get_free_green_and_free_red_sources_str_set()

        # Initialize the set containing Boolean variables which have invalid green edges and valid red edges to the target Boolean variable.
        self.invalid_green_and_valid_red_sources_str_set = set()

        # Initialize the set containing Boolean variables which have valid green edges and no red edges to the target Boolean variable.
        self.valid_green_and_no_red_sources_str_set = set()

        # Initialize the set containing Boolean variables which have no green edges and valid red edges to the target Boolean variable.
        self.no_green_and_valid_red_sources_str_set = set()

        # Initialize the set containing Boolean variables which must have green edges to the target Boolean variable.
        self.determined_green_sources_str_set = set()

        # Initialize the set containing Boolean variables which must have red edges to the target Boolean variable.
        self.determined_red_sources_str_set = set()

        # Initialize the set containing Boolean variables which cannot have green or red edges to the target Boolean variable.
        self.no_green_and_no_red_sources_str_set = set()

        # Initialize the group of sets containing Boolean variables which have necessary green edges to the argument Boolean variable as None.
        self.necessary_green_sources_str_sets_object = None

        # Initialize the group of sets containing Boolean variables which have necessary red edges to the argument Boolean variable as None.
        self.necessary_red_sources_str_sets_object = None

        # Initialize the group of sets containing Boolean variables which have conjugated edges to the argument Boolean variable as None.
        self.conjugated_sources_str_sets_object = None

    def check_if_transitions_can_fit_strong_inhibition(self) -> bool:
        """
            Check if transitions for the argument Boolean variable can fit the dynamics of Strong Inhibition or not.

            Returns:
                (bool).
                    The Boolean variable to denote if transitions for the argument Boolean variable can fit the dynamics of Strong Inhibition or not.
        """

        # Initialize an empty 1-dimensional list to store Boolean variables which provide green edges.
        green_sources_boolean_variables_str_1d_list = []

        # Initialize an empty 1-dimensional list to store Boolean variables which provide red edges.
        red_sources_boolean_variables_str_1d_list = []

        # Call the method to determine some nonexistent red edge. No need to decompose the solution space.
        self.check_nonexistent_red_edge_and_divide_boolean_variables()

        # Iterate each Boolean variable:
        for boolean_variable_str in self.inference_object.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict:

            # If this red edge has not been determined yet, and it is not the target Boolean variable:
            if self.boolean_variables_str_and_if_it_is_a_red_source_bool_dict[boolean_variable_str] == -1 and boolean_variable_str != self.target_boolean_variable_str:

                # Assign the red edge to be existent.
                red_sources_boolean_variables_str_1d_list.append(boolean_variable_str)

        # If the argument explicitly requires to have a self cycle of red edge:
        if self.has_red_self_bool:

            # Set a self red loop edge to itself.
            red_sources_boolean_variables_str_1d_list.append(self.target_boolean_variable_str)

        # Call the method to determine some nonexistent green edges.
        self.check_nonexistent_green_edge_and_divide_boolean_variables()

        # Iterate each Boolean variable:
        for boolean_variable_str in self.inference_object.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict:

            # If this green edge has not been determined yet, and the current Boolean variable is not the target Boolean variable, and the current Boolean variable does not have a green edge to the target Boolean variable:
            if self.boolean_variables_str_and_if_it_is_a_green_source_bool_dict[boolean_variable_str] == -1 and boolean_variable_str != self.target_boolean_variable_str and boolean_variable_str not in red_sources_boolean_variables_str_1d_list:

                # Assign the green edge to be existent.
                green_sources_boolean_variables_str_1d_list.append(boolean_variable_str)

        # Iterate each transition:
        for transitions_dict_1d_tuple in self.inference_object.states_transitions_object.transitions_dict_1d_tuple_1d_list:

            # Initialize a Boolean variable to denote if the target Boolean variable will become active at states after or not.
            become_active_bool = False

            # Iterate each Boolean variable at states before:
            for boolean_variable_str in transitions_dict_1d_tuple[0]:

                # If the current Boolean variable is not the target Boolean variable:
                if boolean_variable_str != self.target_boolean_variable_str:

                    # If this Boolean variable is active at states before:
                    if transitions_dict_1d_tuple[0][boolean_variable_str]:

                        # If this Boolean variable has a red edge to the target Boolean variable:
                        if boolean_variable_str in red_sources_boolean_variables_str_1d_list:

                            # If the target Boolean variable is active at states after:
                            if transitions_dict_1d_tuple[1][self.target_boolean_variable_str]:

                                # There is a contradiction. No solution.
                                return False

                            # If the target Boolean variable is inactive at states after:
                            else:

                                # There is no meaning to check other effects.
                                become_active_bool = None

                                # No need to check other Boolean variables.
                                break

                        # If this Boolean variable has a green edge to the target Boolean variable:
                        elif boolean_variable_str in green_sources_boolean_variables_str_1d_list:

                            # Set the target Boolean variable active at states after.
                            become_active_bool = True

            # If it is necessary to check other effects
            if become_active_bool is not None:

                # If the target Boolean variable becomes active at states after.
                if become_active_bool:

                    # If this Boolean variable is inactive at states before:
                    if not transitions_dict_1d_tuple[1][self.target_boolean_variable_str]:

                        # There is a contradiction. No solution.
                        return False

                # If the target Boolean variable receives no green effects:
                else:

                    # If the target Boolean variable is inactive at states before, then the target Boolean variable should be inactive at states after:
                    if not transitions_dict_1d_tuple[0][self.target_boolean_variable_str]:

                        # If the target Boolean variable is active at states after.
                        if transitions_dict_1d_tuple[1][self.target_boolean_variable_str]:

                            # There is a contradiction. No solution.
                            return False

                    # If the target Boolean variable is active at states before:
                    else:

                        # If the target Boolean variable has a red self loop, then the target Boolean variable should be inactive at states after:
                        if self.target_boolean_variable_str in red_sources_boolean_variables_str_1d_list:

                            # If the target Boolean variable is active at states after.
                            if transitions_dict_1d_tuple[1][self.target_boolean_variable_str]:

                                # There is a contradiction. No solution.
                                return False

                        # If the target Boolean variable does not have a red self loop, then the target Boolean variable should be active at states after:
                        else:

                            # If the target Boolean variable is inactive at states after.
                            if not transitions_dict_1d_tuple[1][self.target_boolean_variable_str]:

                                # There is a contradiction. No solution.
                                return False

        # Return True to denote that the fit succeeds.
        return True

    def get_free_green_and_free_red_sources_str_set(self):
        """
            Get the set of Boolean variables which is always inactive.
        """

        # Iterate each Boolean variable:
        for boolean_variable_str in self.inference_object.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict:

            # If the current Boolean variable is not the target Boolean variable:
            if boolean_variable_str != self.target_boolean_variable_str:

                # Initialize a Boolean variable to denote that if it is always inactive or not.
                is_always_inactive_bool = True

                # Iterate each transition:
                for transitions_dict_1d_tuple in self.inference_object.states_transitions_object.transitions_dict_1d_tuple_1d_list:

                    # If the current Boolean variable is active before at this transition:
                    if transitions_dict_1d_tuple[0][boolean_variable_str]:

                        # The current Boolean variable is not always inactive.
                        is_always_inactive_bool = False

                        # No need to check following transitions.
                        break

                # If the current Boolean variable is always inactive:
                if is_always_inactive_bool:

                    # Remove this Boolean variable from the initial set.
                    self.remaining_boolean_variables_str_set.remove(boolean_variable_str)

                    # Add this Boolean variable into the attribute set with Boolean variables which have free green edge and red edge to the argument Boolean variable.
                    self.free_green_and_free_red_sources_str_set.add(boolean_variable_str)

    def check_nonexistent_red_edge_and_divide_boolean_variables(self):
        """
            Determine if some red edge to the target Boolean variable cannot exist and divide Boolean variables.
            Check active Boolean variables before of other Boolean variables and active Boolean variables after of the target Boolean variable.
            If the target Boolean variable is active at the time step after, then any other active Boolean variables before cannot have red edge to it.
        """

        # Iterate each index of transitions with the target Boolean variable is active after:
        for index_of_transition_with_active_in_states_after_int in self.inference_object.boolean_variables_str_and_indices_of_transitions_with_active_in_states_after_int_list_dict[self.target_boolean_variable_str]:

            # Iterate each active Boolean variable before at the current transition with the target Boolean variable active after:
            for active_boolean_variable_before_str in self.inference_object.active_boolean_variables_in_states_before_2d_list[index_of_transition_with_active_in_states_after_int]:

                # If the red edge has not been determined yet and the active Boolean variable before is not itself:
                if self.boolean_variables_str_and_if_it_is_a_red_source_bool_dict[active_boolean_variable_before_str] == -1 and active_boolean_variable_before_str != self.target_boolean_variable_str:

                    # The active Boolean variable before cannot have a red edge to the target Boolean variable.
                    self.boolean_variables_str_and_if_it_is_a_red_source_bool_dict[active_boolean_variable_before_str] = 0

                    # If the active Boolean variable before is in the set of remaining Boolean variables, then it has not been determined yet:
                    if active_boolean_variable_before_str in self.remaining_boolean_variables_str_set:

                        # Remove the active Boolean variable before from the set of remaining Boolean variables.
                        self.remaining_boolean_variables_str_set.remove(active_boolean_variable_before_str)

                        # Add the active Boolean variable before into the set of Boolean variables with restricted green edges and nonexistent red edges.
                        self.valid_green_and_no_red_sources_str_set.add(active_boolean_variable_before_str)

        # Move the remaining Boolean variables into the set containing Boolean variables with invalid green edge and valid red edge.
        self.invalid_green_and_valid_red_sources_str_set.update(self.remaining_boolean_variables_str_set)

    def check_nonexistent_green_edge_and_divide_boolean_variables(self):
        """
            Determine if some green edge to the target Boolean variable cannot exist and divide Boolean variables.
            Check inactive Boolean variables before of other Boolean variables and inactive Boolean variables after of the target Boolean variable.
            If the target Boolean variable is inactive at the time step after, and any other active Boolean variable before cannot have a red edge to it, then other active Boolean variables before cannot have green edge to the target Boolean variable.
        """

        # Iterate each index of transitions with the target Boolean variable is inactive after:
        for transition_index_with_target_inactive_after_int in self.inference_object.boolean_variables_str_and_indices_of_transitions_with_inactive_in_states_after_int_list_dict[self.target_boolean_variable_str]:

            # Initialize a variable to denote if all other Boolean variables before cannot have red edge to the target Boolean variable. Initialize it as True.
            none_red_edge_before_bool = True

            # Iterate each active Boolean variable before at the current transition with the active target Boolean variable before:
            for active_boolean_variable_before_str in self.inference_object.active_boolean_variables_in_states_before_2d_list[transition_index_with_target_inactive_after_int]:

                # If the red edge may exist and the active Boolean variable before is not the target Boolean variable:
                if self.boolean_variables_str_and_if_it_is_a_red_source_bool_dict[active_boolean_variable_before_str] != 0 and active_boolean_variable_before_str != self.target_boolean_variable_str:

                    # Some other active Boolean variables before may have a red edge to the current Boolean variable.
                    none_red_edge_before_bool = False

                    # Skip it.
                    break

            # Only if all other active Boolean variables before cannot have red edge to the argument Boolean variable:
            if none_red_edge_before_bool:

                # Iterate each index of active Boolean variables before at the current transition with the target Boolean variables inactive after:
                for active_boolean_variable_before_str in self.inference_object.active_boolean_variables_in_states_before_2d_list[transition_index_with_target_inactive_after_int]:

                    # If the active Boolean variable before is not the target Boolean variable:
                    if active_boolean_variable_before_str != self.target_boolean_variable_str:

                        # This active Boolean variable cannot have a green edge to the target Boolean variable.
                        self.boolean_variables_str_and_if_it_is_a_green_source_bool_dict[active_boolean_variable_before_str] = 0

                        # If the active Boolean variable before is in the set of valid green edges and no red edges Boolean variables, then it has not been determined yet:
                        if active_boolean_variable_before_str in self.valid_green_and_no_red_sources_str_set:

                            # Remove the active Boolean variable before from the set of valid green edges and no red edges Boolean variables.
                            self.valid_green_and_no_red_sources_str_set.remove(active_boolean_variable_before_str)

                            # Add the active Boolean variable before into the set of Boolean variables with no green edges and no red edges.
                            self.no_green_and_no_red_sources_str_set.add(active_boolean_variable_before_str)

    def extract_necessary_green_edge_sets(self):
        """
            Extract sets of green edge which are necessary to build the transitions.
        """

        # Initialize an empty list to store sets of green sources string which are necessary to build the transitions.
        necessary_green_sources_str_set_2d_lists = []

        # Iterate each index of transitions with the target Boolean variable is active after:
        for transition_index_with_target_active_after_int in self.inference_object.boolean_variables_str_and_indices_of_transitions_with_active_in_states_after_int_list_dict[self.target_boolean_variable_str]:

            # If the target Boolean variable does not have a red self loop:
            if not self.has_red_self_bool:

                # If the target Boolean variable is active before:
                if self.inference_object.states_transitions_object.transitions_dict_1d_tuple_1d_list[transition_index_with_target_active_after_int][0][self.target_boolean_variable_str]:

                    # No need to check this transition because the target Boolean variable is possible to maintain its active state.
                    continue

            # Initialize an empty list to store the current set of green edge which are necessary to build the transitions.
            necessary_green_sources_str_set_list = []

            # Iterate each index of active Boolean variables before at the current transition with the target Boolean variable active after:
            for active_boolean_variable_before_str in self.inference_object.active_boolean_variables_in_states_before_2d_list[transition_index_with_target_active_after_int]:

                # If this active Boolean variable is a member to have a valid green edge and no red edge to the target Boolean variable:
                if active_boolean_variable_before_str in self.valid_green_and_no_red_sources_str_set:

                    # Append the index of this active Boolean variable at the end of the list which stores the current set of green edge which are necessary to build the transitions.
                    necessary_green_sources_str_set_list.append(active_boolean_variable_before_str)

            # Append the current list at the end of the list to store sets of green edge which are necessary to build the transitions.
            necessary_green_sources_str_set_2d_lists.append(necessary_green_sources_str_set_list)

        # Sort indices of all sets by the number of their elements.
        sorted_indices_of_sets_int_list = sorted(range(len(necessary_green_sources_str_set_2d_lists)), key=lambda i: len(necessary_green_sources_str_set_2d_lists[i]))

        # Initialize an empty set to store indices to remove.
        indices_of_sets_to_remove_int_set = set()

        # Iterate each list of edge sets in sorted order:
        for shorter_sources_str_set_list_sub_index_int, shorter_sources_str_set_list_index_int in enumerate(sorted_indices_of_sets_int_list):

            # Convert list to set for fast subset checking.
            shorter_sources_str_set = set(necessary_green_sources_str_set_2d_lists[shorter_sources_str_set_list_index_int])

            # Iterate each longer list of edge sets:
            for longer_sources_str_set_list_int in sorted_indices_of_sets_int_list[shorter_sources_str_set_list_sub_index_int + 1:]:

                # If the current longer list has not been determined to remove:
                if longer_sources_str_set_list_int not in indices_of_sets_to_remove_int_set:

                    # Convert list to set for the fast subset checking.
                    longer_sources_str_set = set(necessary_green_sources_str_set_2d_lists[longer_sources_str_set_list_int])

                    # If the current shorter list is a subset of the current longer list:
                    if shorter_sources_str_set.issubset(longer_sources_str_set):

                        # Add the current longer list to remove.
                        indices_of_sets_to_remove_int_set.add(longer_sources_str_set_list_int)

        # Remove marked lists.
        necessary_green_sources_str_set_2d_lists = [necessary_green_sources_str_set_2d_lists[i] for i in range(len(necessary_green_sources_str_set_2d_lists)) if i not in indices_of_sets_to_remove_int_set]

        # Initialize an empty set to store indices to remove.
        indices_of_sets_to_remove_int_set = set()

        # Initialize an empty set to store new Boolean variables which must have green edge to the target Boolean variable.
        new_green_sources_str_set = set()

        # Iterate each index of sets of green edge which are necessary to build the transitions:
        for necessary_green_sources_str_set_list_index_int in range(len(necessary_green_sources_str_set_2d_lists)):

            # If there is only one green edge in this set which is necessary to build the transitions:
            if len(necessary_green_sources_str_set_2d_lists[necessary_green_sources_str_set_list_index_int]) == 1:

                # Add the current Boolean variable to remove.
                indices_of_sets_to_remove_int_set.add(necessary_green_sources_str_set_list_index_int)

                # Add this Boolean variable into the set with new Boolean variables which must have green edge to the target Boolean variable.
                new_green_sources_str_set.add(necessary_green_sources_str_set_2d_lists[necessary_green_sources_str_set_list_index_int][0])

        # Add these new Boolean variables into the attribute set with determined Boolean variables which must have green edge to the target Boolean variable.
        self.determined_green_sources_str_set.update(new_green_sources_str_set)

        # Remove these new Boolean variables from the attribute set with Boolean variables which have valid green edge and no red edge to the target Boolean variable.
        self.valid_green_and_no_red_sources_str_set.difference_update(new_green_sources_str_set)

        # Remove marked lists.
        necessary_green_sources_str_set_2d_lists = [necessary_green_sources_str_set_2d_lists[i] for i in range(len(necessary_green_sources_str_set_2d_lists)) if i not in indices_of_sets_to_remove_int_set]

        # Initialize an object of BooleanVariablesSets.
        necessary_green_sources_str_sets_object = BooleanVariablesSets(boolean_variables_str_and_ordered_indices_int_dict=self.inference_object.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict)

        # Iterate each list of sets of green edge which are necessary to build the transitions.
        for necessary_green_sources_str_set_1d_list in necessary_green_sources_str_set_2d_lists:

            # Add the set of green edge into the object.
            necessary_green_sources_str_sets_object.add_one_boolean_variables_set(necessary_green_sources_str_set_1d_list)

        # Initialize the attribute as the object of BooleanVariablesSets containing sets of green edges which are necessary to build the transitions.
        self.necessary_green_sources_str_sets_object = necessary_green_sources_str_sets_object

    def extract_necessary_red_edge_sets(self):
        """
            Extract sets of red edge which are necessary to build the transitions.
        """

        # Initialize an empty list to store sets of red edge which are necessary to build the transitions.
        necessary_red_sources_str_sets_2d_list = []

        # If the current checking does not have a red self edge:
        if not self.has_red_self_bool:

            # Iterate each index of transitions with the target Boolean variable is inactive after:
            for transition_index_with_target_inactive_after_int in self.inference_object.boolean_variables_str_and_indices_of_transitions_with_inactive_in_states_after_int_list_dict[self.target_boolean_variable_str]:

                # If the target Boolean variable is active before:
                if self.inference_object.states_transitions_object.transitions_dict_1d_tuple_1d_list[transition_index_with_target_inactive_after_int][0][self.target_boolean_variable_str]:

                    # Initialize an empty list to store the current set of red edge which are necessary to build the transitions.
                    necessary_red_sources_str_list = []

                    # Iterate each index of active Boolean variables before at the current transition with the target Boolean variable inactive after:
                    for active_boolean_variable_before_str in self.inference_object.active_boolean_variables_in_states_before_2d_list[transition_index_with_target_inactive_after_int]:

                        # If this active Boolean variable is a member to have an invalid green edge and valid red edge to the target Boolean variable:
                        if active_boolean_variable_before_str in self.invalid_green_and_valid_red_sources_str_set:

                            # Append the active Boolean variable at the end of the list which stores the current set of red edge which are necessary to build the transitions.
                            necessary_red_sources_str_list.append(active_boolean_variable_before_str)

                    # Append the current list at the end of the list to store sets of red edge which are necessary to build the transitions.
                    necessary_red_sources_str_sets_2d_list.append(necessary_red_sources_str_list)

            # Sort indices of all lists by the number of their elements.
            sorted_indices_of_sets_int_list = sorted(range(len(necessary_red_sources_str_sets_2d_list)), key=lambda i: len(necessary_red_sources_str_sets_2d_list[i]))

            # Initialize an empty set to store indices to remove.
            indices_of_sets_to_remove_int_set = set()

            # Iterate each list of sources sets in sorted order:
            for shorter_sources_str_set_list_sub_index_int, shorter_sources_str_set_list_index_int in enumerate(sorted_indices_of_sets_int_list):

                # Convert list to set for fast subset checking.
                shorter_sources_str_set = set(necessary_red_sources_str_sets_2d_list[shorter_sources_str_set_list_index_int])

                # Iterate each longer list of sources sets:
                for longer_sources_str_set_list_index_int in sorted_indices_of_sets_int_list[shorter_sources_str_set_list_sub_index_int + 1:]:

                    # If the current longer list has not been determined to remove:
                    if longer_sources_str_set_list_index_int not in indices_of_sets_to_remove_int_set:

                        # Convert list to set for fast subset checking.
                        longer_sources_str_set = set(necessary_red_sources_str_sets_2d_list[longer_sources_str_set_list_index_int])

                        # If the current shorter list is a subset of the current longer list:
                        if shorter_sources_str_set.issubset(longer_sources_str_set):

                            # Add the current longer list to remove.
                            indices_of_sets_to_remove_int_set.add(longer_sources_str_set_list_index_int)

            # Remove marked lists.
            necessary_red_sources_str_sets_2d_list = [necessary_red_sources_str_sets_2d_list[i] for i in range(len(necessary_red_sources_str_sets_2d_list)) if i not in indices_of_sets_to_remove_int_set]

            # Initialize an empty set to store indices to remove.
            indices_to_remove_int_set = set()

            # Initialize an empty set to store new Boolean variables which must have green edge to the target Boolean variable.
            new_red_sources_str_set = set()

            # Iterate each index of sets of green sources which are necessary to build the transitions:
            for necessary_red_sources_str_set_list_index_int in range(len(necessary_red_sources_str_sets_2d_list)):

                # If there is only one green edge in this set which is necessary to build the transitions:
                if len(necessary_red_sources_str_sets_2d_list[necessary_red_sources_str_set_list_index_int]) == 1:

                    # Add the current list to remove.
                    indices_to_remove_int_set.add(necessary_red_sources_str_set_list_index_int)

                    # Add this Boolean variable into the set with new Boolean variables which must have red sources to the argument Boolean variable.
                    new_red_sources_str_set.add(necessary_red_sources_str_sets_2d_list[necessary_red_sources_str_set_list_index_int][0])

            # Add these new Boolean variables into the attribute set with determined Boolean variables which must have red sources to the argument Boolean variable.
            self.determined_red_sources_str_set.update(new_red_sources_str_set)

            # Remove these new Boolean variables from the attribute set with Boolean variables which have invalid green edge and valid red edge to the argument Boolean variable.
            self.invalid_green_and_valid_red_sources_str_set.difference_update(new_red_sources_str_set)

            # Remove marked lists.
            necessary_red_sources_str_sets_2d_list = [necessary_red_sources_str_sets_2d_list[i] for i in range(len(necessary_red_sources_str_sets_2d_list)) if i not in indices_to_remove_int_set]

        # Initialize an object of BooleanVariablesSets.
        necessary_red_sources_str_sets_object = BooleanVariablesSets(boolean_variables_str_and_ordered_indices_int_dict=self.inference_object.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict)

        # Iterate each list of sets of red sources which are necessary to build the transitions.
        for necessary_red_sources_str_set_1d_list in necessary_red_sources_str_sets_2d_list:

            # Add the set of red sources into the object.
            necessary_red_sources_str_sets_object.add_one_boolean_variables_set(necessary_red_sources_str_set_1d_list)

        # Initialize the attribute as the object of BooleanVariablesSets containing sets of red edges which are necessary to build the transitions.
        self.necessary_red_sources_str_sets_object = necessary_red_sources_str_sets_object

    def extract_conjugated_edge_sets(self):
        """
            Extract sets of edge such that if there exists a green edge in one set, then there must be a red edge in this set to build the transitions.
        """

        # Initialize an empty list to store sets of conjugated sources to build the transitions.
        conjugated_sources_str_sets_2d_lists = []

        # Iterate each index of transitions with the target Boolean variable is inactive after:
        for transition_index_with_target_inactive_after_int in self.inference_object.boolean_variables_str_and_indices_of_transitions_with_inactive_in_states_after_int_list_dict[self.target_boolean_variable_str]:

            # If the target Boolean variable does not have a red self loop:
            if not self.has_red_self_bool:

                # If the target Boolean variable is active before:
                if self.inference_object.states_transitions_object.transitions_dict_1d_tuple_1d_list[transition_index_with_target_inactive_after_int][0][self.target_boolean_variable_str]:

                    # No need to check this transition because the requirement has been contained in the necessary red edges.
                    continue

            # Initialize an empty list to store the current set of conjugated sources to build the transitions.
            conjugated_sources_str_set_list = []

            # Initialize a Boolean variable to denote if the current set of conjugated sources has been satisfied or not.
            has_been_satisfied_bool = False

            # Initialize a Boolean variable to denote if the current set of conjugated sources should be added into the sets of necessary red sources or not.
            is_in_red_bool = False

            # Iterate each index of active Boolean variables before at the current transition with the argument Boolean variable inactive after:
            for active_boolean_variable_before_str in self.inference_object.active_boolean_variables_in_states_before_2d_list[transition_index_with_target_inactive_after_int]:

                # If this active Boolean variable is not the argument Boolean variable:
                if active_boolean_variable_before_str != self.target_boolean_variable_str:

                    # If this active Boolean variable is a member which cannot have a green edge or a red edge to the argument Boolean variable:
                    if active_boolean_variable_before_str in self.no_green_and_no_red_sources_str_set:

                        # This active Boolean variable has no effects. Access the next active Boolean variable directly.
                        continue

                    # If this active Boolean variable is a member which must have a red edge to the argument Boolean variable:
                    elif active_boolean_variable_before_str in self.determined_red_sources_str_set:

                        # The current set of conjugated sources has been satisfied.
                        has_been_satisfied_bool = True

                        # No need to check following active Boolean variables.
                        break

                    # If this active Boolean variable is a member which must have a green edge to the argument Boolean variable:
                    elif active_boolean_variable_before_str in self.determined_green_sources_str_set:

                        # The current set of conjugated sources should be added into the sets of necessary red sources.
                        is_in_red_bool = True

                    # For other cases:
                    else:

                        # Add the current active Boolean variable as a member of the current list to store sets of conjugated sources to build the transitions.
                        conjugated_sources_str_set_list.append(active_boolean_variable_before_str)

            # If the current list to store sets of conjugated sources has not been satisfied, or it may be violated:
            if not has_been_satisfied_bool and len(conjugated_sources_str_set_list) > 0:

                # If the current list to store sets of conjugated sources should be a set of necessary red sources:
                if is_in_red_bool:

                    # Select indices of Boolean variables which can have red edge to the attribute Boolean variable in the conjugated edge list.
                    conjugated_sources_str_set_list = [state_index for state_index in conjugated_sources_str_set_list if state_index in self.invalid_green_and_valid_red_sources_str_set]

                    # Add the current list of conjugated edge into the object.
                    self.necessary_red_sources_str_sets_object.add_one_boolean_variables_set(conjugated_sources_str_set_list)

                # If the current list to store sets of conjugated edge has not been converted to other types:
                else:

                    # Append the current list at the end of the list to store sets of conjugated edge which are necessary to build the transitions.
                    conjugated_sources_str_sets_2d_lists.append(conjugated_sources_str_set_list)

        # Initialize an object of BooleanVariablesSets.
        conjugated_sources_str_sets_object = BooleanVariablesSets(boolean_variables_str_and_ordered_indices_int_dict=self.inference_object.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict)

        # Iterate each list of sets of conjugated sources which are necessary to build the transitions.
        for conjugated_sources_str_set_list in conjugated_sources_str_sets_2d_lists:

            # If there exists only one edge in this list:
            if len(conjugated_sources_str_set_list) == 1:

                # If this edge is in the set of Boolean variables which have no green edge and valid red edge to the argument Boolean variable:
                if conjugated_sources_str_set_list[0] in self.no_green_and_valid_red_sources_str_set:

                    # No need to process it.
                    continue

                # If this edge is in the set of Boolean variables which have invalid green sources and valid red sources to the argument Boolean variable:
                elif conjugated_sources_str_set_list[0] in self.invalid_green_and_valid_red_sources_str_set:

                    # Remove this Boolean variable from the set of Boolean variables which have invalid green sources and valid red sources to the argument Boolean variable.
                    self.invalid_green_and_valid_red_sources_str_set.remove(conjugated_sources_str_set_list[0])

                    # Add this Boolean variable into the set of Boolean variables which have no green sources and valid red sources to the argument Boolean variable:
                    self.no_green_and_valid_red_sources_str_set.add(conjugated_sources_str_set_list[0])

                # If this edge is in the set of Boolean variables which have valid green sources and no red sources to the argument Boolean variable:
                elif conjugated_sources_str_set_list[0] in self.valid_green_and_no_red_sources_str_set:

                    # Remove this Boolean variable from the set of Boolean variables which have valid green sources and no red sources to the argument Boolean variable.
                    self.valid_green_and_no_red_sources_str_set.remove(conjugated_sources_str_set_list[0])

                    # Add this Boolean variable into the set of Boolean variables which have no green sources and no red sources to the argument Boolean variable:
                    self.no_green_and_no_red_sources_str_set.add(conjugated_sources_str_set_list[0])

                # For other cases:
                else:

                    # Print the error message.
                    print("There is a problem in extract_conjugated_edge_sets")
                    print("What", conjugated_sources_str_set_list[0])
                    print("Free", self.free_green_and_free_red_sources_str_set)
                    print("No Edges", self.no_green_and_no_red_sources_str_set)
                    print("Determined Green", self.determined_green_sources_str_set)
                    print("Determined Red", self.determined_red_sources_str_set)
                    print("Valid Green and No Red", self.valid_green_and_no_red_sources_str_set)
                    print("No Green and Valid Red", self.no_green_and_valid_red_sources_str_set)
                    print("Invalid Green and Valid Red", self.invalid_green_and_valid_red_sources_str_set)

                    # End the program directly.
                    exit(0)

            # If there exist more than one edge in this list:
            elif len(conjugated_sources_str_set_list) > 1:

                # Add the set of conjugated edge into the object.
                conjugated_sources_str_sets_object.add_one_boolean_variables_set(conjugated_sources_str_set_list)

        # Initialize the attribute as the object of BooleanVariablesSets containing sources of conjugated edges to build the transitions.
        self.conjugated_sources_str_sets_object = conjugated_sources_str_sets_object

    def decompose_solution_space(self):
        """
            Decompose solution spaces for one Boolean variable.
        """

        # Call the method to determine if some red edge to the argument Boolean variable cannot exist.
        self.check_nonexistent_red_edge_and_divide_boolean_variables()

        # Call the method to determine if some green edge to the argument Boolean variable cannot exist.
        self.check_nonexistent_green_edge_and_divide_boolean_variables()

        # Call the method to get sets with necessary green edge.
        self.extract_necessary_green_edge_sets()

        # Call the method to get sets with necessary red edge.
        self.extract_necessary_red_edge_sets()

        # Call the method to get sets with conjugated edge.
        self.extract_conjugated_edge_sets()

    def print_decomposed_information(self):
        """
            Print the decomposed information about each set.
        """

        print()
        print("Target", self.target_boolean_variable_str)
        print("Self Green? Not contained")
        print("Self Red?", self.has_red_self_bool)
        print()
        print("Free", self.free_green_and_free_red_sources_str_set)
        print("No edges", self.no_green_and_no_red_sources_str_set)
        print("Determined Green", self.determined_green_sources_str_set)
        print("Determined Red", self.determined_red_sources_str_set)
        print("Valid Green and No Red", self.valid_green_and_no_red_sources_str_set)
        print("No Green and Valid Red", self.no_green_and_valid_red_sources_str_set)
        print("Invalid Green and Valid Red", self.invalid_green_and_valid_red_sources_str_set)

        print("Green Set")

        for binary_states_of_sorted_boolean_variables_int_list in self.necessary_green_sources_str_sets_object.decimal_ids_of_boolean_variables_sets_int_and_binary_states_of_sorted_boolean_variables_int_list_dict.values():

            print(binary_states_of_sorted_boolean_variables_int_list)

        print("Red Set")
        for binary_states_of_sorted_boolean_variables_int_list in self.necessary_red_sources_str_sets_object.decimal_ids_of_boolean_variables_sets_int_and_binary_states_of_sorted_boolean_variables_int_list_dict.values():

            print(binary_states_of_sorted_boolean_variables_int_list)

        print("Conjugated Set")

        for binary_states_of_sorted_boolean_variables_int_list in self.conjugated_sources_str_sets_object.decimal_ids_of_boolean_variables_sets_int_and_binary_states_of_sorted_boolean_variables_int_list_dict.values():

            print(binary_states_of_sorted_boolean_variables_int_list)

    def enumerate_all_solutions(self) -> (list[dict[str: int]], dict[str: int], dict[str: int]):
        """
            Enumerate all solutions for one Boolean variable.

            Returns:
                (list[dict[str, int]]).
                    The 1-dimensional list containing all assignments.
                (dict[str: int]).
                    The dictionary containing key-value pairs about sources Boolean variables as string and the count of their green edges.
                (dict[str: int]).
                    The dictionary containing key-value pairs about sources Boolean variables as string and the count of their green edges.
        """

        # Call the method to decompose the solution space.
        self.decompose_solution_space()

        # Initialize the dictionary to store key-value pairs about Boolean variables and suitable green, red edges which can be applied into solutions.
        boolean_variables_str_and_suitable_assignments_int_list_dict = {}

        # Iterate each Boolean variable:
        for boolean_variable_str in self.inference_object.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict:

            # If the current Boolean variable is the argument Boolean variable.
            if boolean_variable_str == self.target_boolean_variable_str:

                # Add it into the dictionary and set its value to be -1 if there is a red self loop else 0.
                boolean_variables_str_and_suitable_assignments_int_list_dict[boolean_variable_str] = [-1] if self.has_red_self_bool else [0]

            # If the current Boolean variable has been determined to have a green edge:
            elif boolean_variable_str in self.determined_green_sources_str_set:

                # Add it into the dictionary and set its value to be 1.
                boolean_variables_str_and_suitable_assignments_int_list_dict[boolean_variable_str] = [1]

            # If the current Boolean variable has been determined to have a red edge:
            elif boolean_variable_str in self.determined_red_sources_str_set:

                # Add it into the dictionary and set its value to be -1.
                boolean_variables_str_and_suitable_assignments_int_list_dict[boolean_variable_str] = [-1]

            # If the current Boolean variable has been determined to have no edge:
            elif boolean_variable_str in self.no_green_and_no_red_sources_str_set:

                # Add it into the dictionary and set its value to be 0.
                boolean_variables_str_and_suitable_assignments_int_list_dict[boolean_variable_str] = [0]

            # If the current Boolean variable has been determined to have no red edge:
            elif boolean_variable_str in self.valid_green_and_no_red_sources_str_set:

                # Add it into the dictionary and set its value to be 0, 1.
                boolean_variables_str_and_suitable_assignments_int_list_dict[boolean_variable_str] = [0, 1]

            # If the current Boolean variable has been determined to have no green edge:
            elif boolean_variable_str in self.no_green_and_valid_red_sources_str_set:

                # Add it into the dictionary and set its value to be -1, 0.
                boolean_variables_str_and_suitable_assignments_int_list_dict[boolean_variable_str] = [-1, 0]

            # If the current Boolean variable has not been determined:
            elif boolean_variable_str in self.invalid_green_and_valid_red_sources_str_set or boolean_variable_str in self.free_green_and_free_red_sources_str_set:

                # Add it into the dictionary and set its value to be -1, 0, 1.
                boolean_variables_str_and_suitable_assignments_int_list_dict[boolean_variable_str] = [-1, 0, 1]

            # Otherwise, print the error message:
            else:

                raise ValueError(f"Variable {boolean_variable_str} not in any group.")

        # Get Cartesian product of all domain combinations.
        boolean_variables_str_list = list(boolean_variables_str_and_suitable_assignments_int_list_dict.keys())
        suitable_assignments_int_2d_list = [boolean_variables_str_and_suitable_assignments_int_list_dict[boolean_variable_str] for boolean_variable_str in boolean_variables_str_list]

        # Initialize an empty list to store all assignments.
        all_suitable_boolean_variables_str_and_one_suitable_assignments_int_dict_1d_list = []

        # Iterate each assignment of values of Boolean variable:
        for boolean_variables_assignments in itertools.product(*suitable_assignments_int_2d_list):

            # Get the current assignment and store it into a dictionary.
            boolean_variables_str_and_corresponding_assignments_int_dict = dict(zip(boolean_variables_str_list, boolean_variables_assignments))

            # Call the method to check if the current assignment is valid:
            if self.check_if_assignment_is_valid(boolean_variables_str_and_corresponding_assignments_int_dict):

                # Add the current valid assignment into the list.
                all_suitable_boolean_variables_str_and_one_suitable_assignments_int_dict_1d_list.append(boolean_variables_str_and_corresponding_assignments_int_dict)

        # Initialize an empty dictionary to store the count of green edges.
        green_sources_str_and_count_dict = {boolean_variable_str: 0 for boolean_variable_str in self.inference_object.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}

        # Initialize an empty dictionary to store the count of red edges.
        red_sources_str_and_count_dict = {boolean_variable_str: 0 for boolean_variable_str in self.inference_object.states_transitions_object.boolean_variables_str_and_ordered_indices_int_dict}

        # Iterate each solution:
        for all_suitable_boolean_variables_str_and_one_suitable_assignments_int_dict in all_suitable_boolean_variables_str_and_one_suitable_assignments_int_dict_1d_list:

            # Iterate each source Boolean variable:
            for source_boolean_variable_str in all_suitable_boolean_variables_str_and_one_suitable_assignments_int_dict:

                # If the current source Boolean variable has a green edge to the target Boolean variable:
                if all_suitable_boolean_variables_str_and_one_suitable_assignments_int_dict[source_boolean_variable_str] == 1:

                    # Increment the corresponding green edge by 1.
                    green_sources_str_and_count_dict[source_boolean_variable_str] += 1

                # If the current source Boolean variable has a red edge to the target Boolean variable:
                elif all_suitable_boolean_variables_str_and_one_suitable_assignments_int_dict[source_boolean_variable_str] == -1:

                    # Increment the corresponding red edge by 1.
                    red_sources_str_and_count_dict[source_boolean_variable_str] += 1

        # Return the list containing all assignments and counts of green and red edges.
        return all_suitable_boolean_variables_str_and_one_suitable_assignments_int_dict_1d_list, green_sources_str_and_count_dict, red_sources_str_and_count_dict

    def check_if_assignment_is_valid(self, boolean_variables_str_and_corresponding_assignments_int_dict: dict[str: int]) -> bool:
        """
            Check if the assignment to Boolean variables is valid or not.

            Arguments:
                boolean_variables_str_and_corresponding_assignments_int_dict (dict[str: int]).
                    The dictionary containing key-value pairs about Boolean variables and their assignments.
                        If the assignment is 1, then it has a green edge to the target Boolean variable.
                        If the assignment is 0, then it has no edges to the target Boolean variable.
                        If the assignment is -1, then it has a red edge to the target Boolean variable.

            Returns:
                (bool).
                    The Boolean returns if the assignment to Boolean variables is valid or not.
        """

        # Iterate each green edge set:
        for necessary_green_sources_boolean_variables_str_1d_list in self.necessary_green_sources_str_sets_object.decimal_ids_of_boolean_variables_sets_int_and_boolean_variables_str_1d_list_dict.values():

            # If there is a green edge set without any green edge:
            if all(boolean_variables_str_and_corresponding_assignments_int_dict.get(necessary_green_source_boolean_variable_str) != 1 for necessary_green_source_boolean_variable_str in necessary_green_sources_boolean_variables_str_1d_list):

                # Return False because this green edge set cannot be satisfied.
                return False

        # Iterate each red edge set:
        for necessary_red_sources_boolean_variables_str_1d_list in self.necessary_red_sources_str_sets_object.decimal_ids_of_boolean_variables_sets_int_and_boolean_variables_str_1d_list_dict.values():

            # If there is a red edge set without any red edge:
            if all(boolean_variables_str_and_corresponding_assignments_int_dict.get(necessary_red_source_boolean_variable_str) != -1 for necessary_red_source_boolean_variable_str in necessary_red_sources_boolean_variables_str_1d_list):

                # Return False because this red edge set cannot be satisfied.
                return False

        # Iterate each conjugated edge set:
        for conjugated_sources_boolean_variables_str_1d_list in self.conjugated_sources_str_sets_object.decimal_ids_of_boolean_variables_sets_int_and_boolean_variables_str_1d_list_dict.values():

            # If there is a conjugated edge set with a green edge but without any red edge:
            if any(boolean_variables_str_and_corresponding_assignments_int_dict.get(boolean_variable_str) == 1 for boolean_variable_str in conjugated_sources_boolean_variables_str_1d_list) and all(boolean_variables_str_and_corresponding_assignments_int_dict.get(boolean_variable_str) != -1 for boolean_variable_str in conjugated_sources_boolean_variables_str_1d_list):

                # Return False because this conjugated edge set cannot be satisfied.
                return False

        # Return True if all three checking processes are passed.
        return True
