import pandas as pd
import numpy as np
import networkx as nx
from datetime import datetime, timedelta
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from dccClassWrappers import DccInputNumber
from dataPreprocessor import DataPreprocessor

TOTAL_SHIFT = 3
HOURS_IN_SHIFT = 8
COLUMNS_IN_LAYOUT = 10
NETWORK_GRAPH_COLUMNS = 8
HOURS_IN_DAY = 24
BORDER_LAYOUT_COLOR = 'black'

print('\n\n\n\n\n\n\n\nStarting execution ........................................\n')

inputNumberCreator = DccInputNumber()
progress_value = 0

def generate_mock_data(start_date, days):
    data = []
    np.random.seed(42)
    for day in range(days):
        for hour in range(HOURS_IN_DAY):
            date = start_date + timedelta(days=day, hours=hour)
            num_nodes = np.random.randint(5, 15)
            num_edges = np.random.randint(4, num_nodes*(num_nodes-1)//2)
            
            G = nx.gnm_random_graph(num_nodes, num_edges)
            for edge in G.edges():
                data.append({
                    'datetime': date,
                    'source': edge[0],
                    'target': edge[1],
                    'weight': np.random.rand()
                })
    return pd.DataFrame(data)

df = generate_mock_data(datetime(2023, 1, 1), 2)
data_processor = DataPreprocessor('C:\\Users\\brianmorera\\OneDrive - Microsoft\\Documents\\Personal\\TEC\\Cursos\\Visualizacion de la Informacion\\IndustrialVisualization\\data\\data.csv')
data = data_processor.GetData('2023-06-22 14:17:51.128885', 2, 0.7)
print(data)

dates = df['datetime'].dt.date.unique()

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
     Input('interval-component', 'n_intervals'),
     Input('play-button', 'n_clicks')],
    [State('interval-component', 'disabled')]
)
def update_graph(selected_date, shift_value, n_intervals, n_clicks, interval_disabled):
    global progress_value
    selected_date = pd.to_datetime(selected_date)
    #print('Clicks=[{}], Shift=[{}], Intervals=[{}], Current Hour=[{}], Interval disabled=[{}]'.format(n_clicks, shift_value, n_intervals, progress_value, interval_disabled))
    filtered_df = df[df['datetime'] == selected_date + timedelta(hours=progress_value)]

    run_condition = n_clicks % 2 != 0 and progress_value <= HOURS_IN_SHIFT
    interval_disabled = not run_condition
    progress_value = progress_value if not run_condition else progress_value + 1
    progress_value = 0 if progress_value > HOURS_IN_SHIFT else progress_value
    
    G = nx.from_pandas_edgelist(filtered_df, 'source', 'target', ['weight'])
    
    pos = nx.spring_layout(G)
    edge_trace = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=edge[2]['weight']*5, color='grey'),
            hoverinfo='none',
            mode='lines'
        ))
    
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
