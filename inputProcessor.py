import json
import pandas as pd
import numpy as np
from pathlib import Path


class Data:
    def __init__(self, file_name):
        input_file = open(f'{Path().absolute()}\\{file_name}')
        raw_inputs = input_file.read().split()
        self.numOfNodes = int(raw_inputs[0])
        self.numOfEdges = int(raw_inputs[1])
        edges = []
        nodes = []
        for i in range(2, len(raw_inputs) - 1, 2):
            edges.append({'source': int(raw_inputs[i]), 'target': int(raw_inputs[i + 1])})
        for i in range(1, self.numOfNodes + 1):
            nodes.append({'name': i, 'group': 0})
        self.data = {'nodes': nodes, 'edges': edges}
        self.get_node_groups(self, self.data)

    @staticmethod
    def get_node_groups(self, data):
        num_edges = np.zeros(self.numOfNodes + 1)
        for e in data['edges']:
            num_edges[e['source']] += 1
            num_edges[e['target']] += 1

        for i, n in enumerate(data['nodes']):
            n['group'] = int(num_edges[i])
