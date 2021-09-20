import networkx as nx
import matplotlib.pyplot as plt
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from stellargraph import StellarGraph
from stellargraph.data import BiasedRandomWalk



from networkx.classes.function import nodes
from networkx.generators import random_clustered

# with open(r"Week5\wikiElec.ElecBs3.txt", "r", encoding="utf8", errors="ignore") as graph_file :

#     for i in range(7):

#         graph_file.readline()

#     for line in graph_file:
#         current_line = line.split("    ")
#         if (current_line[0] != " "):
#             print(line)
 #* Wanted to use above dataset, but had data with unfamiliar characters
 #* needed to go through data set and format text to ensure it all satisfies utf8 encoding
    #* or more specifically, the names of the users in the data set (and thus only the "strings")

def main():
    G = nx.read_adjlist(r"Week5/facebook_combined.txt")

    sG = getSampleGraph(G, int(nx.number_of_nodes(G) * 0.8))

    print(nx.number_of_nodes(sG))

    getEmbeddings(sG, G)

    # nx.draw_networkx(sG, pos=nx.spring_layout(sG), with_labels=False)
    # plt.show()

def getSampleGraph(G, count):
    sample = nx.Graph(G)

    all_nodes = list(sample.nodes)

    node_indexes = random.sample(range(0, len(all_nodes) - 1), count)

    for i in range(0, len(node_indexes)):
        sample.remove_node(all_nodes[node_indexes[i]])
    
    # // for i in range(0, len(nx.number_of_nodes(G) * 0.8)):
        # // s = random.randint(0, nx.number_of_nodes(sample))
        # // print(str(s) + " " + str(nx.number_of_nodes(sample)) + " " + str(i))
        # // print(str(s) + " " + str(i))
        # // if (sample.has_node(str(i))):
        # //     print("NODE FOUND")
        # // while not(sample.has_node(str(s))):
        # //     s = random.randint(0, nx.number_of_nodes(sample))
        # //     print(s)
        # // print("\n")
        # // sample.remove_node(str(s))

    # print(len(list(sample.nodes)))

    #* Tried to randomly select 80% of all nodes
    #* and reselect if node not identified
    #* but kept running into issue of infinite looping (or something adjacent to it)
    #* so instead, generated a bunch of indexes to index a list of all nodes
    #* then remove each node from this list 
    #* no indefinite iteration used, and finite time complexity

    return sample

def getEmbeddings(sG, G):
    walk = BiasedRandomWalk(G)
    all_walks = walk.run(nodes=list(G.nodes), length=32, n=10, p=0.5, q=0.2)
    print("Number of walks = " + str(len(all_walks)))


main()