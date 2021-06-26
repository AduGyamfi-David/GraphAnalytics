import networkx as nx
import matplotlib.pyplot as plt

def bubblesort(r):
    for i in range(0, len(r)):
        for j in range(0, len(r) - (i + 1)):
            if (r[j] > r[j + 1]) :
                r[j], r[j + 1] = r[j + 1], r[j]
    return r

G = nx.read_adjlist(r"C:\Users\dadug\Documents\GraphAnalytics\Week3\graph-assignment.txt")

plot = nx.planar_layout(G)
print(nx.shortest_path(G, "0", "4", method="dijkstra"))

H = nx.breadth_first_search.bfs_tree(G, "7")
nx.draw_networkx(H, pos=plot, arrows=True, with_labels=True)
plt.savefig(r"Week3\BFS_Graph.png", format="PNG")
plt.show()

I = nx.depth_first_search.dfs_tree(G, "7")
nx.draw_networkx(I, pos=plot, arrows=True, with_labels=True)
plt.savefig(r"Week3\DFS_Graph.png", format="PNG")
plt.show()

G_pg = nx.pagerank(G)
ranks = list(G_pg.values())

print(ranks[len(ranks) - 1])