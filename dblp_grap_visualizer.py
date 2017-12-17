import networkx as nx
import matplotlib.pyplot as plt

class dblpGraphVisualizer():

    def draw_graph(self, dblpGraph):

        plt.figure(3,figsize=(10,10))

        pos=nx.spring_layout(dblpGraph) # positions for all nodes

        #drawing node
        nx.draw_networkx_nodes(dblpGraph, pos,
                               nodelist=author_node_list,
                               node_color='b',
                               node_size=100,
                               alpha=0.8)

        nx.draw_networkx_nodes(dblpGraph, pos,
                               nodelist=paper_node_list,
                               node_color='r',
                               node_size=100,
                               alpha=0.8)

        nx.draw_networkx_nodes(dblpGraph, pos,
                               nodelist=venue_node_list,
                               node_color='g',
                               node_size=100,
                               alpha=0.8)

        #drawing edge with label
        edge_labels = nx.get_edge_attributes(dblpGraph,'relation_type')
        nx.draw_networkx_edge_labels(dblpGraph, pos,
                                     font_size=5,
                                     labels = edge_labels)