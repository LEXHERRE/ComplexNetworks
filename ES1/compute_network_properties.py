# In order to understand how the code works, it is a good idea to check the
# final section of the file that starts with
#   if __name__ == '__main__'
#
# Your task is essentially to replace all the parts marked as TODO or as
# instructed through comments in the functions, as well as the filenames
# and labels in the main part of the code which can be found at the end of
# this file.
#
# The raise command is used to help you out in finding where you still need to
# write your own code. When you successfully modified the code in that part,
# remove the `raise` command.
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# ====================== FUNCTIONS USED BY THE MAIN CODE ===================
#
# ====================== FOR THE MAIN CODE SCROLL TO THE BOTTOM ============


###############################################################
# Code that is given to you, and does not need to be modified #
###############################################################

def plot_distribution(y_values, x_values, style, x_label, y_label):
    """
    Plots the pre-calculated distribution y(x)
    Returns the figure object

    Parameters
    ----------
    y_values: list
        list of values corresponding to the pre-calculated distribution y(x)
    x_values: list
        the x values for plotting
    style: str
        style of the visualization ('bar' or 'logplot')
    x_label: str
        label of the x axis of the figure
    y_label: str
        label of the y axis of the figure
    """

    # If you are new to matplotlib and want to learn how it works, please read the comments below.
    # The logic is fairly similar to Matlab (also if you use Matlab's handles which are figure objects here)
    # We will use two objects: figure object fig is the whole canvas (or "window");
    # and ax is the pair of axes inside fig where your graph will be plotted.
    #
    # If *very* interested in how all this works, see https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure
    # and https://matplotlib.org/api/axes_api.html

    fig = plt.figure() # Creates a new figure canvas for the plot and returns the object as fig
    ax = fig.add_subplot(111) # Creates a new axis object (ax) in the figure fig. The add_subplot(111) means adding the first subplot in an 1x1 grid of subplots; if you'd like to create the first of say four (2x2), you would say add_subplot(221)
    if style == 'bar': # for plotting a bar chart
        offset = 0.5
        if mpl.__version__[0] == "2":
            # fix for the different api in matplotlib 2.X
            offset = 0
        ax.bar(np.array(x_values) - offset, y_values, width=0.5) # plots a bar chart in axes ax with xvalues-offset as the x axis values and y_values as bar heights
    elif style == 'logplot': # for plotting on double log axes
        ax.loglog(x_values, y_values, 'k', marker='.') # plots a double log plot in axes ax, with black ('k') dots ('.')
    ax.set_xlabel(x_label) # sets the label of the x axis
    ax.set_ylabel(y_label) # sets the label of the y axis

    return fig # Returns the figure object for showing or saving or both

def visualize_network(network, figure_title):
    """
    Visualizes network "network" with networkx, using nx.draw().
    Returns a figure object.

    Parameters
    ----------
    network: a networkx Graph object
    figure_title: title of the figure

    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    nx.draw(network) # networkx command for drawing the network
    ax.set_title(figure_title) # sets the title for the figure

    return fig

def calculate_and_plot_discrete_distribution(input_list, x_label, y_label):
    """
    Calculates and visualizes the discrete probability distribution of a variable
    whose values are given in input_list and returns the figure object

    Parameters
    ----------
    input_list: list
        a list of the variable values, e.g. node degrees
    x_label: str
        label of the x axis of the figure
    y_label: str
        label of the y axis of the figure

    Returns
    -------
    Nothing
    """
    assert len(input_list) > 0, "The input list should not be empty!"
    # Calculate the distribution:
    # np = NumPy, we use the ready-made function bincount that counts the number of non-negative integers
    # in the input_list, up to the max value in the input list, and returns an array of counts
    distribution = np.bincount(input_list)
    n = len(input_list)
    # Normalize:
    distribution = distribution / float(n)
    # Visualize:
    min_range = 0
    max_range = max(input_list) + 1
    x_values = list(range(min_range, max_range)) # range(i,j) gives an iterator from i to j, list(range(i,j)) makes a list out of it.

    fig = plot_distribution(distribution, x_values, 'bar', x_label, y_label) # uses the function defined above

    return fig

def cdf(input_list):
    """
    Calculates the cumulative distribution function of input_list; cdf(k) = p that value smaller than k

    Parameters
    ----------
    input_list : list
        a list of numbers whose frequencies are used to compute the cdf

    Returns
    -------
    x_points: the values for which the cdf is computed
    cdf: np.array
        cdf for the above values
    """
    input_array = np.array(input_list)
    x_points = np.unique(input_array) # np.unique gives back a sorted list of unique values in input_array
    cdf = []
    normalizer=float(input_array.size) # input_array.size is the same as len(input_array)

    for x in x_points:

        cdf.append((input_array[np.where(input_array < x)].size)/normalizer) # appends the share of entries in input_list with values < x

    return (x_points, np.array(cdf))

######################################################
# Starting from here you might need to edit the code #
######################################################



def density(network):
    """
    Calculates the network edge density: D = 2*m / n(n-1) where m=# of edges, n=# of nodes

    Parameters
    ----------
    network: a NetworkX graph object

    Returns
    -------
    D: network edge density
    """
    # YOUR CODE HERE
    E = nx.number_of_edges(network)
    V = nx.number_of_nodes(network)

    D = 2*E/(V*(V-1))

    return D


def get_degrees(network):
    """
    Returns a list of the degrees of all nodes in the network.

    Parameters
    ----------
    network: a NetworkX graph object

    Returns
    -------
    degrees: list
        degrees of all network node
    """
    degrees = [] # empty list
    # YOUR CODE HERE
    for (v) in network.nodes():
        degrees.append(len(list(network.neighbors(v))))
    #TODO: Fill in code to compute node degrees
    # Hint: loop over all nodes, and append the degree of each node
    # to the list 'degrees' by computing the number of neighbors each
    # node has
    return degrees

def load_network(network_fname):
    """
    A function for loading a network from an edgelist (.edg) file.

    Parameters
    ----------
    network_fname: full or relative path (including file name) of the .edg file

    Returns
    -------
    network: the loaded network as NetworkX Graph() object
    """
    # YOUR CODE HERE
    net = nx.read_weighted_edgelist(network_fname)
    # A function that reads an edge file where the edges are weighted (here, with all weights = 1.0).

    # The following two assertion statements stops the execution of
    # this program if the network is not correctly loaded:
    assert net is not None, "network was not correctly loaded"
    assert len(net) > 0, "network should contain at least one node"

    return net

# =============================== MAIN CODE BELOW ======================================

# To create the results asked in the exercise sheet,
# run this file in the terminal by typing
#   python compute_network_properties.py

if __name__ == '__main__':
    # Problem a)

    network_fname = './karate_club_network_edge_file.edg'
    network = load_network(network_fname)


    figure_title = 'The Karate Club network'
    fig = visualize_network(network, figure_title)

    figure_fname = 'karate-club-network.pdf'
    fig.savefig(figure_fname)

    ## Problem b):
    D_own = density(network)
    D_nx = nx.density(network)
    print('D from self-written algorithm: ' + str(D_own))
    print('D from NetworkX function: ' + str(D_nx))

    # Problem c)
    # YOUR CODE HERE
    l_nx = nx.average_shortest_path_length(network)
    assert l_nx is not None, "Avg. path length has not been computed"
    print('<l> from NetworkX function: ' + str(l_nx))


    ## Problem d):
    C_nx = nx.average_clustering(network, count_zeros=True)
    ## The parameter count_zeros is set to True to include nodes with C=0
    ## into the average:
    print('C from NetworkX function: ' + str(C_nx))


    # Problem e)
    # YOUR CODE HERE
    degree_distribution_x_label = 'Node degree'
    degree_distribution_y_label = '# nodes'

    degrees = get_degrees(network)
    fig = calculate_and_plot_discrete_distribution(
        degrees,
        degree_distribution_x_label,
        degree_distribution_y_label
    )

    degree_distribution_fig_fname = 'karate-club-degree-dist.pdf'
    fig.savefig(degree_distribution_fig_fname)

    # YOUR CODE HERE
    #TODO: set correct labels for the 1-CDF
    cdf_x_label = 'Degree k'
    cdf_y_label = '1-CDF(k)'

    cdf_x_values, cdf_vals = cdf(degrees)
    fig = plot_distribution(1-cdf_vals, cdf_x_values, 'logplot',
                           cdf_x_label, cdf_y_label) # 1-cdf is the so-called complementary cumulative distribution.

    ccdf_fig_fname = 'karate-club-degree-1-cdf.pdf'
    fig.savefig(ccdf_fig_fname)
