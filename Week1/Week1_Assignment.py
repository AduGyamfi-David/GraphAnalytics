import matplotlib.pyplot as plt
import networkx as nx
import csv

#* GRAPH OF DOM FOR HTML SITES

DOM = nx.DiGraph()
#* Direction of nodes points to parent element

with open('Week1/dom_graph.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    count = 0
    for row in reader:
        if count == 0:
            count += 1
        else:
            print(row)
            DOM.add_node(row[0], name=row[1], id=row[0])
            # if DOM.nodes[count - 1]['name'] == "HTML":
            #     DOM.nodes[count]['color']="#008000"
            print(DOM.nodes)
            DOM.add_edge(row[0], row[2])
    print("DONE")

color_map = []
#! need to select specific nodes by certain attributes to assign color map
# for node in DOM:
#     if node

nx.draw(DOM, with_labels=True)
plt.show()

# todo:
# todo - add color to essential nodes (i.e., essential elements in DOM, <body>, <head>, to specify hierarchy and different types of nodes) 
# todo - show nodes by name, not number
# todo - visualise as tree
# todo - script elements can be linked to elements (i.e., events). Need Different colour edges to demonstrate
