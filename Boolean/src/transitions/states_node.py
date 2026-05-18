# Import to convert Boolean values to a Binary string.
from src.scripts.universal_operations import convert_boolean_dictionary_to_binary_string


class StatesNode:
    """
        This class denotes a type of nodes which represent states.

        Attributes:
            boolean_variables_str_and_boolean_values_bool_dict (dict[str: bool]).
                The dictionary containing key-value pairs about Boolean variables and their corresponding Boolean values.
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.
            decimal_states_int (int).
                The decimal integral format of states.
            child_states_node_object (StatesNode).
                The child of this node.
            parents_decimal_states_int_and_states_nodes_object_dict (dict[int: StatesNode]).
                The dictionary containing key-value pairs about decimal integral format of states nodes as parents and parents states nodes.
            component_index_int (int).
                The index of component.
            basin_size_in_component_int (int).
                The integer denoting the basin size in its component.
            height_in_component_int (int).
                The integer denoting the height in its component.
    """

    def __init__(self, boolean_variables_str_and_boolean_values_bool_dict: dict[str: bool], boolean_variables_str_and_ordered_indices_int_dict: dict[str: int]):
        """
            Construct objects by initializing attributes.

            Arguments:
                boolean_variables_str_and_boolean_values_bool_dict (dict[str: bool]).
                    The dictionary containing key-value pairs about Boolean variables and their corresponding Boolean values.
                boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                    The dictionary containing key-value pairs about Boolean variables string as keys and their corresponding indices of the order as values.
        """

        # Initialize attributes by assigning arguments to them.
        self.boolean_variables_str_and_boolean_values_bool_dict = boolean_variables_str_and_boolean_values_bool_dict
        self.boolean_variables_str_and_ordered_indices_int_dict = boolean_variables_str_and_ordered_indices_int_dict

        # Convert the Boolean values to a Binary string.
        binary_str = convert_boolean_dictionary_to_binary_string(boolean_variables_str_and_boolean_values_bool_dict=boolean_variables_str_and_boolean_values_bool_dict, boolean_variables_str_and_ordered_indices_int_dict=boolean_variables_str_and_ordered_indices_int_dict)

        # Initialize the attribute by computing.
        self.decimal_states_int = int(binary_str.replace(" ", ""), 2)

        # Initialize the attribute as None.
        self.child_states_node_object = None

        # Initialize the attribute as an empty dictionary.
        self.parents_decimal_states_int_and_states_nodes_object_dict = {}

        # Initialize the attribute as -1 to denote it has not been determined yet.
        self.component_index_int = -1

        # Initialize the attribute as 1 for itself.
        self.basin_size_in_component_int = 1

        # Initialize the attribute as -1 to denote it has not been determined yet.
        self.height_in_component_int = -1

    def add_child_states_node(self, child_states_node_object: "StatesNode"):
        """
            Add the states node as the child.

            Arguments:
                child_states_node_object (StatesNode).
                    The instance of StatesNode as the child.
        """

        # Update the child states node.
        self.child_states_node_object = child_states_node_object

    def add_parent_states_node(self, parent_states_node_object: "StatesNode"):
        """
            Add the states node as one parent.

            Arguments:
                parent_states_node_object (StatesNode).
                    The instance of StatesNode as one parent.
        """

        # If the argument states node has not been added into the dictionary:
        if parent_states_node_object.decimal_states_int not in self.parents_decimal_states_int_and_states_nodes_object_dict:

            # Add the argument states node into the dictionary as one parent states node.
            self.parents_decimal_states_int_and_states_nodes_object_dict[parent_states_node_object.decimal_states_int] = parent_states_node_object
