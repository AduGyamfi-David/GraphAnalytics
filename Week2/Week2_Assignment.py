import matplotlib.pyplot as plt
import networkx as nx

G = nx.read_graphml(r"C:\Users\dadug\Documents\GraphAnalytics\Week2\graph.graphml")

pos1 = nx.spring_layout(G)

data = nx.get_node_attributes(G, "name")

# print(data)

nx.draw_networkx(G, pos=pos1, node_size=1000, node_color="#FFFFFF", with_labels=True, edgecolors="#000000", labels=data)
plt.savefig("Graph.png", format="PNG")
plt.show()

# ! - Orginal color is blue (#1f78b4), must change all to clear/white first
# * clear color is node_color = "ffffff" (using hex) 
# % ISSUE: Setting color to white also removes borders. Need to add border to nodes
# _ RESOLVED: Now must include labels
# // todo - Suggesting orginal default settings (inc pos), so "hard-write" all "default" settings 
# // todo - Show labels on graph