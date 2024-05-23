from dash import dcc

class DccInputNumber:
    def __init__(self, min_value=0.0, max_value=1.0, initial_value=0.5):
        self.min_value = min_value
        self.max_value = max_value
        self.initial_value = initial_value
        self.__validate()
    
    def __validate(self):
        if(self.min_value >= self.max_value):
            raise Exception('max value should be higher than min.')
        if(self.initial_value < self.min_value or self.initial_value > self.max_value):
            raise Exception('initial value should be between min and max.')

    def create(self, id, style={'width': '100%', 'margin-bottom': '10px'}):
        return dcc.Input(id=id,
                         type='number',
                         value=self.initial_value,
                         min=self.min_value,
                         max=self.max_value,
                         style=style)