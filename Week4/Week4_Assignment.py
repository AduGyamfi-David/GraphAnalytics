import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community.centrality import girvan_newman
import random

colors = [
    "blue", "gray", "pink", "red", "orange", "purple", "brown",
    "yellow", "green", "snow", "wheat", "lime", "crimson", "maroon",
    "dodgerblue", "olive", "gold", "hotpink", "palegreen",  
    "peachpuff", "steelblue", "royalblue", "slategray", "sandybrown",       
    "lawngreen", "lightgray", "sienna", "khaki", "mistyrose"]

G = nx.read_graphml(r"Week4\assignment3_graph.graphml")
H = nx.read_graphml(r"Week4\assignment3_graph.graphml")

p_G = nx.planar_layout(G)
p_H = nx.planar_layout(H)

color_dict = nx.coloring.greedy_color(G, strategy="random_sequential")

print(color_dict)

count = 0
node_colors = []
for i in color_dict.keys():
    node_colors.append(colors[color_dict[i]])

print(node_colors)

nx.draw_networkx(G, pos=p_G, with_labels=True, node_color=node_colors)
plt.savefig(r"Week4\colored_graph.png", format="PNG")
plt.show()

coms = girvan_newman(H)
node_coms = []

# print(coms)
# print(type(coms))

for community in next(coms):
    # print(community)
    node_coms.append(community)

coms_node_colors = []
for nc in range(len(node_coms)):
    col = random.randint(0, len(colors) - 1)
    print(col)
    for node in H:
        if node in node_coms[nc]:
            coms_node_colors.append(colors[col])

nx.draw_networkx(H, pos=p_H, node_color=coms_node_colors)
plt.savefig(r"Week4\community_graph.png", format="PNG")
plt.show()