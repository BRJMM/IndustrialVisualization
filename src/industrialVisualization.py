import plotly.graph_objs as go
from layout import AreaVisualization, VisualizationLayout

# Create dummy data for the visualizations
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

# Create AreaVisualization instances for each visualization
scatter_vis = AreaVisualization(scatter_data, 'xy', 1, 1, 1, 5)
bar_vis = AreaVisualization(bar_data, 'xy', 1, 6, 1, 10)
line_vis = AreaVisualization(line_data, 'xy', 2, 1, 10, 8)
pie_vis = AreaVisualization(pie_data, 'domain', 2, 9, 10, 10)

# Create a VisualizationLayout instance
layout = VisualizationLayout(10, 10, [scatter_vis, bar_vis, line_vis, pie_vis])

# Show the layout
layout.show()
