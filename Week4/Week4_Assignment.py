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

p = nx.planar_layout(G)

color_dict = nx.coloring.greedy_color(G, strategy="random_sequential")

print(color_dict)

count = 0
node_colors = []
for i in color_dict.keys():
    node_colors.append(colors[color_dict[i]])

nx.draw_networkx(G, pos=p, with_labels=True, node_color=node_colors)
plt.savefig(r"Week4\colored_graph.png", format="PNG")
plt.show()