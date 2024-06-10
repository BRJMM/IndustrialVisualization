import pandas as pd
import networkx as nx
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from dccClassWrappers import DccInputNumber
from dataPreprocessor import DataPreprocessor
from machineSelector import MachineSelector
from contextParameter import ContextParameter
from correlationTracker import CorrelationTracker

TOTAL_SHIFT = 3
HOURS_IN_SHIFT = 1440
COLUMNS_IN_LAYOUT = 10
NETWORK_GRAPH_COLUMNS = 8
HOURS_IN_DAY = 24
BORDER_LAYOUT_COLOR = 'black'

print('\n\n\n\n\n\n\n\nStarting execution ........................................\n')

machineSelector = MachineSelector('/home/craav/pCloudDrive/Computer_Science_Master/Visualizacion_Informacion/Proyecto/IndustrialVisualization/data/test_data.csv')
input_file_path = machineSelector.ExecuteSelection('primary')

inputNumberCreator = DccInputNumber()
progress_value = 0

data_processor = DataPreprocessor(input_file_path)
dates = data_processor.GetDates()

contextParameter = ContextParameter()
correlationTracker = CorrelationTracker()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(style={
    'display': 'grid',
    'grid-template-columns': '{}fr {}fr'.format(NETWORK_GRAPH_COLUMNS, COLUMNS_IN_LAYOUT-NETWORK_GRAPH_COLUMNS),
    'grid-template-rows': 'auto 1fr',
    'gap': '10px',
    'height': '100vh',
    'padding': '10px'
}, children=[
    html.Div(style={
        'border': '2px solid {}'.format(BORDER_LAYOUT_COLOR),
        'padding': '10px'
    }, children=[
        dbc.Button("Play", id="play-button", n_clicks=0, style={'width': '100%', 'margin-bottom': '10px'}),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0, disabled=True),
        dbc.Progress(id="progress-bar", value=0, max=HOURS_IN_SHIFT, striped=True, animated=True, style={'width': '100%'}),
        html.Div(style={'display': 'flex', 'justify-content': 'space-between', 'margin-top': '10px'}, children=[
            html.Span('|', style={'margin': '0 2px'}) for _ in range(HOURS_IN_SHIFT+1)
        ])
    ], id='BUTTON_PLAY_AND_PROGRESS_BAR'),

    html.Div(style={
        'border': '2px solid {}'.format(BORDER_LAYOUT_COLOR),
        'padding': '10px'
    }, children=[
        html.Label("Shift"),
        dcc.Dropdown(
            id='shift-dropdown',
            options=[{'label': i, 'value': i} for i in range(1, TOTAL_SHIFT+1)],
            value=1,
            style={'margin-bottom': '10px'}
        ),
        html.Label("Date"),
        dcc.Dropdown(
            id='date-dropdown',
            options=[{'label': date, 'value': str(date)} for date in dates],
            value=str(dates[0]),
            style={'margin-bottom': '10px'}
        )
    ], id='DATE_AND_SHIFT_SELECTORS'),

    html.Div(style={
        'border': '2px solid {}'.format(BORDER_LAYOUT_COLOR),
        'padding': '10px',
        'grid-column': '1',
        'grid-row': '2'
    }, children=[
        dcc.Graph(id='network-graph', style={'width': '100%', 'height': '100%'})
    ], id='NETWORK_GRAPH_VISUALIZATION'),

    html.Div(style={
        'border': '2px solid {}'.format(BORDER_LAYOUT_COLOR),
        'padding': '10px',
        'grid-column': '2',
        'grid-row': '2'
    }, children=[
        html.Label("Correlated Threshold"),
        inputNumberCreator.create(id='correlated-threshold'),
        html.Label("Correlation Change"),
        inputNumberCreator.create(id='correlation-change', style={'width': '100%'})
    ], id='CONFIG_THRESHOLD')
])

@app.callback(
    [Output('network-graph', 'figure'),
     Output('progress-bar', 'value'),
     Output('interval-component', 'disabled')],
    [Input('date-dropdown', 'value'),
     Input('shift-dropdown', 'value'),
     Input('correlated-threshold', 'value'),
     Input('correlation-change', 'value'),
     Input('play-button', 'n_clicks'),
     Input('interval-component', 'n_intervals')],
    [State('interval-component', 'disabled')]
)
def update_graph(selected_date, shift_value, correlation_threshold, correlation_change, n_clicks, n_intervals, interval_disabled):
    global progress_value
    contextParameter.SetState(str(selected_date), str(shift_value), correlation_threshold, correlation_change)
    has_changed = contextParameter.HasAnyChanged()
    selected_date = pd.to_datetime(selected_date)
    filtered_df = data_processor.GetData(selected_date, shift_value, progress_value, correlation_threshold)

    correlationTracker.SetCorrChangeValue(corr_change=correlation_change)
    correlationTracker.SetCurrentStatus(filtered_df)

    run_condition = n_clicks % 2 != 0 and progress_value <= HOURS_IN_SHIFT
    interval_disabled = not run_condition
    progress_value = progress_value if not run_condition else progress_value + 1
    progress_value = 0 if ((progress_value > HOURS_IN_SHIFT) or has_changed) else progress_value

    print('Date=[{}], Shift=[{}], Correlation Threshold=[{}], Correlation Change=[{}], Shift Hour=[{}], Clicks=[{}], Interval disabled=[{}], Parameter change=[{}]'.format(selected_date, shift_value, correlation_threshold, correlation_change, progress_value, n_clicks, interval_disabled, has_changed))

    G = nx.from_pandas_adjacency(filtered_df)
    pos = nx.spring_layout(G)
    edge_trace = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=abs(edge[2]['weight'])*5, color=correlationTracker.GetColor(edge[0], edge[1])),
            hoverinfo='none',
            mode='lines'))
    
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2
        )
    )
    
    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['text'] += tuple([str(node)])
    
    fig = go.Figure(data=edge_trace + [node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Network Graph",
                            showarrow=False,
                            xref="paper", yref="paper"
                        )],
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)
                    ))
    
    return fig, progress_value, interval_disabled

if __name__ == '__main__':
    app.run_server(debug=True)