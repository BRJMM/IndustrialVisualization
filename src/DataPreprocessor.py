import pandas as pd
from datetime import time

class DataPreprocessor():
    """Creating a data preprocessor class."""

    def __init__(self, file_path):
        """Initialize dataframe."""
        self.df = pd.read_csv(file_path)
        self.__generateShifts()
        self.df_goal = self.df.copy()

    def __generateShifts(self):
        self.df['date_time'] = pd.to_datetime(self.df['date_time'])
        self.df.loc[(self.df['date_time'].dt.time >= time(6,0,0)) &
              (self.df['date_time'].dt.time < time(14,0,0)), 'shift'] = 'Shift_I'
        self.df.loc[(self.df['date_time'].dt.time >= time(14,0,0)) &
              (self.df['date_time'].dt.time < time(22,0,0)), 'shift'] = 'Shift_II'
        self.df.loc[(self.df['date_time'].dt.time >= time(22,0,0)) &
              (self.df['date_time'].dt.time < time(23,59,59)), 'shift'] = 'Shift_III'
        self.df.loc[(self.df['date_time'].dt.time >= time(0,0,0)) &
              (self.df['date_time'].dt.time < time(6,0,0)), 'shift'] = 'Shift_III'

    def FilterByDate(self, date):
        self.df = self.df[self.df['date_time'].dt.date == pd.to_datetime(date).date()]

    def FilterByShift(self, shift):
        self.df = self.df[self.df['shift'].dt.date == shift]

    def GetCorrelation(self, magnitude=0.1):
        correlation_matrix = self.df.select_dtypes(include='number').corr()
        mask = correlation_matrix.abs() >= magnitude
        correlation_matrix = correlation_matrix.where(mask)
        correlation_matrix = correlation_matrix.fillna(0)
        return correlation_matrix

    def Restart(self):
        self.df = self.df_goal.copy()