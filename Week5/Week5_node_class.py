from calendar import c
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import gensim
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from stellargraph import StellarGraph
from stellargraph.data import BiasedRandomWalk
from networkx.classes.function import nodes
from networkx.generators import random_clustered

names = ["Esther-Eden", "Zach", "Jemma", "Gabriel", "Abigail", "David", "Sam", "Mother", "Father"]

def loadGraph(e_path, n_path):
    edges = pd.read_csv(e_path, ',')
    G = nx.from_pandas_edgelist(edges, "id_1", "id_2")

    nodes = pd.read_csv(n_path, ',')
    nx.set_node_attributes(G, pd.Series(nodes.developer_type, index=nodes.id).to_dict(), "developer_type")
    nx.set_node_attributes(G, pd.Series(nodes.name, index=nodes.name).to_dict(), "name")
    nx.set_node_attributes(G, pd.Series(nodes.id, index=nodes.id).to_dict(), "id")

    return G

def getSampleGraph(G, count, seed):
    random.seed(seed)
    sample = nx.Graph(G)

    all_nodes = list(sample.nodes)

    node_indexes = random.sample(range(0, len(all_nodes) - 1), count)

    for i in range(0, len(node_indexes)):
        sample.remove_node(all_nodes[node_indexes[i]])

    return StellarGraph.from_networkx(sample)
    #* Returns Stellar directional graph

def getEmbeddings(sG, save=True):
    rw = BiasedRandomWalk(sG)

    walks = rw.run(nodes=list(sG.nodes()), length=32, n=10, p=0.5, q=2.0) #! Understand this
    print("Number of random walks: {}".format(len(walks)))

    str_walks = [[str(n) for n in walk] for walk in walks] #! Understand this
    #* Takes string for each walk in all biased random walks executed

    model = gensim.models.Word2Vec(str_walks, vector_size = 128, window = 5, min_count = 0, sg = 1, workers = 2) #! Understand this
    #* Word2Vec also commonly used in NLP
    #* i.e., all walks have been converted into strings, and now will used Word2Vec ot convert into vectors, therefore obtaining the node embeddings

    if (save):
        model.wv.save_word2vec_format(r"Week5/embeddings.txt")

    return model

def split_data(G, embeddings):
    X, Y = []

    for k in embeddings.keys():
        X.append(embeddings[k])
        Y.append(G.nodes[k]["developer_type"])

    x_train, y_train, x_test, y_test = model_selection.train_test_split(X, Y, test_size=0.2)

    return x_train, x_test, y_train, y_test

def main():
    G = loadGraph(r"Week5/git_edges.csv", r"Week5/git_nodes.csv")
    #* Nodes represent developers who have starred >10 repos
    #* edges represent mutual follower relationships between developers
    #* Web-developers = 0, ML developers = 1
    sG = getSampleGraph(G, int(nx.number_of_nodes(G) * 0.8), 1)

    model = getEmbeddings(sG)
    # x_train, x_test, y_train, y_test = split_data(G, model) 

    return 0

if (__name__ == "__main__"):
    main()