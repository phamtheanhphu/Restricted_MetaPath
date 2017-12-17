import networkx as nx
import matplotlib.pyplot as plt

dblpGraph = nx.DiGraph()


def file_to_dict(file_name):
    result = dict()
    f = open(file_name, 'r', encoding='utf-8')
    for line in f:
        splited = line.rstrip().split('\t')
        if splited[0] in result:
            result[splited[0]].append(splited[1])
        else:
            result.update({splited[0]: [splited[1]]})
    f.close()
    return result


def file_to_reverse_dict(file_name):
    result = dict()
    f = open(file_name, 'r', encoding='utf-8')
    for line in f:
        splited = line.rstrip().split('\t')
        if splited[1] in result:
            result[splited[1]].append(splited[0])
        else:
            result.update({splited[1]: [splited[0]]})
    f.close()
    return result


# params
author_file_path = 'data/dblp/authors.txt'
paper_file_path = 'data/dblp/papers.txt'
venue_file_path = 'data/dblp/venues.txt'

author_paper_maps_file_path = 'data/dblp/author_paper_maps.txt'
paper_venue_maps_file_path = 'data/dblp/paper_venue_maps.txt'

# loading the data
authors_dict = file_to_dict(author_file_path)
authors_reversed_dict = file_to_reverse_dict(author_file_path)
papers_dict = file_to_dict(paper_file_path)
venues_dict = file_to_dict(venue_file_path)

author_paper_maps_dict = file_to_dict(author_paper_maps_file_path)
paper_venue_maps_dict = file_to_dict(paper_venue_maps_file_path)

author_node_list = []
paper_node_list = []
venue_node_list = []


for index, author_paper_map in enumerate(author_paper_maps_dict):

    author_node_id = 'author_{}'.format(author_paper_map)
    author_name = authors_dict[author_paper_map][0]
    dblpGraph.add_node(author_node_id, node_type = 'AUTHOR', full_name = author_name)

    for paper_id in author_paper_maps_dict[author_paper_map]:

        paper_title = ''
        paper_node_id = 'paper_{}'.format(paper_id)
        if paper_id in papers_dict:
            paper_title = papers_dict[paper_id][0]
        dblpGraph.add_node(paper_node_id, node_type = 'PAPER', title = paper_title)

        dblpGraph.add_edge(author_node_id, paper_node_id, relation_type='write')

for index, paper_venue_map in enumerate(paper_venue_maps_dict):

    paper_node_id = 'paper_{}'.format(paper_venue_map)
    venue_node_id = 'venue_{}'.format(paper_venue_maps_dict[paper_venue_map][0])

    dblpGraph.add_node(venue_node_id, node_type='VENUE',
                       name = venues_dict[paper_venue_maps_dict[paper_venue_map][0]][0])

    dblpGraph.add_edge(paper_node_id, venue_node_id, relation_type = 'publish_at')

nx.write_gexf(dblpGraph, 'data/dblp_graph.gexf', encoding="utf-8")
