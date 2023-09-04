import igraph as ig
import plotly.graph_objs as go
import layoutBuilder
from dataProcessor import DataProcessor

print("Enter .txt file location (Example: C:\\Users\\USER\\Documents\\Graph3DVisualisation\\inputsExample.txt):")
dataProcessor = DataProcessor(input())
data = dataProcessor.data

# Create graph from data
edges = [(data['edges'][k]['source'], data['edges'][k]['target']) for k in range(dataProcessor.numOfEdges)]
G = ig.Graph(edges=edges, directed=False)

# Visualization of graph
nodeName = []
group = []
for node in data['nodes']:
    nodeName.append(node['name'])
    group.append(node['group'])
# Returns a layout for the graph based of the type of algorith supplied.
# In our case we use the kk algorithm which optimises readability.
layoutBlueprint = G.layout('kk', dim=3)

# Positions of the nodes in 3d space based on the algorithm
Xn = [layoutBlueprint[k][0] for k in range(1, dataProcessor.numOfNodes)]  # x-coordinates of nodes
Yn = [layoutBlueprint[k][1] for k in range(1, dataProcessor.numOfNodes)]  # y-coordinates of nodes
Zn = [layoutBlueprint[k][2] for k in range(1, dataProcessor.numOfNodes)]  # z-coordinates of nodes

# Positions of the edges in 3d space that connect the nodes
Xe = []
Ye = []
Ze = []
for e in edges:
    Xe += [layoutBlueprint[e[0]][0], layoutBlueprint[e[1]][0], None]  # x-coordinates of edge ends
    Ye += [layoutBlueprint[e[0]][1], layoutBlueprint[e[1]][1], None]  # y-coordinates of edge ends
    Ze += [layoutBlueprint[e[0]][2], layoutBlueprint[e[1]][2], None]  # z-coordinates of edge ends

# Creates traces based on edge position to be visualized by plotly
trace1 = go.Scatter3d(x=Xe, y=Ye, z=Ze, mode='lines', line=dict(color='rgb(125,125,125)', width=1.25), hoverinfo='none')

# Creates traces based on node position to be visualized by plotly
trace2 = go.Scatter3d(x=Xn, y=Yn, z=Zn, mode='markers', name='actors',
                      marker=dict(symbol='circle', size=6, color=group, colorscale='rainbow',
                                  line=dict(color='rgb(0,0,0)', width=1.5))
                      , text=nodeName, hoverinfo='text')

layout = layoutBuilder.get_html_layout()
data = [trace1, trace2]
fig = go.Figure(data=data, layout=layout)
fig.write_html(f'{dataProcessor.file.parent}\\build.html', auto_open=False)
