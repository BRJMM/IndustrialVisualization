from plotly.subplots import make_subplots

class AreaVisualization:
    def __init__(self, trace, type, start_row, start_col, end_row, end_col):
        self.trace = trace
        self.__set_type(type)
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
    
    def __set_type(self, type) -> None:
        self.type = type.lower()
        TYPES = ['xy', 'domain']
        if self.type not in TYPES:
            raise Exception('Type parameter should be {}, but has value=[{}]'.format(TYPES), type)

class VisualizationLayout:
    def __init__(self, rows, cols, visualizations,
                 horizontal_spacing=0.02,
                 vertical_spacing=0.05,
                 border_layout_color='blue',
                 border_layout_width=2,
                 border_layout_type='line'):
        self.rows = rows
        self.cols = cols
        self.visualizations = visualizations

        # Layout border
        self.color = border_layout_color
        self.width = border_layout_width
        self.border_type = border_layout_type
        
        # Initialize specs with the appropriate spans
        specs = [[{} for _ in range(cols)] for _ in range(rows)]
        for vis in visualizations:
            for r in range(vis.start_row - 1, vis.end_row):
                for c in range(vis.start_col - 1, vis.end_col):
                    specs[r][c] = {'type': vis.type}
        
        self.fig = make_subplots(
            rows=rows, 
            cols=cols, 
            specs=specs,
            horizontal_spacing=horizontal_spacing,
            vertical_spacing=vertical_spacing
        )
        
        self._add_visualizations()
        self._add_separations()
        self._add_outer_borders()

    def _add_visualizations(self):
        for vis in self.visualizations:
            for i in range(vis.start_row, vis.end_row + 1):
                for j in range(vis.start_col, vis.end_col + 1):
                    self.fig.add_trace(vis.trace, row=i, col=j)
                    if i == vis.start_row and j == vis.start_col:
                        continue
                    self.fig.update_xaxes(matches='x', row=i, col=j)
                    self.fig.update_yaxes(matches='y', row=i, col=j)

    def _add_separations(self):
        self.fig.add_shape(
            dict(
                type=self.border_type,
                x0=0.5, y0=1, x1=0.5, y1=0.9,
                xref="paper", yref="paper",
                line=dict(
                    color=self.color,
                    width=self.width
                )
            )
        )
        self.fig.add_shape(
            dict(
                type=self.border_type,
                x0=0, y0=0.9, x1=1, y1=0.9,
                xref="paper", yref="paper",
                line=dict(
                    color=self.color,
                    width=self.width
                )
            )
        )
        self.fig.add_shape(
            dict(
                type=self.border_type,
                x0=0.8, y0=0.9, x1=0.8, y1=0,
                xref="paper", yref="paper",
                line=dict(
                    color=self.color,
                    width=self.width
                )
            )
        )

    def _add_outer_borders(self):
        self.fig.add_shape(
            dict(
                type=self.border_type,
                x0=0, y0=1, x1=1, y1=1,
                xref="paper", yref="paper",
                line=dict(
                    color=self.color,
                    width=self.width
                )
            )
        )
        self.fig.add_shape(
            dict(
                type=self.border_type,
                x0=0, y0=0, x1=1, y1=0,
                xref="paper", yref="paper",
                line=dict(
                    color=self.color,
                    width=self.width
                )
            )
        )
        self.fig.add_shape(
            dict(
                type=self.border_type,
                x0=0, y0=0, x1=0, y1=1,
                xref="paper", yref="paper",
                line=dict(
                    color=self.color,
                    width=self.width
                )
            )
        )
        self.fig.add_shape(
            dict(
                type=self.border_type,
                x0=1, y0=0, x1=1, y1=1,
                xref="paper", yref="paper",
                line=dict(
                    color=self.color,
                    width=self.width
                )
            )
        )

    def show(self):
        self.fig.update_layout(
            title_text="4 Different Visualizations in One Window",
            height=900,
            showlegend=False
        )
        self.fig.show()