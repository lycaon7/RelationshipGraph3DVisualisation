import plotly.graph_objs as go

AXIS = dict(showbackground=False, showline=False, zeroline=False, showgrid=False, showticklabels=False, title='')


# Returns a layout for the HTML file that displays the graph
def get_html_layout():
    return go.Layout(
        width=1000,
        height=1000,
        showlegend=False,
        scene=dict(
            xaxis=dict(AXIS),
            yaxis=dict(AXIS),
            zaxis=dict(AXIS),
        ),
        margin=dict(t=100),
        hovermode='closest',
        annotations=[
            dict(
                showarrow=False,
                text='',
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
        ],
    )
