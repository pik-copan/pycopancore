
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
                 layout=nx.spring_layout, ax=None, node_positions=None):
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

        interconnecting graphs: list of N-1 networkx.Graph objects
            List of graphs, one for each layer connection.

        value_arrays: array of N arrays for each N graphs (not interconnecting !)
            with binary values that can be used for state plotting

        node_labels : dict node ID : str label or None (default None)
            Dictionary mapping nodes to labels.
            If None is provided, nodes are not labelled.

        layout_func : function handle (default networkx.spring_layout)
            Function used to compute the layout.

        ax : mpl_toolkits.mplot3d.Axes3d instance or None (default None)
            The axis to plot to. If None is given, a new figure and a new axis are created.

        node_posistions: in case they should stay the same
        """

        # book-keeping
        self.graphs = graphs
        self.connecting_graphs = connecting_graphs
        self.total_layers = len(graphs)
        self.value_arrays = value_arrays
        self.node_labels = node_labels
        self.layout = layout
        self.node_positions = node_positions

        if ax:
            self.ax = ax
        else:
            fig = plt.figure()
            self.ax = fig.add_subplot(111, projection='3d')

        # create internal representation of nodes and edges
        self.get_nodes()
        self.get_edges_within_layers()
        self.get_edges_between_layers()

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

        composition = self.graphs[0]
        for index, h in enumerate(self.graphs[1:]):
            composition = nx.compose(composition, h)
            composition = nx.compose(composition, self.connecting_graphs[index])

        pos = self.layout(composition, *args, **kwargs)

        self.node_positions = dict()
        for z, g in enumerate(self.graphs):
            self.node_positions.update({(node, z) : (*pos[node], z) for node in g.nodes()})

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
                ax.text(*self.node_positions[(node, z)], node_labels[node], *args, **kwargs)


    def draw(self):

        self.draw_edges(self.edges_within_layers,  color='k', alpha=0.3, linestyle='-', zorder=2)
        self.draw_edges(self.edges_between_layers, color='k', alpha=0.3, linestyle='--', zorder=2)

        # for different plotstyles for different layers:
        marker_map = ["^", "o"]
        size_map = [150, 300]

        for z in range(self.total_layers):
            self.draw_plane(z, alpha=0.2, zorder=1)
            if self.value_arrays:
                color_map = []
                for v in self.value_arrays[z]:
                    if v:
                        color_map.append("crimson")
                    else:
                        color_map.append("navy")
                self.draw_nodes([node for node in self.nodes if node[1] == z], color=color_map, s=size_map[z], zorder=3, marker=marker_map[z])
            else:
                self.draw_nodes([node for node in self.nodes if node[1] == z], s=200, zorder=3)

        if self.node_labels:
            self.draw_node_labels(self.node_labels,
                                  self.ax,
                                  horizontalalignment='center',
                                  verticalalignment='center',
                                  zorder=100)

        self.ax.grid(False)
        # self.ax.set_xlabel("")
