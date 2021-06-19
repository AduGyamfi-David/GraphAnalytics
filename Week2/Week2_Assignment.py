import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.bipartite.basic import color

G = nx.read_graphml(r"C:\Users\dadug\Documents\GraphAnalytics\Week2\graph.graphml")

pos1 = nx.spring_layout(G)

data = {
    "1": "Person",
    "2": "Social Media",
    "3": "Credit Card",
    "4": "Transaction",
    "5": "Pos",
    "6": "Store",
    "22": "Category"
}

nx.set_node_attributes(G, "#fff", "color")

color_map = nx.get_node_attributes(G, "color")

# print(color_map)

color_map["1"] = "#ff0000"
color_map["6"] = "#ffa000"

node_colors = color_map.values()
print(node_colors)
# print(data)

nx.draw_networkx(G, pos=pos1, node_color=node_colors, with_labels=True, edgecolors="#000000", labels=data)
plt.savefig("Graph1.png", format="PNG")
plt.show()

# ! - Orginal color is blue (#1f78b4), must change all to clear/white first
# * clear color is node_color = "ffffff" (using hex) 
# % ISSUE: Setting color to white also removes borders. Need to add border to nodes
# _ RESOLVED: Now must include labels
# // todo - Suggesting orginal default settings (inc pos), so "hard-write" all "default" settings 
# // todo - Show labels on graph
# ! Struggled with resizing nodes to automatically fit text