import networkx as nx
import matplotlib.pyplot as plt

def findmax(r):
    dict_max = ""
    for i in range(0, len(r) - 1):
        if (r[str(i)] > r[str(i + 1)]):
            dict_max = (i, r[str(i)])
    return dict_max

G = nx.read_adjlist(r"C:\Users\dadug\Documents\GraphAnalytics\Week3\graph-assignment.txt")
# G = nx.read_graphml(r"C:\Users\dadug\Documents\GraphAnalytics\Week3\assignment3_graph.graphml")

weights = nx.get_edge_attributes(G, "weight")
# print(weights)

plot = nx.planar_layout(G)
nx.draw_networkx(G, pos=plot)
nx.draw_networkx_edge_labels(G, pos=plot, edge_labels=weights)
plt.savefig(r"Week3\Graph_adjlist.png", format="PNG")
plt.show()

print(nx.dijkstra_path(G, "0", "4"))
print(nx.dijkstra_path_length(G, "0", "4"))

H = nx.breadth_first_search.bfs_tree(G, "7")
nx.draw_networkx(H, pos=plot, arrows=True, with_labels=True)
plt.savefig(r"Week3\BFS_Graph_adjlist.png", format="PNG")
plt.show()

I = nx.depth_first_search.dfs_tree(G, "7")
nx.draw_networkx(I, pos=plot, arrows=True, with_labels=True)
plt.savefig(r"Week3\DFS_Graph_adjlist.png", format="PNG")
plt.show()

G_pg = nx.pagerank(G)

print(findmax(G_pg))