import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()

# G.add_edge("1", "2", type="CONNECTED_TO")
G.add_edges_from([(1, 2), (2, 3), (3, 1)], type="CONNECTED_TO")
# G.add_node({[1, label='Person', name='me'], [2, label='ha', name='me']})
# print(G.nodes)

pos = nx.spring_layout(G)

nx.draw(G, pos)
plt.show()