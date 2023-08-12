import json
import urllib.request
import igraph as ig
import numpy
import plotly.graph_objs as go
import pandas as pd
from inputProcessor import Data
from pathlib import Path

PROCESSED_DATA = Data('inputs.txt')
data = PROCESSED_DATA.data

# Save data to cvs for ease of analysis
for d in data:
    df = pd.DataFrame(data[d])
    filepath = f'{Path().absolute()}\\data{d.capitalize()}.csv'
    df.to_csv(filepath)

# Create graph from data
edges = [(data['edges'][k]['source'], data['edges'][k]['target']) for k in range(PROCESSED_DATA.numOfEdges)]
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
Xn = [layt[k][0] for k in range(PROCESSED_DATA.numOfNodes)]  # x-coordinates of nodes
Yn = [layt[k][1] for k in range(PROCESSED_DATA.numOfNodes)]  # y-coordinates of nodes
Zn = [layt[k][2] for k in range(PROCESSED_DATA.numOfNodes)]  # z-coordinates of nodes

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

axis = dict(showbackground=False, showline=False, zeroline=False, showgrid=False, showticklabels=False, title='')

# Layout of the HTML
layout = go.Layout(
    title="Test of Library",
    width=1000,
    height=1000,
    showlegend=False,
    scene=dict(
        xaxis=dict(axis),
        yaxis=dict(axis),
        zaxis=dict(axis),
    ),
    margin=dict(
        t=100
    ),
    hovermode='closest',
    annotations=[
        dict(
            showarrow=False,
            text="Data source: <a href='http://bost.ocks.org/mike/miserables/miserables.json'>[1] miserables.json</a>",
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=dict(
                size=14
            )
        )
    ], )

data = [trace1, trace2]
fig = go.Figure(data=data, layout=layout)
fig.write_html('graph.html', auto_open=False)
