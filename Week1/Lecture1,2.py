import matplotlib.pyplot as plt
import networkx as nx

G = nx.complete_graph(5, nx.Graph())
plt.subplot(121)
nx.draw(G)

H = G.to_directed()
plt.subplot(122)
nx.draw(H)

plt.show()