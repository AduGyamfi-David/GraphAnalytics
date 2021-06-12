import matplotlib.pyplot as plt
import networkx as nx
import csv

#* GRAPH OF DOM FOR HTML SITES

DOM = nx.DiGraph()

with open('dom_graph.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    count = 0
    for row in reader:
        if count == 0:
            count += 1
        else:
            print(row)
            DOM.add_node(row[0], name=row[1], id=row[0])
            DOM.add_edge(row[0], row[2])
    print("DONE")

nx.draw(DOM, with_labels=True)
plt.show()

