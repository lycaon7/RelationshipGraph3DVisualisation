import pandas as pd
import numpy as np
from pathlib import Path


# Class used to process input .txt file in to an easier to work with format.
class DataProcessor:
    def __init__(self, file):
        self.file = Path(Path(file).as_posix())

        # Reads input txt file and puts the values into an array.
        # Note that the code is written in a way to accept the format of the txt files outputted from
        # the FORTRAN simulations used in the research of Prof. Richard Berkovits.
        # As such it is not generalised for any txt file of relationships.
        try:
            input_file = open(self.file, 'r')
            if self.file.suffix != '.txt':
                exit("Invalid File Type")
        except FileNotFoundError:
            exit("File Not Found")
        raw_inputs = input_file.read().split()

        # The first value in the array is the number of nodes
        # and the second value is the number of edges.
        # Following that, values at an even index are the source of an edge
        # and values at an odd index are the target of the edge
        self.numOfNodes = int(raw_inputs[0])
        self.numOfEdges = int(raw_inputs[1])
        edges = []
        nodes = []
        for i in range(1, self.numOfNodes):
            nodes.append({'name': i, 'group': 0})
        for i in range(2, len(raw_inputs) - 1, 2):
            edges.append({'source': int(raw_inputs[i]), 'target': int(raw_inputs[i + 1])})
        self.data = {'nodes': nodes, 'edges': edges}

        self.get_node_groups(self, self.data)
        self.create_csv(self)

    # Iterators over the edges and counts how many edges each node has.
    # We then define the group of the node based on the number of edges it has.
    @staticmethod
    def get_node_groups(self, data):
        num_edges = np.zeros(self.numOfNodes + 1)
        for e in data['edges']:
            num_edges[e['source']] += 1
            num_edges[e['target']] += 1

        for i, n in enumerate(data['nodes']):
            n['group'] = int(num_edges[i + 1])

    # Creates CSV files of the nodes and their group and the edge's source and target.
    @staticmethod
    def create_csv(self):
        for d in self.data:
            df = pd.DataFrame(self.data[d])
            filepath = Path(f'{self.file.parent}/CSVs/data{d.capitalize()}.csv')
            filepath.parent.mkdir(exist_ok=True)
            df.to_csv(filepath)
