from GraphBuilder import *
from GraphMetrics import *
import copy

''' compute the density variation sequence '''
def density_variation_seq(graph, args):
    # make a copy of the graph to work with
    graph_copy = copy.deepcopy(graph)
    # initialize vars to track min densities and weak nodes
    seq_min_densities = []
    seq_weak_nodes = []
    # compute min density and remove weak nodes until graph is empty
    while len(graph_copy.nodes) > 0:
        cur_min_density, weak_nodes = minimum_density(graph_copy, args)
        seq_min_densities.append(cur_min_density)
        seq_weak_nodes.append(weak_nodes)
        graph_copy.remove_nodes_from(weak_nodes)

    return seq_min_densities, seq_weak_nodes


''' identify the set of core nodes 
-- alpha = [0,1], beta is a real number
iterate thru sequences
for ith position in sequence:
    if ((min_dens[i] - min_dens[i+1]) / min_dens[i]) > alpha:
        if i-beta =< i <= i+beta where all [min_dens[i-beta],min_dens[i+beta]] also have greater rate of increase than alpha
            core_nodes.append(weak_nodes[i])
'''
def identify_core_nodes(seq_min_densities, seq_weak_nodes,
                        alpha, beta):
    # sanity check
    if len(seq_min_densities) != len(seq_weak_nodes):
        print('Sequence lengths are not equal')
        return
    # track core nodes
    core_nodes = []
    # iterate thru sequences
    for i in range(len(seq_min_densities)-1):
        condition1 = 0
        # calculate condition 1
        if seq_min_densities[i] > 0:
            condition1 = ((seq_min_densities[i] - seq_min_densities[i + 1]) / seq_min_densities[i])
            # check condition 1
            if condition1 > alpha:
                # calculate condition 2
                if ((seq_min_densities[i] - seq_min_densities[i + 1]) / seq_min_densities[i]) > alpha:
                        # establish beta-group
                        lb = i - beta
                        if lb < 0:
                            lb = 0
                        ub = i + beta + 1
                        if ub > len(seq_min_densities):
                            ub = len(seq_min_densities)
                        beta_group = seq_min_densities[lb:ub]
                        # check condition 2:
                        condition2 = True
                        for j in range(len(beta_group) - 1):
                            if beta_group[j] == 0:
                                if 0 < alpha:
                                    condition2 = False
                            # if last element is last in seq_min_dens, skip
                            else:
                                if ((beta_group[j] - beta_group[j + 1]) / beta_group[j]) <= alpha:
                                    condition2 = False
                        # if condition 2 also satisfied, add as a core node
                        if condition2:
                            core_nodes.extend(seq_weak_nodes[i])

    return core_nodes


''' partition the core nodes into cluster cores.
the clustering method here can be a little more flexible / optional;
it's just a measure to help reduce the number of total nodes to be 
clustered.
 '''
def partition_core_nodes(core_nodes):
    # set up dict with core nodes as keys and cluster nodes as values
    core_nodes_dict = {}
    for node in core_nodes:
        core_nodes_dict[node] = []
    return core_nodes_dict

''' assign remaining non-core nodes to clusters 
for each non-core node, compute similarity between
it and existing clusters; assign to highest sim cluster
options for measuring similarity 
- sim(n,C) = average weights between n and all nodes in C
- sim(n,C) = max weight between n and a node in cluster
pseudo
clusters = core_nodes
for node in graph not in core_nodes:
    max_sim, max_cluster = 0
    for core_node in core_node:
        cur_sim = similarity(node, core_node)
        if cur_sim > max_sim, max_sim 
            max_sim, max_cluster = cur_sim, core_node
    clusters[max_cluster].append(node)
'''
def expand_clusters(core_nodes_dict, graph):
    print('beginning expand clusters...')
    for node in graph.nodes:
        # check only remaining non-core nodes
        if node not in core_nodes_dict.keys():
            # set up comparison node calculation
            ind = 0
            max_sim = 0
            max_node = 0
            # iterate thru clusters
            for core_node in core_nodes_dict.keys():
                # define the cluster (i.e. add core node to assoc cluster nodes)
                cluster_set = [core_node]
                cluster_set.extend(core_nodes_dict[core_node])
                # calculate similarity between node and cluster
                cur_node_cluster_sim = node_cluster_similarity(node, cluster_set, graph)
                # initialize comparison node
                if ind == 0:
                    max_sim = cur_node_cluster_sim
                    max_node = core_node
                ind += 1
                # update max sim and node if necessary
                if cur_node_cluster_sim > max_sim:
                    max_sim = cur_node_cluster_sim
                    max_node = core_node
            # add the node to the cluster
            core_nodes_dict[max_node].append(node)
    # return expanded clusters
    return core_nodes_dict


''' implements core-clustering
the core cluster algorithm is comprised of 4 steps:
1. computing the sequence of density variation
2. identification of core nodes
3. partitioning core nodes into cluster cores
4. assign non-core nodes to cluster cores 
 '''
def core_cluster(graph, args):
    # core clustering time oooo 
    seq_min_densities, seq_weak_nodes = density_variation_seq(graph, args)
    core_nodes = identify_core_nodes(seq_min_densities, seq_weak_nodes, alpha=.01, beta=1)
    core_nodes_dict = partition_core_nodes(core_nodes)
    core_nodes_dict = expand_clusters(core_nodes_dict, graph)



def main():
    # test sample text
    raw_text = "Premium composition leather exterior and soft interior offer great protection against daily use; Classic and professional design, solid construction\
                Support auto Sleep/Wake feature; Cover features magnetic closure; Features a large front document card pocket to keep personal belongings\
                Full access to all features (Cameras, Speaker, Ports and Buttons); Multiple slots able to set up multiple horizontal stand angles\
                Built-in elastic pencil holder for Apple Pencil or stylus"
    #raw_text = "Premium composition leather exterior and soft interior offer great protection against daily use"
    args = {'TokenType':'word', 'EdgeType':'single', 'GraphType':'undirected'}
    # build graph
    graph = build_text_graph(raw_text,args)
    core_cluster(graph, args)



if __name__ == '__main__':
    main()
