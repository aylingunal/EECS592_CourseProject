import networkx as nx
import random
from helpers import *

'''calculate the density of a node given its id and graph'''
def node_density(node_id, graph, args):
    node_density = 0
    # since we're looping thru edges, check for edge directions
    directed = False
    if args['GraphType'] == 'directed':
        directed = True
    # loop thru edges
    edges_seen = []
    for u, v in graph.edges:
        # check that edge is connected to node_id
        if ((node_id == u) or (node_id == v)):
            if (u,v) not in edges_seen:
                # if directed, just check (u,v)
                if directed:
                    edges_seen.append((u,v))
                    node_density += graph.edges[u,v]['weight']
                # if undirected, don't repeat edges since (u,v)==(v,u)
                else:
                    if (v,u) not in edges_seen:
                        edges_seen.append((u,v))
                        edges_seen.append((v,u))
                        node_density += graph.edges[u,v]['weight']
    
    # node density = sum of edge weights / num vertices # TODO --> double check if H = # verts or # neighbors
    return node_density/len(graph.nodes)

'''compute the minimum density and return associated nodes.
function assumes that graph is not empty. '''
def minimum_density(graph, args):
    tmp = -1
    # **this is a terrible way of trivially picking a baseline node but networkx data structure is not allowing more obvious solutions!!
    for item in graph.nodes:
        tmp = item
        break
    # have random baseline comparison node for finding min density
    cur_min_density = node_density(tmp,graph,args)
    # track the weakest nodes
    weak_nodes = []
    # loop thru graph and find actual minimum density
    for node in graph.nodes:
        cur_node_density = node_density(node,graph,args)
        if cur_node_density < cur_min_density:
            # reassign min_density
            cur_min_density = cur_node_density
            # clear list of nodes w/ prev weakness threshold
            weak_nodes.clear()
            weak_nodes.append(node)
        # track nodes with the min density
        elif cur_node_density == cur_min_density:
            weak_nodes.append(node)
    
    return cur_min_density, weak_nodes

''' calculate similarity between a node and a cluster 
i.e. the average of the weighted edges between the node
and each node in the cluster 
'''
def node_cluster_similarity(node, cluster_nodes, graph):
    avg_weight = 0.0
    for cluster_node in cluster_nodes:
        if graph.has_edge(node, cluster_node):
            avg_weight += graph.edges[node, cluster_node]['weight']
    if len(cluster_nodes) == 0:
        return avg_weight
    return avg_weight / len(cluster_nodes)

''' calculate the similarity between two clusters
i.e. the average of the weighted edges of every edge between
the clusters '''
def cluster_cluster_similarity(cluster1, cluster2, graph):
    avg_weight = 0.0
    for node1 in cluster1:
        for node2 in cluster2:
            if graph.has_edge(node1, node2):
                avg_weight += graph.edges[node1, node2]['weight']
    if len(cluster1) * len(cluster2) == 0:
        return 0.0
    return avg_weight / (len(cluster1) * len(cluster2))

''' get similarity of new sentence to a cluster ''' 
def local_global_similarity(local_desc, global_cluster, graph):
    # convert global cluster
    global_cluster_text = [graph.nodes[x]['token'] for x in global_cluster]
    avg_weight = 0.0
    for node in global_cluster_text:
        avg_weight += compute_cosine_sim(local_desc, node)
    avg_weight = avg_weight / len(global_cluster_text)

    return avg_weight

# calculate density of input graph
def graph_density(graph):
    # density = # edges / # nodes
    return len(graph.edges)/len(graph.nodes)
