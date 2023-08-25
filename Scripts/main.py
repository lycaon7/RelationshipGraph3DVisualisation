import igraph as ig
import plotly.graph_objs as go
import layoutBuilder
from pathlib import Path
from dataProcessor import DataProcessor

# Input file name. Note the input file needs to be in the same folder as the python scripts!
FILE_NAME = 'inputs.txt'
dataProcessor = DataProcessor(FILE_NAME)
data = dataProcessor.data

# Create graph from data
edges = [(data['edges'][k]['source'], data['edges'][k]['target']) for k in range(dataProcessor.numOfEdges)]
G = ig.Graph(edges, directed=False)

# Visualization of graph
labels = []
group = []
for node in data['nodes']:
    labels.append(node['name'])
    group.append(node['group'])
# Returns a layout for the graph based of the type of algorith supplied.
# In our case we use the kk algorithm which optimises readability.
layt = G.layout('kk', dim=3)

# Positions of the nodes in 3d space based on the algorithm
Xn = [layt[k][0] for k in range(dataProcessor.numOfNodes)]  # x-coordinates of nodes
Yn = [layt[k][1] for k in range(dataProcessor.numOfNodes)]  # y-coordinates of nodes
Zn = [layt[k][2] for k in range(dataProcessor.numOfNodes)]  # z-coordinates of nodes

# Positions of the edges in 3d space that connect the nodes
Xe = []
Ye = []
Ze = []
for e in edges:
    Xe += [layt[e[0]][0], layt[e[1]][0], None]  # x-coordinates of edge ends
    Ye += [layt[e[0]][1], layt[e[1]][1], None]  # y-coordinates of edge ends
    Ze += [layt[e[0]][2], layt[e[1]][2], None]  # z-coordinates of edge ends

# Creates traces based on edge position to be visualized by plotly
trace1 = go.Scatter3d(x=Xe, y=Ye, z=Ze, mode='lines', line=dict(color='rgb(125,125,125)', width=1), hoverinfo='none')

# Creates traces based on node position to be visualized by plotly
trace2 = go.Scatter3d(x=Xn, y=Yn, z=Zn, mode='markers', name='actors',
                      marker=dict(symbol='circle', size=6, color=group, colorscale='rainbow',
                                  line=dict(color='rgb(50,50,50)', width=0.5))
                      , text=labels, hoverinfo='text')

layout = layoutBuilder.get_html_layout()
data = [trace1, trace2]
fig = go.Figure(data=data, layout=layout)
fig.write_html(f'{Path().absolute().parent}\\build.html', auto_open=False)
