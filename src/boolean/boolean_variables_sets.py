# Import chain, combinations packages to get power sets.
from itertools import chain, combinations

# Import to convert Boolean values to a Binary string.
from src.scripts.universal_operations import boolean_str_1d_list_to_decimal_int


class BooleanVariablesSets:
    """
        This class represents a class containing sets containing Boolean variables.

        Attributes:
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.
            ordered_indices_of_existent_boolean_variables_int_set (set[int]).
                The set containing indices of Boolean variables, which are existent in the group.
            decimal_ids_of_boolean_variables_sets_int_and_boolean_variables_str_1d_list_dict (dict[int: list[int]]).
                The dictionary containing key-value pairs about decimal ids of sets of Boolean variables and their sets.
    """

    def __init__(self, boolean_variables_str_and_ordered_indices_int_dict: dict[str: int]):
        """
            Construct objects by initializing attributes.

            Arguments:
                boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                    The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.
        """

        # Initialize the attribute by assigning the argument to it.
        self.boolean_variables_str_and_ordered_indices_int_dict = boolean_variables_str_and_ordered_indices_int_dict

        # Initialize the attribute as an empty set.
        self.ordered_indices_of_existent_boolean_variables_int_set = set()

        # Initialize the attribute as an empty dictionary.
        self.decimal_ids_of_boolean_variables_sets_int_and_boolean_variables_str_1d_list_dict = {}

    def add_one_boolean_variables_set(self, boolean_variables_str_1d_list: list[str]):
        """
            Add a set of Boolean variables into the attribute dictionary.

            Arguments:
                boolean_variables_str_1d_list (list[str]).
                    The 1-dimensional list containing Boolean variables, which will be as an existent set in the group.
        """

        # Initialize a dictionary containing key-value pairs about Boolean variables as string and Boolean values. Initialize all Boolean values as False.
        boolean_variables_str_and_boolean_values_bool_dict = {boolean_variable_str: False for boolean_variable_str in self.boolean_variables_str_and_ordered_indices_int_dict}

        # Iterate each Boolean variable from the argument:
        for boolean_variable_str in boolean_variables_str_1d_list:

            # Get the index of the current Boolean variable in the dictionary.
            boolean_variables_str_and_boolean_values_bool_dict[boolean_variable_str] = True

            # Add the ordered index of the current existent Boolean variable into the attribute set.
            self.ordered_indices_of_existent_boolean_variables_int_set.add(self.boolean_variables_str_and_ordered_indices_int_dict[boolean_variable_str])

        # Get the decimal integral format of this Boolean variables set.
        boolean_variables_set_decimal_int = boolean_str_1d_list_to_decimal_int(boolean_variables_str_1d_list=boolean_variables_str_1d_list, boolean_variables_str_and_ordered_indices_int_dict=self.boolean_variables_str_and_ordered_indices_int_dict)

        # If this decimal id has not been in the attribute dictionary:
        if boolean_variables_set_decimal_int not in self.decimal_ids_of_boolean_variables_sets_int_and_boolean_variables_str_1d_list_dict:

            # Add the key-value pair into the attribute dictionary. The key is the decimal id and the value is the argument list.
            self.decimal_ids_of_boolean_variables_sets_int_and_boolean_variables_str_1d_list_dict[boolean_variables_set_decimal_int] = boolean_variables_str_1d_list

    def remove_super_edges_set_lists(self):
        """
            Sorts the attribute dictionary by the length of its values (lists of edges sets) and
            removes lists of edges sets where one list contains all elements of another list.
        """

        # Initialize an empty set to store decimal format of Boolean variables set to remove.
        decimal_ids_of_boolean_variables_sets_to_remove_int_set = set()

        # Iterate each decimal id of Boolean variables sets as the target:
        for target_decimal_ids_of_boolean_variables_sets_int in self.decimal_ids_of_boolean_variables_sets_int_and_boolean_variables_str_1d_list_dict:

            # Iterate each decimal id of Boolean variables sets:
            for current_decimal_ids_of_boolean_variables_sets_int in self.decimal_ids_of_boolean_variables_sets_int_and_boolean_variables_str_1d_list_dict:

                # If the current one is a super set:
                if target_decimal_ids_of_boolean_variables_sets_int != current_decimal_ids_of_boolean_variables_sets_int and (target_decimal_ids_of_boolean_variables_sets_int & current_decimal_ids_of_boolean_variables_sets_int) == target_decimal_ids_of_boolean_variables_sets_int:

                    # Add the current decimal id of Boolean variables set as one to remove.
                    decimal_ids_of_boolean_variables_sets_to_remove_int_set.add(current_decimal_ids_of_boolean_variables_sets_int)

        # Iterate each decimal id of Boolean variables sets to remove:
        for decimal_id_of_boolean_variables_set_to_remove_int in decimal_ids_of_boolean_variables_sets_to_remove_int_set:

            # Remove key-value pairs with marked decimal ids of Boolean variables sets from the attribute dictionary.
            del self.decimal_ids_of_boolean_variables_sets_int_and_boolean_variables_str_1d_list_dict[decimal_id_of_boolean_variables_set_to_remove_int]

    def get_hitting_sets_list(self) -> list[set[int]]:
        """
            Get all possible hitting sets such that each list in the attribute dictionary has at least one element in each hitting set.

            Returns:
                (list[set[int]]):
                    The 2-dimensional list containing all hitting sets.
        """

        # Get the power set of all ordered indices of existent Boolean variables.
        ordered_indices_of_existent_boolean_variables_int_power_set_1d_list = list(chain.from_iterable(combinations(self.ordered_indices_of_existent_boolean_variables_int_set, r) for r in range(1, len(self.ordered_indices_of_existent_boolean_variables_int_set) + 1)))

        # Iterate each subset of ordered indices of existent Boolean variables:
        for ordered_indices_of_existent_boolean_variables_int_sub_set in ordered_indices_of_existent_boolean_variables_int_power_set_1d_list:

            # Initialize a Boolean variable to denote that if the current subset is a hitting set or not. Initialize it as True.
            is_a_hitting_set_bool = True

            # Iterate each Boolean variables set:
            for boolean_variables_str_1d_list in self.decimal_ids_of_boolean_variables_sets_int_and_boolean_variables_str_1d_list_dict.values():

                # Initialize a Boolean variable to denote that if the current subset can hit the current set or not. Initialize it as True.
                does_hit_bool = False

                # Iterate each Boolean variable in the set:
                for boolean_variable_str in boolean_variables_str_1d_list:

                    # If the current Boolean variable is in the subset:
                    if self.boolean_variables_str_and_ordered_indices_int_dict[boolean_variable_str] in ordered_indices_of_existent_boolean_variables_int_sub_set:

                        # Hit successfully.
                        does_hit_bool = True

                        # No need to check other Boolean variables.
                        break

                # If the Boolean variable denotes that the current subset fails to hit:
                if not does_hit_bool:

                    # Set the current subset is not a hitting set.
                    is_a_hitting_set_bool = False

            # If the current Boolean variable denotes that the current subset is a hitting set:
            if is_a_hitting_set_bool:

                # Yield the current hitting set.
                yield set(ordered_indices_of_existent_boolean_variables_int_sub_set)
