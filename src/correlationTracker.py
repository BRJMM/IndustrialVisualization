import pandas as pd

class CorrelationTracker:
    def __init__(self, corr_change:float = 1.0, num_digits = 6) -> None:
        self.tracker_value = {}
        self.tracker_color = {}
        self.num_digits = num_digits
        self.corr_change = corr_change

    def __getColor(self, key:str, curr_corr_value: float) -> str:
            diff = abs(curr_corr_value) - abs(self.tracker_value[key])
            change_color = (abs(diff) >= self.corr_change)
            color = 'green' if diff >= 0.0 else 'red'
            color = color if change_color else 'grey'
            return color
    
    def __getKey(self, column, row) -> str:
         return '{}-{}'.format(column, row)

    def SetCorrChangeValue(self, corr_change:float, num_digits=6) -> None:
        self.num_digits = num_digits
        self.corr_change = corr_change

    def SetCurrentStatus(self, data: pd.DataFrame) -> None:
        variables = data.columns
        keys = self.tracker_value.keys()
        for column in variables:
            for row in variables:
                curr_corr_value = round(data[column][row], self.num_digits)
                key = self.__getKey(column, row)
                if not key in keys:
                     self.tracker_value[key] = 0.0
                     self.tracker_color[key] = 'grey'
                color = self.__getColor(key, curr_corr_value)
                self.tracker_value[key] = curr_corr_value
                if color == 'grey':
                     self.tracker_color[key] = color
                if key == 'pumpspeed_rpm-pa7b3_mm':
                    print('Edge=[{}], Color=[{}], Value=[{}]'.format(key, self.tracker_color[key], self.tracker_value[key]))
    
    def GetColor(self, column, row) -> str:
         keya = self.__getKey(column, row)
         keyb = self.__getKey(row, column)
         keys = self.tracker_color.keys()
         if keya in keys:
              return self.tracker_color[keya]
         elif keyb in keys:
              return self.tracker_color[keyb]
         else:
             return 'grey'
