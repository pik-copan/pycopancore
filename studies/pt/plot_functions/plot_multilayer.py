
"""
Plot multi-graphs in 3D.
Based upon https://stackoverflow.com/questions/60392940/multi-layer-graph-in-networkx
and adjusted for personal needs.
"""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# TODO: get groups to be plotted in middle of inds for looks
# TODO: label the layers, make dots smaller and maybe different shapes for groups/inds?
# TODO: think about illustrating cognitive dissonance

class LayeredNetworkGraph(object):

    def __init__(self, graphs, connecting_graphs, value_arrays=None, node_labels=None,
                 layout=nx.spring_layout, ax=None, node_positions=None, scaling_factor=None, highlight_cluster=None):
        """Given an ordered list of graphs [g1, g2, ..., gn] that represent
        different layers in a multi-layer network, plot the network in
        3D with the different layers separated along the z-axis.

        Within a layer, the corresponding graph defines the connectivity.

        Between layers, nodes in subsequent layers are connected if
        they share an edge in the connecting graph i1.

        E.g. LayeredNetworkGraph([g1, g2], [i1])

        Arguments:
        ----------
        graphs : list of N networkx.Graph objects
            List of graphs, one for each layer.

        interconnecting graphs: list of N-1 networkx.DiGraph objects
            List of DiGraphs, one for each layer connection.

        value_arrays: array of N arrays for each N graphs (not interconnecting !)
            with binary values that can be used for state plotting

        node_labels : dict node ID : str label or None (default None)
            Dictionary mapping nodes to labels.
            If None is provided, nodes are not labelled.

        layout_func : function handle (default networkx.spring_layout)
            Function used to compute the layout.

        ax : mpl_toolkits.mplot3d.Axes3d instance or None (default None)
            The axis to plot to. If None is given, a new figure and a new axis are created.

        node_posistions: self.nodepositions object or None
        in case they should stay the same

        scaling_factor: float or None
        for many nodes plot gets too crowded, use: k=0.3*1/np.sqrt(400)

        highlight_cluster: str = "Sus" or str = "Nonsus" or None
        if "Sus" (or "Nonsus") links between sustainable (and nonsustainable respectively) groups and sustainable (")
        individuals are highlighted in the respective colour
        """

        # book-keeping
        self.graphs = graphs
        self.connecting_graphs = connecting_graphs
        self.total_layers = len(graphs)
        self.value_arrays = value_arrays
        self.node_labels = node_labels
        self.layout = layout
        self.node_positions = node_positions
        self.scaling_factor = scaling_factor
        self.highlight_cluster = highlight_cluster

        if ax:
            self.ax = ax
        else:
            fig = plt.figure()
            self.ax = fig.add_subplot(111, projection='3d')

        # create internal representation of nodes and edges
        self.get_nodes()
        self.get_edges_within_layers()
        self.get_edges_between_layers()
        if self.highlight_cluster is not None:
            self.get_colored_edges_within_layers(which_edges=self.highlight_cluster)
            self.get_colored_edges_between_layers(which_edges=self.highlight_cluster)

        # compute layout and plot
        if not self.node_positions:
            self.get_node_positions()
        self.draw()


    def get_nodes(self):
        """Construct an internal representation of nodes with the format (node ID, layer)."""
        self.nodes = []
        for z, g in enumerate(self.graphs):
            self.nodes.extend([(node, z) for node in g.nodes()])


    def get_edges_within_layers(self):
        """Remap edges in the individual layers to the internal representations of the node IDs."""
        self.edges_within_layers = []
        for z, g in enumerate(self.graphs):
            self.edges_within_layers.extend([((source, z), (target, z)) for source, target in g.edges()])


    def get_edges_between_layers(self):
        """Determine edges between layers. Nodes in subsequent layers (e.g. g1, g2) are
        thought to be connected if they share an edge in the connecting graph (i1)."""
        self.edges_between_layers = []
        for z1, g in enumerate(self.graphs[:-1]):
            z2 = z1 + 1
            h = self.graphs[z2]
            i = self.connecting_graphs[z1]
            for n1 in g:
                for n2 in h:
                    if n2 in list(i.successors(n1)):
                        self.edges_between_layers.extend([((n1, z1), (n2, z2))])


    def get_colored_edges_within_layers(self, which_edges):
        """Determine colored edges between layers. Nodes in subsequent layers (e.g. g1, g2) are
        thought to be connected if they share an edge in the connecting graph (i1).
        which_edges = self.highlight_cluster
        """
        self.colored_edges_within_layers = []
        if which_edges == "Sus":
            for z, g in enumerate(self.graphs):
                for index_1, n1 in enumerate(g):
                    for index_2, n2 in enumerate(g):
                        if n2 in list(g.neighbors(n1)) and self.value_arrays[z][index_1] == self.value_arrays[z][index_2] == 1:
                            self.colored_edges_within_layers.extend([((n1, z), (n2, z))])
        elif which_edges == "Unsus":
            for z, g in enumerate(self.graphs):
                for index_1, n1 in enumerate(g):
                    for index_2, n2 in enumerate(g):
                        if n2 in list(g.neighbors(n1)) and self.value_arrays[z][index_1] == self.value_arrays[z][index_2] == 0:
                            self.colored_edges_within_layers.extend([((n1, z), (n2, z))])
        else:
            print("Error. Wrong highlight_cluster keyword given. Use \"Sus\" or \"Unsus\".")


    def get_colored_edges_between_layers(self, which_edges):
        """Determine colored edges between layers. Nodes in subsequent layers (e.g. g1, g2) are
        thought to be connected if they share an edge in the connecting graph (i1).
        which_edges = self.highlight_cluster
        """
        self.colored_edges_between_layers = []
        if which_edges == "Sus":
            for z1, g in enumerate(self.graphs[:-1]):
                z2 = z1 + 1
                h = self.graphs[z2]
                i = self.connecting_graphs[z1]
                for index_g, n1 in enumerate(g):
                    for index_h, n2 in enumerate(h):
                        if n2 in list(i.successors(n1)) and self.value_arrays[z1][index_g] == self.value_arrays[z2][index_h] == 1: # only works for two graphs yet
                            self.colored_edges_between_layers.extend([((n1, z1), (n2, z2))])
        elif which_edges == "Unsus":
            for z1, g in enumerate(self.graphs[:-1]):
                z2 = z1 + 1
                h = self.graphs[z2]
                i = self.connecting_graphs[z1]
                for index_g, n1 in enumerate(g):
                    for index_h, n2 in enumerate(h):
                        if n2 in list(i.successors(n1)) and self.value_arrays[z1][index_g] == self.value_arrays[z2][index_h] == 0:
                            self.colored_edges_between_layers.extend([((n1, z1), (n2, z2))])
        else:
            print("Error. Wrong highlight_cluster keyword given. Use \"Sus\" or \"Unsus\".")
    def get_node_positions(self, *args, **kwargs):
        """Get the node positions in the layered layout."""
        # What we would like to do, is apply the layout function to a combined, layered network.
        # However, networkx layout functions are not implemented for the multi-dimensional case.
        # Futhermore, even if there was such a layout function, there probably would be no straightforward way to
        # specify the planarity requirement for nodes within a layer.
        # Therefore, we compute the layout for the full network in 2D, and then apply the
        # positions to the nodes in all planes.
        # For a force-directed layout, this will approximately do the right thing.
        # TODO: implement FR in 3D with layer constraints.

        # composition = self.graphs[0]
        # for index, h in enumerate(self.graphs[1:]):
        #     composition = nx.compose(composition, h)
        #     composition = nx.compose(composition, self.connecting_graphs[index])
        #
        # pos = self.layout(composition, *args, **kwargs)
        # if self.layout == nx.spring_layout:
        #     pos = self.layout(composition, k=self.scaling_factor, *args, **kwargs)
        #
        # self.node_positions = dict()
        # for z, g in enumerate(self.graphs):
        #     self.node_positions.update({(node, z) : (*pos[node] * 100, z - 0.25) for node in g.nodes()})

        # try own scaling for two layers
        # pos_0 = nx.spring_layout(self.graphs[0], *args, **kwargs)
        pos_1 = nx.circular_layout(self.graphs[1], center=[0.5,0.5], scale = 0.25)
        # pos_0 = nx.spring_layout(self.graphs[0])
        pos_0 = nx.random_layout(self.graphs[0])
        node_positions1 = dict()
        node_positions2 = dict()
        node_positions1.update({(node, 0) : (*pos_0[node], 0) for node in self.graphs[0].nodes()})
        node_positions2.update({(node, 1) : (*pos_1[node], 1) for node in self.graphs[1].nodes()})
        self.node_positions = node_positions1 | node_positions2 # cool new operator, joins both dicts

    def save_node_positions(self):
        return self.node_positions

    def draw_nodes(self, nodes, *args, **kwargs):
        x, y, z = zip(*[self.node_positions[node] for node in nodes])
        self.ax.scatter(x, y, z, *args, **kwargs)


    def draw_edges(self, edges, *args, **kwargs):
        segments = [(self.node_positions[source], self.node_positions[target]) for source, target in edges]
        line_collection = Line3DCollection(segments, *args, **kwargs)
        self.ax.add_collection3d(line_collection)


    def get_extent(self, pad=0.1):
        xyz = np.array(list(self.node_positions.values()))
        xmin, ymin, _ = np.min(xyz, axis=0)
        xmax, ymax, _ = np.max(xyz, axis=0)
        dx = xmax - xmin
        dy = ymax - ymin
        return (xmin - pad * dx, xmax + pad * dx), \
            (ymin - pad * dy, ymax + pad * dy)


    def draw_plane(self, z, *args, **kwargs):
        (xmin, xmax), (ymin, ymax) = self.get_extent(pad=0.1)
        u = np.linspace(xmin, xmax, 10)
        v = np.linspace(ymin, ymax, 10)
        U, V = np.meshgrid(u ,v)
        W = z * np.ones_like(U) * 0.1
        self.ax.plot_surface(U, V, W, *args, **kwargs)


    def draw_node_labels(self, node_labels, *args, **kwargs):
        for node, z in self.nodes:
            if node in node_labels:
                self.ax.text(*self.node_positions[(node, z)], node_labels[node], *args, **kwargs)


    def draw(self):
        self.draw_edges(self.edges_within_layers,  color='k', alpha=0.05, linestyle='-', zorder=2)
        self.draw_edges(self.edges_between_layers, color='k', alpha=0.05, linestyle='--', zorder=2)
        if self.highlight_cluster is not None:
            if self.highlight_cluster == "Sus":
                c_value = "blue"
            elif self.highlight_cluster == "Unsus":
                c_value = "red"
            self.draw_edges(self.colored_edges_within_layers, color=c_value, alpha=0.25, linestyle='-', zorder=2)
            self.draw_edges(self.colored_edges_between_layers, color=c_value, alpha=0.25, linestyle='-', zorder=2)

        # for different plotstyles for different layers:
        marker_map = ["^", "o"]
        # size_map = [150, 300]

        for z in range(self.total_layers): # i reverse the range, so that groups tend to be outside
            # self.draw_plane(z, alpha=0.2, zorder=1)
            if self.value_arrays:
                # make color map
                color_map = []
                for v in self.value_arrays[z]:
                    if v:
                        color_map.append("navy")
                    else:
                        color_map.append("crimson")
                # self.draw_nodes([node for node in self.nodes if node[1] == z], color=color_map, s=size_map[z], zorder=3, marker=marker_map[z])
                # without size map
                self.draw_nodes([node for node in self.nodes if node[1] == z], color=color_map, zorder=3, marker=marker_map[z], alpha=1)
            else:
                self.draw_nodes([node for node in self.nodes if node[1] == z], s=200, zorder=3)

        if self.node_labels:
            self.draw_node_labels(self.node_labels,
                                  self.ax,
                                  horizontalalignment='center',
                                  verticalalignment='center',
                                  zorder=100)

        self.ax.grid(False)
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.get_zaxis().set_visible(False)
        # self.ax.set_xlabel("")
