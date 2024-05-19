import dash_daq as daq

class PrecisionInputCreator:
    def __init__(self, min_value=0.0, max_value=1.0, initial_value=0.5, precision=4):
        self.min_value = min_value
        self.max_value = max_value
        self.initial_value = initial_value
        self.precision = precision
    
    def __verify_label_position(self, position):
        POSITIONS = ['top', 'bottom']
        if position.lower() not in POSITIONS:
            raise Exception('Position parameter should be {}, but has value=[{}]'.format(POSITIONS), type)

    def create(self, id, label, labelPosition='top'):
        self.__verify_label_position(labelPosition)
        return daq.PrecisionInput(
            min=self.min_value,
            max=self.max_value,
            value=self.initial_value,
            precision=self.precision,
            id=id,
            label=label,
            labelPosition=labelPosition
        )