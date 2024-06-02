import pandas as pd
from datetime import time, date

class DataPreprocessor():
    """Crearing a data preprocessor class."""

    def __init__(self, dataframe):
        """Initialize dataframe."""
        self.dataframe = dataframe

    def dateFiltering(self, date):
        return self.dataframe[self.dataframe['date_time'].dt.date == pd.to_datetime(date).date()]

    def shiftFiltering(self, shift):
        return self.dataframe[self.dataframe['shift'].dt.date == shift]
        
    def shiftGenerator(self):
        
        self.dataframe.loc[(self.dataframe['date_time'].dt.time >= time(6,0,0)) &
              (self.dataframe['date_time'].dt.time < time(14,0,0)), 'shift'] = 'Shift_I'
        self.dataframe.loc[(self.dataframe['date_time'].dt.time >= time(14,0,0)) &
              (self.dataframe['date_time'].dt.time < time(22,0,0)), 'shift'] = 'Shift_II'
        self.dataframe.loc[(self.dataframe['date_time'].dt.time >= time(22,0,0)) &
              (self.dataframe['date_time'].dt.time < time(23,59,59)), 'shift'] = 'Shift_III'
        self.dataframe.loc[(self.dataframe['date_time'].dt.time >= time(0,0,0)) &
              (self.dataframe['date_time'].dt.time < time(6,0,0)), 'shift'] = 'Shift_III'
        
        return self.dataframe
        
    def correlationMatrix(self):        
        return self.dataframe.select_dtypes(include='number').corr()