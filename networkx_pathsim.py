import networkx as nx


# finding the author node by full name
def find_author_node_by_name(dblpGraph, author_name):
    for (p, d) in dblpGraph.nodes(data=True):
        if d['node_type'] == 'AUTHOR':
            if d['full_name'] == author_name:
                return p


# reading dblp graph from gexf file
dblpGraph = nx.DiGraph()
dblpGraph = nx.read_gexf('data/dblp_graph.gexf')

# params
author_node_list = []
venue_node_list = []
paper_node_list = []

for (p, d) in dblpGraph.nodes(data=True):
    if d['node_type'] == 'AUTHOR':
        author_node_list.append(p)
    if d['node_type'] == 'VENUE':
        venue_node_list.append(p)
    if d['node_type'] == 'PAPER':
        paper_node_list.append(p)

# finding similar author by PathSim
source_author_name = 'AnHai Doan'
source_author_id = find_author_node_by_name(dblpGraph, source_author_name)

for target_author_id in author_node_list:

    meta_path_count = 0
    self_source_path_count = 0
    self_target_path_count = 0

    for venue_node_id in venue_node_list:

        path_count_source_author_venue = 0
        path_count_target_author_venue = 0

        if nx.has_path(dblpGraph, source_author_id, venue_node_id):

            source_existed_paths = nx.all_simple_paths(dblpGraph, source=source_author_id, target=venue_node_id)
            for path in source_existed_paths:
                path_count_source_author_venue += 1

            self_source_path_count += float(path_count_source_author_venue) ** 2

            if nx.has_path(dblpGraph, target_author_id, venue_node_id):
                target_existed_paths = nx.all_simple_paths(dblpGraph, source=target_author_id, target=venue_node_id)
                for path in target_existed_paths:
                    path_count_target_author_venue += 1
            self_target_path_count += float(path_count_target_author_venue) ** 2

            meta_path_count += (float(path_count_source_author_venue) * float(path_count_target_author_venue))
        else:
            continue

    if meta_path_count > 0:

        sim_socre = 2 * float(meta_path_count) / (float(self_source_path_count)
                                                  + float(self_target_path_count))

        print('SimScore: {} -> {} = {}'.format(dblpGraph.nodes(data=True)[source_author_id]['full_name'],
                                     dblpGraph.nodes(data=True)[target_author_id]['full_name'],
                                     sim_socre))
