# Import to do annotations.
from typing import Callable

# Import os package to generate paths.
import os


def load_general_boolean_network(general_boolean_network_file_name_with_type_str: str, boolean_variables_str_and_ordered_indices_int_dict: dict[str: int] = None) -> (dict[str: Callable], dict[str: str], dict[str: int]):
    """
        Load the file containing a general boolean network.

        Attributes:
            general_boolean_network_file_name_with_type_str (str).
                The name of the file containing a general boolean network with the type of the file.
            boolean_variables_str_and_ordered_indices_int_dict (dict[str: int]).
                Default value is None.
                The dictionary containing key-value pairs about Boolean variables string as keys and their corresponding indices of the order as values.
                    
        Returns:
            (dict[str: Callable]).
                The dictionary containing key-value pairs about Boolean variables and their corresponding Boolean expressions.
            (dict[str: str]).
                The dictionary containing key-value pairs about Boolean variables and their corresponding Boolean expressions.
            (dict[str: int]).
                The dictionary containing key-value pairs about Boolean variables string as keys and their corresponding indices of the order as values.
    """

    # Get the path of the project.
    project_directory_path_str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    # Get the path of the file containing a general boolean network.
    general_boolean_network_file_path_with_name_and_type_str = os.path.join(project_directory_path_str, "data/networks", general_boolean_network_file_name_with_type_str)

    # Initialize an empty set to store all Boolean variables.
    boolean_variables_str_set = set()
    
    # If the argument does not explicitly provide the order of Boolean variables:
    if boolean_variables_str_and_ordered_indices_int_dict is None:
        
        # Initialize a Boolean variable to denote that the order of Boolean variables should be checked.
        need_boolean_variables_str_and_ordered_indices_int_dict_bool = True
        
        # Initialize an empty dictionary to store the key-value pairs about Boolean variables as string and their corresponding order indices.
        boolean_variables_str_and_ordered_indices_int_dict = {}
    
    # If the argument explicitly provides the order of Boolean variables:
    else:

        # Initialize a Boolean variable to denote that the order of Boolean variables does not need to be checked.
        need_boolean_variables_str_and_ordered_indices_int_dict_bool = False 
    
    # Initialize an integer to follow the index of the current Boolean variable.
    current_boolean_variable_index_int = 0

    # Open the file containing a general boolean network:
    with open(general_boolean_network_file_path_with_name_and_type_str, "r") as general_boolean_network_file:

        # Iterate each line in the file:
        for boolean_equation_str in general_boolean_network_file:

            # Delete the symbol of changing the line.
            boolean_equation_str = boolean_equation_str.strip()

            # If the line is empty or the format is not correct:
            if not boolean_equation_str or "=" not in boolean_equation_str:
                
                # No need to process this line.
                continue

            # Get the target Boolean variable.
            target_boolean_variable_str, _ = map(str.strip, boolean_equation_str.split("=", 1))

            # Add the current Boolean variable into the set.
            boolean_variables_str_set.add(target_boolean_variable_str)
            
            # If the argument does not explicitly provide the order of Boolean variables:
            if need_boolean_variables_str_and_ordered_indices_int_dict_bool:
                
                # Set the current index as the order of the current target Boolean variable.
                boolean_variables_str_and_ordered_indices_int_dict[target_boolean_variable_str] = current_boolean_variable_index_int
                
                # Increment the index of the current Boolean variables by 1.
                current_boolean_variable_index_int += 1

    # Initialize an empty dictionary to store corresponding callable Boolean expressions for each Boolean variable.
    boolean_variables_str_and_boolean_expressions_callable_dict = {}

    # Initialize an empty dictionary to store corresponding Boolean expressions as string for each Boolean variable.
    boolean_variables_str_and_boolean_expressions_str_dict = {}

    # Open the file containing a general Boolean network:
    with open(general_boolean_network_file_path_with_name_and_type_str, "r") as general_boolean_network_file:

        # Iterate each line in the file:
        for boolean_equation_str in general_boolean_network_file:

            # Delete the symbol of changing the line.
            boolean_equation_str = boolean_equation_str.strip()

            # If the line is empty or the format is not correct:
            if not boolean_equation_str or "=" not in boolean_equation_str:

                # No need to process this line.
                continue

            # Get the target Boolean variable and its Boolean expression.
            target_boolean_variable_str, boolean_expression_str = map(str.strip, boolean_equation_str.split("=", 1))

            # Add the key-value pair about Boolean variable and its corresponding Boolean expression into the dictionary.
            boolean_variables_str_and_boolean_expressions_str_dict[target_boolean_variable_str] = boolean_expression_str

            # Call the method to get tokens and indices of Boolean variables.
            boolean_expression_tokens_str_list, boolean_variables_str_and_indices_in_tokens_int_list_dict = convert_boolean_expression_to_tokens_and_indices(boolean_variables_str_set, boolean_expression_str)
            
            # Call the method to add the callable Boolean expression.
            boolean_variables_str_and_boolean_expressions_callable_dict[target_boolean_variable_str] = help_function_to_return_callable(boolean_expression_tokens_str_list, boolean_variables_str_and_indices_in_tokens_int_list_dict)

    # Return the dictionary containing key-value pairs about Boolean variables and their corresponding Boolean expressions.
    return boolean_variables_str_and_boolean_expressions_callable_dict, boolean_variables_str_and_boolean_expressions_str_dict, boolean_variables_str_and_ordered_indices_int_dict


def convert_boolean_expression_to_tokens_and_indices(boolean_variables_str_set: set[str], boolean_expression_str: str) -> (list[str], dict[str: list[int]]):
    """
        Convert a Boolean equation to tokens and indices of Boolean variables in it.
        
        Arguments:
            boolean_variables_str_set (set[str]).
                The set containing all Boolean variables.
            boolean_expression_str (str).
                The string containing a Boolean expression.
                
        Returns:
            (list[str]).
                The list containing tokens.
            (dict[str: list[int]]).
                The dictionary containing key-value pairs about Boolean variables and their corresponding indices in tokens as a list.
    """
    
    # Split the string based on spaces.
    boolean_expression_tokens_str_list = boolean_expression_str.split()

    # Remove '(' and ')' to get simplified tokens.
    simplified_boolean_expression_tokens_str_list = [boolean_expression_token_string.replace("(", "").replace(")", "") for boolean_expression_token_string in boolean_expression_tokens_str_list]

    # Initialize a dictionary to store corresponding indices for each Boolean variable.
    boolean_variables_str_and_indices_in_tokens_int_list_dict = {boolean_variable_str: [] for boolean_variable_str in boolean_variables_str_set}

    # Iterate each simplified token:
    for boolean_expression_token_string_index_int in range(len(simplified_boolean_expression_tokens_str_list)):

        # Get the current token.
        current_boolean_expression_token_str = simplified_boolean_expression_tokens_str_list[boolean_expression_token_string_index_int]

        # If the current token is a Boolean variable:
        if current_boolean_expression_token_str in boolean_variables_str_set:
            
            # Append the current index into the dictionary.
            boolean_variables_str_and_indices_in_tokens_int_list_dict[current_boolean_expression_token_str].append(boolean_expression_token_string_index_int)
    
    # Return tokens and indices of Boolean variables.
    return boolean_expression_tokens_str_list, boolean_variables_str_and_indices_in_tokens_int_list_dict


def help_function_to_return_callable(boolean_expression_tokens_str_list: list[str], boolean_variables_str_and_indices_in_tokens_int_list_dict: dict[str: list[int]]) -> Callable:
    """
        The function to return callable as Boolean expressions.

        Arguments:
            boolean_expression_tokens_str_list (list[str]).
                The list containing tokens of a Boolean expression.
            boolean_variables_str_and_indices_in_tokens_int_list_dict (dict[str: list[int]]).
                The dictionary containing key-value pairs about Boolean variables and their corresponding indices in the list of tokens.

        Returns:
            (Callable).
                The callable denoting a Boolean expression.
    """

    def replace_boolean_variables_string_with_assigned_boolean_values(boolean_variables_str_and_assigned_bool_dict: dict[str, bool]) -> str:
        """
            Replace Boolean variables in tokens with their corresponding Boolean values.

            Arguments:
                boolean_variables_str_and_assigned_bool_dict (dict[str, bool]).
                    The dictionary containing key-value pairs about Boolean variables and their corresponding Boolean values.

            Returns:
                (str).
                    The concatenated string of the Boolean expression after Boolean variables are replaced by their corresponding Boolean values.
        """

        # Copy the list of tokens of Boolean expression.
        copied_boolean_expression_tokens_str_list = boolean_expression_tokens_str_list[:]

        # Iterate each Boolean variable:
        for boolean_variable_str in boolean_variables_str_and_assigned_bool_dict:

            # Iterate each index of this current Boolean variable to replace:
            for boolean_variable_str_index_in_tokens_int in boolean_variables_str_and_indices_in_tokens_int_list_dict[boolean_variable_str]:

                # Replace the current Boolean variable with its assigned Boolean values.
                copied_boolean_expression_tokens_str_list[boolean_variable_str_index_in_tokens_int] = copied_boolean_expression_tokens_str_list[boolean_variable_str_index_in_tokens_int].replace(boolean_variable_str, str(boolean_variables_str_and_assigned_bool_dict[boolean_variable_str]))

        # Concatenate all string in the copied list.
        return " ".join(copied_boolean_expression_tokens_str_list)

    # Return the callable as the Boolean expression.
    return replace_boolean_variables_string_with_assigned_boolean_values
