# Import to implement Breadth First Search.
from collections import deque

# Import to do annotations.
from src.transitions.states_node import StatesNode

# # Import to visualize.
# from src.visualization.values_visualization import visualize_3d_landscape

# Import to create arrays.
import numpy as np


class StatesComponent:
    """
        This class inherits StatesTransitions as a component of states nodes.

        Attributes:
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.
            component_decimal_states_int_and_states_nodes_object_dict (dict[int: StatesNode]).
                The dictionary containing key-value pairs about decimal integral format of states nodes and states nodes objects in this component.
            component_index_int (int).
                The integer denoting the index of this component.
            cycle_decimal_states_int_1d_list (list[int]).
                The 1-dimensional list containing decimal integral format of states nodes in the cycle of this component.
            heights_int_and_decimal_states_int_set_dict (dict[int: set[int]]).
                The dictionary containing key-value pairs about heights and their corresponding sets with the decimal states format.
    """

    def __init__(self, boolean_variables_str_and_ordered_indices_int_dict: dict[str: int], component_decimal_states_int_and_states_nodes_object_dict: dict[int: StatesNode], component_index_int: int):
        """
            Construct objects by initializing attributes.

            Arguments:
                boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                    The dictionary containing key-value pairs about Boolean variables string and their corresponding indices of the order.
                component_decimal_states_int_and_states_nodes_object_dict (dict[int: StatesNode]).
                    The dictionary containing key-value pairs about decimal integral format of states nodes and states nodes objects in this component.
                component_index_int (int).
                    The integer denoting the index of this component.
        """

        # Initialize attributes by assigning arguments to them.
        self.boolean_variables_str_and_ordered_indices_int_dict = boolean_variables_str_and_ordered_indices_int_dict
        self.component_decimal_states_int_and_states_nodes_object_dict = component_decimal_states_int_and_states_nodes_object_dict
        self.component_index_int = component_index_int

        # Call the method to initialize attributes.
        self.cycle_decimal_states_int_1d_list = self.compute_cycle_by_depth_first_search()
        self.heights_int_and_decimal_states_int_set_dict = self.compute_heights_by_breadth_first_search()

    def compute_cycle_by_depth_first_search(self) -> list[int]:
        """
             Compute the cycle of this component.

             Returns:
                 (list[int]).
                    The 1-dimensional list containing decimal integral format of states nodes in the cycle of this component.
        """

        # Initialize an empty list to store the path containing decimal integral format of states which have been visited.
        path_of_visited_decimal_states_int_1d_list = []

        # Initialize an empty dictionary to store decimal integral format of states node and their corresponding indices of being visited.
        decimal_states_int_and_visited_indices_int_dict = {}

        # Convert the decimal integral format of all states nodes in this component into a list. Get its first one.
        current_visited_decimal_states_int = list(self.component_decimal_states_int_and_states_nodes_object_dict.keys())[0]

        # While the current states node has not been recorded as visited:
        while current_visited_decimal_states_int not in decimal_states_int_and_visited_indices_int_dict:

            # Add the current states node into the dictionary to denote that it has been visited, and label its index of being visited as the length of the list.
            decimal_states_int_and_visited_indices_int_dict[current_visited_decimal_states_int] = len(path_of_visited_decimal_states_int_1d_list)

            # Add the decimal format of the current states node into the path.
            path_of_visited_decimal_states_int_1d_list.append(current_visited_decimal_states_int)

            # Update the decimal integral format of the current states node to be the decimal integral format of its child.
            current_visited_decimal_states_int = self.component_decimal_states_int_and_states_nodes_object_dict[current_visited_decimal_states_int].child_states_node_object.decimal_states_int

        # The current decimal integral format of states nodes is the first one which has been visited before. Denote it as the starting of the cycle.
        cycle_starting_index_int = decimal_states_int_and_visited_indices_int_dict[current_visited_decimal_states_int]

        # Get the list containing decimal integral format of states nodes as a cycle.
        cycle_decimal_states_int_1d_list = path_of_visited_decimal_states_int_1d_list[cycle_starting_index_int:]

        # Return the cycle of the component.
        return cycle_decimal_states_int_1d_list

    def compute_heights_by_breadth_first_search(self) -> dict[int: set[int]]:
        """
             Compute heights for all states nodes based on Breath First Search.

             Returns:
                 (dict[int: set[int]]).
                    The dictionary containing key-value pairs about heights and their corresponding decimal integral format of states nodes.
        """

        # Initialize an empty dictionary to store key-value pairs about heights and their corresponding decimal integral format of states nodes.
        heights_int_and_decimal_states_int_set_dict = {}

        # Add all decimal integral format of states nodes into the queue for heights.
        decimal_states_for_heights_int_queue = deque(self.cycle_decimal_states_int_1d_list)

        # Initialize an integer to denote the current height.
        current_height_int = 0

        # While the queue about heights has remaining decimal integral format of states nodes:
        while decimal_states_for_heights_int_queue:

            # Get the number of decimal integral format of states nodes in the queue.
            number_of_decimal_states_int_in_queue_int = len(decimal_states_for_heights_int_queue)

            # Initialize the set of states nodes with the current height.
            heights_int_and_decimal_states_int_set_dict[current_height_int] = set()

            # Iterate each number of index:
            while number_of_decimal_states_int_in_queue_int > 0:

                # Pop the left most decimal integral format of states nodes.
                decimal_states_int = decimal_states_for_heights_int_queue.popleft()

                # Update the height of the current node.
                self.component_decimal_states_int_and_states_nodes_object_dict[decimal_states_int].height_in_component_int = current_height_int

                # Add the current node into the set with that height.
                heights_int_and_decimal_states_int_set_dict[current_height_int].add(decimal_states_int)

                # Get the list containing decimal integral format of states nodes which are parents of the current node.
                parents_decimal_states_int_1d_list = list(self.component_decimal_states_int_and_states_nodes_object_dict[decimal_states_int].parents_decimal_states_int_and_states_nodes_object_dict.keys())

                # Remove the decimal integral format of states nodes which are in the cycle.
                parents_decimal_states_int_1d_list = [decimal_states_int for decimal_states_int in parents_decimal_states_int_1d_list if decimal_states_int not in self.cycle_decimal_states_int_1d_list]

                # If there is any valid parent, this states node is an intermediate node:
                if len(parents_decimal_states_int_1d_list) != 0:

                    # Extend the remaining parents states nodes to the queue.
                    decimal_states_for_heights_int_queue.extend(parents_decimal_states_int_1d_list)

                # If there is no parent, this states node is on the edge:
                else:

                    # The height of this states node is its height.
                    self.component_decimal_states_int_and_states_nodes_object_dict[decimal_states_int].height_in_component_int = current_height_int

                # Decrement the number of decimal integral format of states nodes in the queue by 1.
                number_of_decimal_states_int_in_queue_int -= 1

            # Increment the height by 1.
            current_height_int += 1

        # Return the dictionary about heights.
        return heights_int_and_decimal_states_int_set_dict

    def compute_basin_by_breadth_first_search(self):
        """
             Compute basin sizes for all states nodes based on Breath First Search.
        """

        # Iterate the height as the descending order:
        for height_int, decimal_states_int_set in sorted(self.heights_int_and_decimal_states_int_set_dict.items(), reverse=True):

            # Iterate each decimal integral format of states nodes:
            for decimal_states_int in decimal_states_int_set:

                # Get the current node.
                current_states_node_object = self.component_decimal_states_int_and_states_nodes_object_dict[decimal_states_int]

                # If the current height is not on the cycle:
                if height_int > 0:

                    # Converge the basin size of the current node into its child node.
                    current_states_node_object.child_states_node_object.basin_size_in_component_int += current_states_node_object.basin_size_in_component_int

    def check_if_component_is_a_process(self) -> int:
        """
             Check if states in the component form a process or not.

             Returns:
                 (int).
                    If this is -1, then it means that states in the component cannot form a process.
                    If this is not -1, then it denotes the decimal format of states node which is the starting point of the process.
        """

        # Initialize an integer to denote the number of states nodes which have no parents.
        number_of_states_nodes_without_parents = 0

        # Initialize an integer to denote the decimal format of states node which is the starting point of the process.
        decimal_states_of_starting_int = 0

        # Iterate each decimal format of states node:
        for decimal_states_int in self.component_decimal_states_int_and_states_nodes_object_dict:

            # If the number of states nodes which have no parents is more than 1:
            if number_of_states_nodes_without_parents > 1:

                # Return -1 to denote that the component cannot form a process.
                return -1

            # If the number of states nodes which have no parents is no more than 1:
            else:

                # Get the current states node object.
                states_nodes_object = self.component_decimal_states_int_and_states_nodes_object_dict[decimal_states_int]

                # If the current states node object has no parents:
                if len(states_nodes_object.parents_decimal_states_int_and_states_nodes_object_dict) == 0:

                    # Increment the number of states nodes which have no parents by 1.
                    number_of_states_nodes_without_parents += 1

                    # Update the decimal format of states node which is the starting point of the process.
                    decimal_states_of_starting_int = decimal_states_int

        # If there is only one states nodes which has no parents:
        if number_of_states_nodes_without_parents == 1:

            # Return the decimal format of states node which is the starting point of the process.
            return decimal_states_of_starting_int

        # If there is more than one states nodes which has no parents:
        else:

            # Return -1 to denote that states in the component cannot form a process.
            return -1

    # def visualize_transitions_landscape(self):
    #     """
    #         Visualize
    #     """
    #
    #     # Initialize an empty dictionary to store key-value pairs about decimal integral format of states nodes and their corresponding 3D coordinates as a 1-dimensional tuple.
    #     decimal_states_int_and_coordinates_float_1d_tuple_dict = {}
    #
    #     # If there is only one attractor:
    #     if len(self.cycle_decimal_states_int_1d_list) == 1:
    #
    #         # Set its coordinates as the zero point.
    #         decimal_states_int_and_coordinates_float_1d_tuple_dict[self.cycle_decimal_states_int_1d_list[0]] = (0.0, 0.0, 0.0)
    #
    #     # If there is a limited cycle:
    #     else:
    #
    #         # Divide 360 degrees into the same number of states nodes in the cycle uniformly.
    #         angles_float_1d_array = np.linspace(0, 2 * np.pi, len(self.cycle_decimal_states_int_1d_list), endpoint=False)
    #
    #         # Initialize a float to denote the radius.
    #         radius_float = 0.5
    #
    #         # Iterate each integral format of states nodes in the cycle and each angle:
    #         for cycle_decimal_states_int, theta_float in zip(self.cycle_decimal_states_int_1d_list, angles_float_1d_array):
    #
    #             # Update the coordinates of the current states node from the cycle in the dictionary.
    #             decimal_states_int_and_coordinates_float_1d_tuple_dict[cycle_decimal_states_int] = (radius_float * np.cos(theta_float), radius_float * np.sin(theta_float), 0.0)
    #
    #     # Initialize an empty dictionary to store key-value pairs about heights and their corresponding 1-dimensional list containing decimal integral format of states nodes:
    #     heights_int_and_decimal_states_int_1d_list_dict = {}
    #
    #     # Initialize an integer to denote the maximal height.
    #     max_height_int = 0
    #
    #     # Iterate each decimal integral format of states node in the component:
    #     for component_decimal_states_int in self.component_decimal_states_int_and_states_nodes_object_dict:
    #
    #         # If the current states node is not in the cycle:
    #         if component_decimal_states_int not in self.cycle_decimal_states_int_1d_list:
    #
    #             # Get the current states node object.
    #             states_nodes_object = self.component_decimal_states_int_and_states_nodes_object_dict[component_decimal_states_int]
    #
    #             # Append the current states node into the list with that height.
    #             heights_int_and_decimal_states_int_1d_list_dict.setdefault(states_nodes_object.height_in_component_int, []).append(component_decimal_states_int)
    #
    #             # Update the maximal height.
    #             max_height_int = max(max_height_int, states_nodes_object.height_in_component_int)
    #
    #     # Iterate each height:
    #     for height_int in range(1, max_height_int + 1):
    #
    #         # Get the 1-dimensional list containing decimal integral format of states nodes with that height.
    #         decimal_states_int_1d_list = heights_int_and_decimal_states_int_1d_list_dict.get(height_int, [])
    #
    #         # If the current height has states nodes:
    #         if len(decimal_states_int_1d_list) != 0:
    #
    #             # Set the radius as the current height.
    #             radius_int = height_int
    #
    #             # Divide 360 degrees into the same number of states nodes in the cycle uniformly.
    #             angles_float_1d_array = np.linspace(0, 2 * np.pi, len(decimal_states_int_1d_list), endpoint=False)
    #
    #             # Iterate each integral format of states nodes and each angle:
    #             for decimal_states_int, theta_float in zip(decimal_states_int_1d_list, angles_float_1d_array):
    #
    #                 # Get the X-coordinate.
    #                 x_coordinate_float = radius_int * np.cos(theta_float)
    #
    #                 # Get the Y-coordinate.
    #                 y_coordinate_float = radius_int * np.sin(theta_float)
    #
    #                 # Get the Z-coordinate.
    #                 z_coordinate_float = height_int
    #
    #                 # Update the coordinates of the current states node in the dictionary.
    #                 decimal_states_int_and_coordinates_float_1d_tuple_dict[decimal_states_int] = (x_coordinate_float, y_coordinate_float, z_coordinate_float)
    #
    #     # Call the method to visualize 3D landscape.
    #     visualize_3d_landscape(keys_int_and_coordinates_float_1d_tuple_dict=decimal_states_int_and_coordinates_float_1d_tuple_dict)