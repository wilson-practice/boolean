# Import to convert Boolean values to a Binary string.
from src.scripts.universal_operations import convert_boolean_dictionary_to_binary_string, find, union

# Import to initialize its objects.
from src.transitions.states_component import StatesComponent

# Import to initialize its objects.
from src.transitions.states_node import StatesNode


class StatesTransitions:
    """
        This class denotes transitions of states.

        Attributes:
             transitions_dict_1d_tuple_1d_list (list[(dict[str: bool], dict[str: bool])]).
                The list containing all transitions as tuples.
                The first element in each tuple is a dictionary denoting binary states before.
                The second element in each tuple is a dictionary denoting binary states after.
             boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.
             decimal_states_int_and_states_nodes_object_dict (dict[int: StatesNode]).
                The dictionary containing key-value pairs about decimal integral format of states nodes and states nodes objects.
             components_indices_int_and_states_components_object_dict (dict[int: StatesComponent]).
                The dictionary containing key-value pairs about indices of components and their corresponding objects.
    """

    def __init__(self, transitions_dict_1d_tuple_1d_list: list[(dict[str: bool], dict[str: bool])], boolean_variables_str_and_ordered_indices_int_dict: dict[str: int]):
        """
            Construct objects by initializing attributes.

            Arguments:
                transitions_dict_1d_tuple_1d_list (list[(dict[str: bool], dict[str: bool])]).
                    The list containing all transitions as tuples.
                    The first element in each tuple is a dictionary denoting binary states before.
                    The second element in each tuple is a dictionary denoting binary states after.
                boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                    The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.
        """

        # Initialize attributes by assigning arguments to them.
        self.transitions_dict_1d_tuple_1d_list = transitions_dict_1d_tuple_1d_list
        self.boolean_variables_str_and_ordered_indices_int_dict = boolean_variables_str_and_ordered_indices_int_dict

        # Initialize the attribute as an empty dictionary.
        self.decimal_states_int_and_states_nodes_object_dict = {}

        # Iterate each transition:
        for transition_tuple in self.transitions_dict_1d_tuple_1d_list:

            # Get the dictionary about states before.
            states_before_boolean_variables_str_and_boolean_values_bool_dict = transition_tuple[0]

            # Convert Boolean values of states before into a Binary string.
            states_before_binary_str = convert_boolean_dictionary_to_binary_string(boolean_variables_str_and_boolean_values_bool_dict=states_before_boolean_variables_str_and_boolean_values_bool_dict, boolean_variables_str_and_ordered_indices_int_dict=self.boolean_variables_str_and_ordered_indices_int_dict)

            # Get the decimal integral format of states before.
            states_before_decimal_states_int = int(states_before_binary_str.replace(" ", ""), 2)

            # If the states before have not been added into the dictionary yet:
            if states_before_decimal_states_int not in self.decimal_states_int_and_states_nodes_object_dict:

                # Initialize an instance of StatesNode as the current states and add it into the dictionary.
                self.decimal_states_int_and_states_nodes_object_dict[states_before_decimal_states_int] = StatesNode(states_before_boolean_variables_str_and_boolean_values_bool_dict, self.boolean_variables_str_and_ordered_indices_int_dict)

            # Get the instance of states before.
            states_before_node_object = self.decimal_states_int_and_states_nodes_object_dict[states_before_decimal_states_int]

            # Get the dictionary about states after.
            states_after_boolean_variables_str_and_boolean_values_bool_dict = transition_tuple[1]

            # Convert Boolean values of states after into a Binary string.
            states_after_binary_str = convert_boolean_dictionary_to_binary_string(boolean_variables_str_and_boolean_values_bool_dict=states_after_boolean_variables_str_and_boolean_values_bool_dict, boolean_variables_str_and_ordered_indices_int_dict=self.boolean_variables_str_and_ordered_indices_int_dict)

            # Get the decimal integral format of states after.
            states_after_decimal_states_int = int(states_after_binary_str.replace(" ", ""), 2)

            # If the states after have not been added into the dictionary yet:
            if states_after_decimal_states_int not in self.decimal_states_int_and_states_nodes_object_dict:

                # Initialize states after node.
                self.decimal_states_int_and_states_nodes_object_dict[states_after_decimal_states_int] = StatesNode(states_after_boolean_variables_str_and_boolean_values_bool_dict, self.boolean_variables_str_and_ordered_indices_int_dict)

            # Get the instance of states after.
            states_after_node_object = self.decimal_states_int_and_states_nodes_object_dict[states_after_decimal_states_int]

            # Add the instance of states after as a child of the instance of states before.
            states_before_node_object.add_child_states_node(states_after_node_object)

            # Add the instance of states before as a parent of the instance of states after.
            states_after_node_object.add_parent_states_node(states_before_node_object)

        # Initialize the attribute as an empty dictionary.
        self.components_indices_int_and_states_components_object_dict = {}

        # Call the method to build components.
        self.compute_components_of_states_nodes()

    def compute_components_of_states_nodes(self):
        """
            Compute components for all states nodes.
        """

        # Initialize an empty dictionary to store key-value pairs about decimal integral format of states nodes and the decimal integral format of their corresponding leaders.
        decimal_states_int_and_leader_decimal_states_int_int_dict = {}

        # Iterate each decimal integral format of states nodes:
        for decimal_states_int in self.decimal_states_int_and_states_nodes_object_dict:

            # Assign the decimal integral format of the states nodes as the decimal integral format of its own leader.
            decimal_states_int_and_leader_decimal_states_int_int_dict[decimal_states_int] = decimal_states_int

        # Iterate each decimal integral format of states nodes:
        for decimal_states_int in self.decimal_states_int_and_states_nodes_object_dict:

            # Get the parent states node.
            parent_states_node_object = self.decimal_states_int_and_states_nodes_object_dict[decimal_states_int]

            # Get the child states node.
            child_states_node_object = self.decimal_states_int_and_states_nodes_object_dict[decimal_states_int].child_states_node_object
            
            # Union the parent states node and the child states node into one component.
            union(parent_states_node_object.decimal_states_int, child_states_node_object.decimal_states_int, decimal_states_int_and_leader_decimal_states_int_int_dict)
        
        # Initialize an empty dictionary to store key-value pairs about the decimal integral format of final leaders and the decimal integral format of their corresponding members.
        final_leader_decimal_states_int_and_decimal_states_int_set_dict = {}

        # Iterate each decimal integral format of states nodes:
        for decimal_states_int in decimal_states_int_and_leader_decimal_states_int_int_dict:

            # Call the method to get the decimal integral format of its final leader.
            final_leader_decimal_states_int = find(decimal_states_int, decimal_states_int_and_leader_decimal_states_int_int_dict)

            # If the decimal integral format of its final leader is not in the dictionary:
            if final_leader_decimal_states_int not in final_leader_decimal_states_int_and_decimal_states_int_set_dict:

                # Add the decimal integral format of its final leader into the dictionary. Initialize its value as an empty set.
                final_leader_decimal_states_int_and_decimal_states_int_set_dict[final_leader_decimal_states_int] = set()

            # Increment the size of this component by 1.
            final_leader_decimal_states_int_and_decimal_states_int_set_dict[final_leader_decimal_states_int].add(decimal_states_int)

        # Initialize an integer as the index of a component.
        component_index_int = 0

        # Iterate each flag of components as the ascending order of their sizes:
        for final_leader_decimal_states_int in sorted(final_leader_decimal_states_int_and_decimal_states_int_set_dict, key=lambda k: len(final_leader_decimal_states_int_and_decimal_states_int_set_dict[k])):

            # Initialize an empty dictionary to store key-value pairs about decimal integral format of states nodes and their corresponding objects in the current component.
            component_decimal_states_int_and_states_nodes_object_dict = {}

            # Iterate each decimal integral format of states nodes in the current component:
            for decimal_states_int in final_leader_decimal_states_int_and_decimal_states_int_set_dict[final_leader_decimal_states_int]:

                # Set the index of component for the current node.
                self.decimal_states_int_and_states_nodes_object_dict[decimal_states_int].component_index_int = component_index_int

                # Add the key-value pair of the current node into the dictionary.
                component_decimal_states_int_and_states_nodes_object_dict[decimal_states_int] = self.decimal_states_int_and_states_nodes_object_dict[decimal_states_int]

            # Update the current component.
            self.components_indices_int_and_states_components_object_dict[component_index_int] = StatesComponent(boolean_variables_str_and_ordered_indices_int_dict=self.boolean_variables_str_and_ordered_indices_int_dict, component_decimal_states_int_and_states_nodes_object_dict=component_decimal_states_int_and_states_nodes_object_dict, component_index_int=component_index_int)

            # Increment the index of the component by 1.
            component_index_int += 1
