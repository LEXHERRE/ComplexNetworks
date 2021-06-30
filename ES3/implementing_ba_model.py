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
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import binned_statistic

# ====================== FUNCTIONS USED BY THE MAIN CODE ===================
#
# ====================== FOR THE MAIN CODE SCROLL TO THE BOTTOM ============

def log_bins(max_degree):
    # have the number of logbins such that there are 10 bins per decade

    num_logbins = int(np.log10(1.5 * max_degree) - np.log10(1.5)) * 10

    # generate log bins from k=1.5 to k=1.5*max(degree)
    bins = np.logspace(
        np.log10(1.5), np.log10(1.5 * max_degree), num_logbins)

    return bins

def ba_network(N, m, seedsize=3):
    # Generate initial small seed network (clique of seedsize nodes)
    net = nx.complete_graph(seedsize)

    # YOUR CODE HERE
    # TODO: Grow the network here
    nodes = list(net.nodes)*(seedsize-1)
    for u in range(seedsize, N):
        edges = np.random.choice(nodes,m,replace=False)
        net.add_edges_from(zip([u]*m, edges))

        nodes.extend(edges)
        nodes.extend([u]*m)

    return net

# =========================== MAIN CODE BELOW ==============================

if __name__ == "__main__":
    np.random.seed(42)

    # part a
    fig = plt.figure()
    ax = fig.add_subplot(111)

    N = 200
    m = 1
    net = ba_network(N, m)
    nodes = net.nodes()
    degrees_dict = nx.degree(net)
    degrees = [degrees_dict[node] for node in nodes]

    print("The maximum degree is: ", max(degrees))
    print("The total number of edges is: ", len(net.edges()))

    nx.draw_spring(
        net, node_size=100, node_color=degrees, cmap='autumn',
        vmin=np.min(degrees), vmax=np.max(degrees))
    ax.set_aspect('equal')

    figure_filename = 'BA_visualized.pdf'


    fig.savefig(figure_filename)
    # or just use plt.show() and save manually

    # part b
    N = 10000
    m = 2
    net = ba_network(N, m)
    degrees = [deg for _, deg in nx.degree(net)]
    # if you are using an older version of networkx where the return value of nx.degree is a dict instead of
    # a DegreeView, you will get a type error from the above line. To fix, change it to:
    # degrees = list(nx.degree(net).values())

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # so use np.histogram to get histogram and bin edges
    bins = log_bins(max(degrees))
    pk, bin_edges = np.histogram(degrees, bins=bins, density=True)

    bincenters, _, _ = binned_statistic(
        degrees, degrees, statistic='mean', bins=bins)
    ax.set_xlabel('Degree k')
    ax.set_ylabel('P(k)')

    ax.loglog(bincenters, pk, 'ro', label='Simulated')
    ax.loglog(bins, 2 * 2 * (2 + 1) /
              (bins * (bins + 1) * (bins + 2)),
              label='Theoretical')

    ax.legend()

    figure_filename = 'BA_degree_distribution.pdf'


    fig.savefig(figure_filename)
    # or just use plt.show() and save manually
