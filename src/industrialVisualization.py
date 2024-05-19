import dash
from dash import html, dcc
import dash_daq as daq
import plotly.graph_objs as go
from layout import AreaVisualization, VisualizationLayout

##################
# Resolving Layout

scatter_data = go.Scatter(
    x=[1, 2, 3, 4, 5],
    y=[10, 11, 12, 13, 14],
    mode='markers',
    name='Scatter'
)

bar_data = go.Bar(
    x=['A', 'B', 'C', 'D'],
    y=[5, 7, 9, 11],
    name='Bar'
)

line_data = go.Scatter(
    x=[1, 2, 3, 4, 5],
    y=[2, 3, 5, 7, 11],
    mode='lines',
    name='Line'
)

pie_data = go.Pie(
    labels=['A', 'B', 'C', 'D'],
    values=[10, 20, 30, 40],
    name='Pie'
)

scatter_vis = AreaVisualization(scatter_data, 'xy', 1, 1, 1, 5)
bar_vis = AreaVisualization(bar_data, 'xy', 1, 6, 1, 10)
line_vis = AreaVisualization(line_data, 'xy', 2, 1, 10, 8)
pie_vis = AreaVisualization(pie_data, 'domain', 2, 9, 10, 10)

visualization_layout = VisualizationLayout(10, 10, [scatter_vis, bar_vis, line_vis, pie_vis], 'Dummy Title')
layout = visualization_layout.get_layout()

###################
# Application setup
app = dash.Dash(__name__)

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Dummy Big Title"),
    dcc.Graph(
        id='example-graph',
        figure=layout
    ),
    html.Div([
        html.Label("Set Precision:"),
        daq.PrecisionInput(
            id='precision-input',
            precision=2,
            labelPosition='top'
        )
    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top'})
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)