#https://networkx.org/documentation/stable/reference/introduction.html#networkx-basics
import networkx as nx
from nltk.tokenize import word_tokenize, sent_tokenize
import matplotlib.pyplot as plt

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
        tokens = sent_tokenize(raw_text)
    
    # add nodes to the graph, hash by position in tokens list
    for ind in range(len(tokens)):
        graph.add_node(ind)
        # add node attributes
        attributes = {ind:{'token':tokens[ind]}}
        nx.set_node_attributes(graph, attributes)

    # add edges to the graph
    for ind in range(len(tokens) - 1):
        # assuming undirected graph, only assigning one way
        graph.add_edge(ind, (ind+1))
        # add edge attributes
        attributes = {(ind, ind+1):{'cosine_sim':0.0}}
        nx.set_edge_attributes(graph, attributes)

    nx.draw(graph)
    plt.show()
    return graph

def main():
    raw_text = "hello world! I am here"
    args = {'TokenType':'sentence', 'EdgeType':'single'}
    build_text_graph(raw_text,args)


if __name__ == '__main__':
    main()

