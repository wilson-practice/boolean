# Import to visualize.
import matplotlib.pyplot as plt

# Import to store values.
import numpy as np

# Import to create the directory.
import os

from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter


def visualize_belief_propagation_and_full_search(bp_float_1d_list: list[float], fs_float_1d_list: list[float], x_label_str: str = None, y_label_str: str = None, title_str: str = None, output_figure_path_with_name_but_without_type_str: str = None):
    """
        Given a 1-dimensional array about Belief Propagation and a 1-dimensional array about Full Search, visualize them into one figure.

        Arguments:
            bp_float_1d_list (list[float]).
                The 1-dimensional list containing Belief Propagation values.
            fs_float_1d_list (list[float]).
                The 1-dimensional list containing Full Search values.
            x_label_str (str).
                Default value is None.
                The string denoting the label of X-axis.
            y_label_str (str).
                Default value is None.
                The string denoting the label of Y-axis.
            title_str (str).
                Default value is None.
                The string denoting the title of the figure.
            output_figure_path_with_name_but_without_type_str (str).
                Default value is None.
                The string denoting the path to save this figure with name but without type.
    """

    # Set the size of the plot: 1900 * 1200.
    fig, ax = plt.subplots(figsize=(19, 12))

    # plot the two curves
    ax.plot(range(len(bp_float_1d_list)), bp_float_1d_list, marker="o", color="red", label="BP")
    ax.plot(range(len(fs_float_1d_list)), fs_float_1d_list, marker="o", color="green", label="FS")

    # Iterate each index:
    for index_int in range(len(bp_float_1d_list)):

        # If BP has a larger value:
        if bp_float_1d_list[index_int] > fs_float_1d_list[index_int]:

            # Set the current color as red.
            color_str = "red"

        # If BP does not have a larger value:
        else:

            # Set the current color as red.
            color_str = "green"

        # Visualize the line between two points.
        ax.plot([index_int, index_int], [bp_float_1d_list[index_int], fs_float_1d_list[index_int]], color=color_str, linewidth=2)

    # Show legends.
    ax.legend()

    # If the path to save the figure is not provided explicitly:
    if output_figure_path_with_name_but_without_type_str is None:

        # Show the figure directly.
        plt.show()

    # If the path to save the plot is provided explicitly:
    else:

        # Ensure the directory exists.
        os.makedirs(os.path.dirname(output_figure_path_with_name_but_without_type_str), exist_ok=True)

        # Save the figure.
        plt.savefig(output_figure_path_with_name_but_without_type_str)

        # Close the figure to free up memory.
        plt.close()


def plot_xy_points_with_diagonal_and_correlation(file_path):
    """
    File format:
        each row: y x
    """

    # load data
    data = np.loadtxt(file_path)

    Y = data[:, 0]
    X = data[:, 1]

    # Pearson correlation
    r = np.corrcoef(X, Y)[0, 1]

    fig, ax = plt.subplots(figsize=(6, 6))

    # hollow blue points
    ax.scatter(
        X,
        Y,
        facecolors='none',
        edgecolors='blue'
    )

    # equal axis scale
    ax.set_aspect('equal', adjustable='box')

    # plotting range
    vmin = min(X.min(), Y.min())
    vmax = max(X.max(), Y.max())

    # y = x line
    ax.plot(
        [vmin, vmax],
        [vmin, vmax],
        linestyle='--',
        color='black'
    )

    ax.set_xlabel("Full Search")
    ax.set_ylabel("BP")

    # show Pearson correlation
    ax.set_title(f"n = {len(data)} r = {r:.4f}")

    plt.show()

    return r


# def visualize_3d_landscape(keys_int_and_coordinates_float_1d_tuple_dict: dict[int: (float, float, float)], number_of_grids_in_one_side_int: int = 100, title_str: str = None, output_figure_path_with_name_but_without_type_str: str = None):
#     """
#          Visualize 3-dimensional landscape.
#
#          Arguments:
#              keys_int_and_coordinates_float_1d_tuple_dict (dict[int: (float, float, float)]).
#                 The dictionary containing key-value pairs about integral keys and their corresponding coordinates as a 1-dimensional tuple.
#              number_of_grids_in_one_side_int (int).
#                 Default value is 100.
#                 The integer denoting the number of grids in one side of the left or the right.
#              title_str (str).
#                 Default value is None.
#                 The string denoting the title of the figure.
#              output_figure_path_with_name_but_without_type_str (str).
#                 Default value is None.
#                 The string denoting the path to save this figure with name but without type.
#     """
#
#     # Set the size of the plot: 1900 * 1200.
#     fig, ax = plt.subplots(figsize=(19, 12))
#
#     # Add a subplot.
#     ax = fig.add_subplot(111, projection="3d")
#
#     # Get all X-coordinates.
#     x_coordinates_float_1d_array = np.array([keys_int_and_coordinates_float_1d_tuple_dict[key_int][0] for key_int in keys_int_and_coordinates_float_1d_tuple_dict])
#
#     # Get all Y-coordinates.
#     y_coordinates_float_1d_array = np.array([keys_int_and_coordinates_float_1d_tuple_dict[key_int][1] for key_int in keys_int_and_coordinates_float_1d_tuple_dict])
#
#     # Get all Z-coordinates.
#     z_coordinates_float_1d_array = np.array([keys_int_and_coordinates_float_1d_tuple_dict[key_int][2] for key_int in keys_int_and_coordinates_float_1d_tuple_dict])
#
#     # Get all X-coordinates of grids.
#     grids_x_coordinates_float_1d_array = np.linspace(x_coordinates_float_1d_array.min(), x_coordinates_float_1d_array.max(), number_of_grids_in_one_side_int)
#
#     # Get all Y-coordinates of grids.
#     grids_y_coordinates_float_1d_array = np.linspace(y_coordinates_float_1d_array.min(), y_coordinates_float_1d_array.max(), number_of_grids_in_one_side_int)
#
#     X, Y = np.meshgrid(grids_x_coordinates_float_1d_array, grids_y_coordinates_float_1d_array)
#
#     Z = griddata((x_coordinates_float_1d_array, y_coordinates_float_1d_array), z_coordinates_float_1d_array, (X, Y), method="cubic")
#     Z_nearest = griddata((x_coordinates_float_1d_array, y_coordinates_float_1d_array), z_coordinates_float_1d_array, (X, Y), method="nearest")
#     Z = np.where(np.isnan(Z), Z_nearest, Z)
#
#     # Smoothing.
#     Z = gaussian_filter(Z, sigma=3)
#
#     # Visualize the 3D landscape.
#     ax.plot_surface(X, Y, Z, cmap="viridis", linewidth=0, antialiased=True)
#
#     # If the title is provided explicitly:
#     if title_str is not None:
#
#         # Add the title. Set the size of its font.
#         ax.set_title(title_str, fontsize=15)
#
#     # If the path to save the figure is not provided explicitly:
#     if output_figure_path_with_name_but_without_type_str is None:
#
#         # Show the figure directly.
#         plt.show()
#
#     # If the path to save the plot is provided explicitly:
#     else:
#
#         # Ensure the directory exists.
#         os.makedirs(os.path.dirname(output_figure_path_with_name_but_without_type_str), exist_ok=True)
#
#         # Save the figure.
#         plt.savefig(output_figure_path_with_name_but_without_type_str)
#
#         # Close the figure to free up memory.
#         plt.close()