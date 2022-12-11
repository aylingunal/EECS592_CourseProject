#https://networkx.org/documentation/stable/reference/introduction.html#networkx-basics
import networkx as nx
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import matplotlib.pyplot as plt
from helpers import *

# given an input text, create a text graph given
# specifications provided by args (type dict)
def build_text_graph(raw_text, args):
    # create graph object
    graph = nx.Graph()
    if args['EdgeType'] == 'Multi':
        graph = nx.MultiGraph()

    # tokenize the text
    tokens = []
    if args['TokenType'] == 'word':
        tokens = word_tokenize(raw_text)
    elif args['TokenType'] == 'sentence':
        tokens = raw_text.split('</s>')
       # tokens = sent_tokenize(raw_text)
    
    # add nodes to the graph, hash by position in tokens list
    for ind in range(len(tokens)):
        graph.add_node(ind)
        # add node attributes
        attributes = {ind:{'token':tokens[ind]}}
        nx.set_node_attributes(graph, attributes)

    ### ADD EDGES ###
    # add edges to the graph
    for ind in range(len(tokens)):
        # get cos sim between every pair of nodes for now
        for ind2 in range(len(tokens)):
            # don't compare node to itself, and assuming undirected graph so don't add (u,v),(v,u) both
            if ((ind != ind2) and (graph.has_edge(ind2, ind) == False)):
                cosine_sim = compute_cosine_sim(tokens[ind],tokens[ind2])
                if cosine_sim > 5.0:
                    graph.add_edge(ind, ind2)
                    # add edge attributes
                    #cosine_sim = compute_cosine_sim(tokens[ind],tokens[ind2])
                    attributes = {(ind, ind2):{'weight':cosine_sim,'weight_type':'cosine_sim'}}
                    nx.set_edge_attributes(graph, attributes)

    # TODO / optional: remove edges w/ sim weights below a certain threshold

    # display graph (comment this out for large datasets, this takes a while)
   # nx.draw(graph)
   # plt.show()
    return graph

# def main():
#     raw_text = "Premium composition leather exterior and soft interior offer great protection against daily use; Classic and professional design, solid construction\
#                 Support auto Sleep/Wake feature; Cover features magnetic closure; Features a large front document card pocket to keep personal belongings\
#                 Full access to all features (Cameras, Speaker, Ports and Buttons); Multiple slots able to set up multiple horizontal stand angles\
#                 Built-in elastic pencil holder for Apple Pencil or stylus"
#     args = {'TokenType':'word', 'EdgeType':'single'}
#     graph = build_text_graph(raw_text,args)




# if __name__ == '__main__':
#     main()