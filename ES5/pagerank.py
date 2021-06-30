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
from __future__ import print_function
import time
import datetime

import numpy as np
import matplotlib as mpl
import matplotlib.pylab as plt
import networkx as nx

# ====================== FUNCTIONS USED BY THE MAIN CODE ===================
#
# ====================== FOR THE MAIN CODE SCROLL TO THE BOTTOM ============

###############################################################
# Code that is given to you, and does not need to be modified #
###############################################################

def add_colorbar(cvalues, cmap='OrRd', cb_ax=None):
    """
    Add a colorbar to the axes.

    Parameters
    ----------
    cvalues : 1D array of floats

    """
    eps = np.maximum(0.0000000001, np.min(cvalues)/1000.)
    vmin = np.min(cvalues) - eps
    vmax = np.max(cvalues)
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    scm = mpl.cm.ScalarMappable(norm, cmap)
    scm.set_array(cvalues)
    if cb_ax is None:
        plt.colorbar(scm)
    else:
        cb = mpl.colorbar.ColorbarBase(cb_ax, cmap=cmap, norm=norm, orientation='vertical')

######################################################
# Starting from here you might need to edit the code #
######################################################

def pageRank(network, d, n_steps):
    """
    Returns the PageRank value, calculated using a random walker, of each
    node in the network. The random walker teleports to a random node with
    probability 1-d and with probability d picks one of the neighbors of the
    current node.

    Parameters
    -----------
    network : a networkx graph object
    d : damping factor of the simulation
    n_steps : number of steps of the random walker

    Returns
    --------
    page_rank: dictionary of node PageRank values (fraction of time spent in
               each node)
    """

    # Initializing PageRank dictionary:
    pageRank = {}
    nodes = list(network.nodes())

    # YOUR CODE HERE
    #TODO: write code for calculating PageRank of each node
    # 1) Initialize PageRank of each node to 0
    # 2) Pick a random starting point for the random walker (Hint: np.random.choice)
    # 3) Random walker steps, at each step:
    #   1) Increase the PageRank of current node by 1
    #   2) Check if the random walker will teleport or go to a neighbor
    #   3) Pick the next node either randomly or from the neighbors
    #   4) Update the current node variable to point to the next node
    # 4) Repeat random walker steps 1-4 n_steps times
    # 5) Normalize PageRank by n_steps
    pageRank = dict.fromkeys(nodes, 0)
    randWalker = np.random.choice(nodes)

    for _ in range(n_steps):
        pageRank[randWalker]+=1

        if d < np.random.rand():
            randWalker = np.random.choice(nodes)
        else:
            neighbors = list(nx.neighbors(network, randWalker))
            randWalker = np.random.choice(neighbors)

    pageRank = {k: v / n_steps for k, v in pageRank.items()}
    return pageRank

def pagerank_poweriter(g, d, iterations):
    """
    Uses the power iteration method to calculate PageRank value for each node
    in the network.

    Parameters
    -----------
    g : a networkx graph object
    d : damping factor of the simulation
    iterations : number of iterations to perform

    Returns
    --------
    pr_new : dict where keys are nodes and values are PageRank values
    """
    print("Running function for obtaining PageRank by power iteration...")
    # YOUR CODE HERE
    #TODO: write code for calculating power iteration PageRank
    # Some pseudocode:
    # 1) Create a PageRank dictionary and initialize the PageRank of each node
    #    to 1/n where n is the number of nodes.
    # 2) For each node i, find nodes having directed link to i and calculate
    #    sum(x_j(t-1)/k_j^out) where the sum is across the node's neighbors
    #    and x_j(t-1) is the PageRank of node  .
    # 3) Update each node's PageRank to (1-d)*1/n + d*sum(x_j(t-1)/k_j^out).
    # 4) Repeat 2-3 n_iterations times.
    nodes = list(g.nodes)
    n_nodes = len(nodes)
    pr_new = dict.fromkeys(nodes, 1/n_nodes)

    for _ in range(iterations):
        pr_old = pr_new.copy()
        for i in nodes:
            inEdges = g.in_edges(i)
            if len(inEdges) != 0:
                neighbors = [edge[0] for edge in inEdges]
                neighSum = sum([pr_old[j]/g.out_degree(j) for j in neighbors])
            else:
                neighSum = 0
            pr_new[i] = (1-d)/n_nodes + d*neighSum

            # sanity checks in each iteration:
            #print('PageRank sums to ')
            #print(sum(pr_new.values()))
            #print('PageRank difference since last iteration:')
            #print(sum([abs(pr_new[i]-pr_old[i]) for i in g]))
    return pr_new # TODO replace this!

def visualize_network(network, node_positions, cmap='OrRd',
                      node_size=3000, node_colors=[], with_labels=True, title=""):
    """
    Visualizes the given network using networkx.draw and saves it to the given
    path.

    Parameters
    ----------
    network : a networkx graph object
    node_positions : a dict of positions of nodes, obtained by e.g. networkx.graphviz_layout
    cmap : colormap
    node_size : int
    node_colors : a list of node colors
    with_labels : should node labels be drawn or not, boolean
    title: title of the figure, string
    """
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)
    if node_colors:
        #TODO: write code to visualize the networks with nodes colored by PageRank.
        # YOUR CODE HERE
        # use nx.draw and make use of parameters pos, node_color,
        # cmap, node_size and with_labels
        nx.draw(network, pos=node_positions, node_color=node_colors, cmap=cmap,
                node_size=node_size, with_labels=with_labels)
        add_colorbar(node_colors)
    else:
        #TODO: write code to visualize the networks without node coloring.
        # YOUR CODE HERE
        # use nx.draw and make use of parameters pos, cmap, node_size and
        # with_labels
        nx.draw(network, pos=node_positions, cmap=cmap, node_size=node_size,
                with_labels=with_labels)
        #pass # TODO: Remove this
    ax.set_title(title)
    plt.tight_layout()

    return fig

def investigate_d(network, ds, colors, n_steps):
    """
    Calculates PageRank at different values of the damping factor d and
    visualizes and saves results for interpretation

    Parameters
    ----------
    network : a NetworkX graph object
    ds : a list of d values
    colors : visualization color for PageRank at each d, must have same length as ds
    n_steps : int; number of steps taken in random walker algorithm
    """
    #import pdb; pdb.set_trace()
    n_nodes = len(network.nodes())
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #TODO: write a for loop to obtain node PageRank values at each d and to plot the PageRank.
    # YOUR CODE HERE
    # use zip to loop over ds and colors at once
    for d,c in zip(ds,colors):
        pr = pageRank(network,d,n_steps)
        ordered_pr=np.zeros(n_nodes)
        for node in pr:
            ordered_pr[int(node)] = pr[node]
        plt.plot(ordered_pr,label=np.round(d,2),color=c)
    ax.set_xlabel(r'Node index')
    ax.set_ylabel(r'PageRank')
    ax.set_title(r'PageRank with different damping factors')
    ax.legend(loc=0)
    plt.tight_layout

    return fig

# =========================== MAIN CODE BELOW ==============================

if __name__ == '__main__':

    #TODO: replace, set the correct path to the network
    network_path = './pagerank_network.edg'

    network =  nx.read_edgelist(network_path, create_using=nx.DiGraph())

    # Visualization of the network (note that spring_layout
    # is intended to be used with undirected networks):
    node_positions = nx.spring_layout(network.to_undirected())
    cmap = 'OrRd'
    node_size = 3000

    fig=visualize_network(network, node_positions, cmap=cmap, node_size=node_size, title="Network")

    fig.savefig('./network_visualization.pdf')

    nodes = network.nodes()
    n_nodes = len(nodes)
    # PageRank with self-written function
    # YOUR CODE HERE
    n_steps = 10000 # TODO: replace: set a reasonable n_steps
    d = 0.85 # TODO: replace: set a reasonable d; nx.pagerank zuses d = 0.85
    pageRank_rw = pageRank(network, d, n_steps)

    # Visualization of PageRank on network:
    node_colors = [pageRank_rw[node] for node in nodes]

    fig = visualize_network(network, node_positions, cmap=cmap, node_size=node_size,
                            node_colors=node_colors, title="PageRank random walker")

    fig.savefig('./network_visualization_pagerank_rw.pdf')

    # PageRank with networkx:
    pageRank_nx = nx.pagerank(network)

    # Visualization to check that results from own function and nx.pagerank match:

    pageRank_rw_array = np.zeros(n_nodes)
    pageRank_nx_array = np.zeros(n_nodes)
    for node in nodes:
        pageRank_rw_array[int(node)] = pageRank_rw[node]
        pageRank_nx_array[int(node)] = pageRank_nx[node]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(range(0, n_nodes), pageRank_rw_array, 'k+', label=r'Random walker')
    plt.plot(range(0, n_nodes), pageRank_nx_array, 'rx', label='networkx')
    ax.set_xlabel(r'Node index')
    ax.set_ylabel(r'PageRank')
    ax.set_title(r'PageRank with different methods')
    ax.legend(loc=0)
    plt.tight_layout()

    fig.savefig('./network_visualization_pagerank_nx.pdf')

    # PageRank with power iteration
    n_iterations = 10
    pageRank_pi = pagerank_poweriter(network, d, n_iterations)

    # Visualization of PageRank by power iteration

    node_colors = [pageRank_pi[node] for node in nodes]
    fig = visualize_network(network, node_positions, cmap=cmap, node_size=node_size,
                            node_colors=node_colors, title="PageRank power iteration")

    fig.savefig('./network_visualization_pagerank_pi.pdf')


    # Investigating the running time of the power iteration function
    num_tests = 3
    # YOUR CODE HERE
    n_nodes = 10**4
    k5net = nx.directed_configuration_model(n_nodes*[5],n_nodes*[5],create_using=nx.DiGraph())
                            # TODO: replace with a test network of suitable size
    # TODO: Print results: how many seconds were taken for the test network of
    # 10**4 nodes, how many hours would a 26*10**6 nodes network take?
    # Run num_tests times and use the average or minimum running time in your calculations.

    sum_time = 0
    for i in range(num_tests):
        print('Test ' + str(i+1) + ':')
        start_time = time.time()
        pagerank_poweriter(k5net,d,n_iterations)
        sum_time += time.time()-start_time
    avg_time = sum_time/num_tests

    print('Power iteration function (10**4 nodes): '+ str(avg_time) +' seconds')
    N_nodes = 26*10**6
    estimated_time = avg_time/n_nodes*N_nodes/3600
    print('Power iteration function (26*10**6 nodes): '+ str(estimated_time) +' hours')
    print()

    # Investigating the running time of the random walker function
    n_nodes = 10**4
    k5net = nx.directed_configuration_model(n_nodes*[5],n_nodes*[5],create_using=nx.DiGraph())

    # YOUR CODE HERE
    n_steps = 10**6 # TODO: set such number of steps that each node gets visited on average 1000 times

    for i in range(num_tests):
        print('Test ' + str(i+1) + ':')
        start_time = time.time()
        pageRank(k5net,d,n_steps)
        sum_time += time.time()-start_time
    avg_time = sum_time/num_tests

    print('Random walker function (10**4 nodes): '+ str(avg_time) +' seconds')
    N_nodes = 26*10**6
    estimated_time = avg_time/n_nodes*N_nodes/3600
    print('Random walker function (26*10**6 nodes): '+ str(estimated_time) +' hours')

    # Investigating effects of d:
    ds = np.arange(0, 1.2, 0.2)
    colors = ['b', 'r', 'g', 'm', 'k', 'c']
    # YOUR CODE HERE
    n_steps = 10000
    fig = investigate_d(network, ds, colors, n_steps)
    fig.savefig('./effects_of_d_pageRank.pdf')
