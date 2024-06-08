import pandas as pd
import numpy as np
from datetime import time

HOURS_IN_SHIFT = 8

class DataPreprocessor():
    """Creating a data preprocessor class."""

    def __init__(self, file_path):
        """Initialize dataframe."""
        self.df = pd.read_csv(file_path)
        self.selectedDate = ''
        self.selectedShift = 'Shift_I'
        self.selectedShiftHourRange = []
        self.__generateShifts()
        # Data frame for restore
        self.df_goal = self.df.copy()

    def __generateShifts(self) -> None:
        self.df['date_time'] = pd.to_datetime(self.df['date_time'])
        self.df.loc[(self.df['date_time'].dt.time >= time(6,0,0)) &
              (self.df['date_time'].dt.time < time(14,0,0)), 'shift'] = 'Shift_I'
        self.df.loc[(self.df['date_time'].dt.time >= time(14,0,0)) &
              (self.df['date_time'].dt.time < time(22,0,0)), 'shift'] = 'Shift_II'
        self.df.loc[(self.df['date_time'].dt.time >= time(22,0,0)) &
              (self.df['date_time'].dt.time < time(23,59,59)), 'shift'] = 'Shift_III'
        self.df.loc[(self.df['date_time'].dt.time >= time(0,0,0)) &
              (self.df['date_time'].dt.time < time(6,0,0)), 'shift'] = 'Shift_III'
    
    def __shiftIntToString(self, shiftAsInt: int) -> str:
        if shiftAsInt == 1:
            return 'Shift_I'
        if shiftAsInt == 2:
            return 'Shift_II'
        return 'Shift_III'

    def __filterByDate(self, date) -> None:
        self.selectedDate = pd.to_datetime(date).date()
        self.df = self.df[self.df['date_time'].dt.date == self.selectedDate]

    def __setHourShiftRange(self, shiftAsInt: int) -> None:
        if shiftAsInt == 1:
            self.selectedShiftHourRange = [6,7,8,9,10,11,12,13]
        elif shiftAsInt == 2:
            self.selectedShiftHourRange = [14,15,16,17,18,19,20,21]
        elif shiftAsInt == 3:
            self.selectedShiftHourRange = [22,23,0,1,2,3,4,5]
        else:
            raise Exception('__setHourShiftRange: shift should be [1,2,3]')

    def __filterByShift(self, shiftAsInt: int) -> None:
        self.__setHourShiftRange(shiftAsInt)
        self.selectedShift = self.__shiftIntToString(shiftAsInt)
        self.df = self.df[self.df['shift'] == self.selectedShift]

    def __filterByHour(self, hour:int) -> pd.DataFrame:
        copy = self.df.copy()
        return copy[copy['date_time'].dt.hour == self.selectedShiftHourRange[hour]]

    def __getCorrelationMatrix(self, data:pd.DataFrame, magnitude, useNaN = False) -> pd.DataFrame:
        correlation_matrix = data.select_dtypes(include='number').corr()
        mask = correlation_matrix.abs() >= magnitude
        correlation_matrix = correlation_matrix.where(mask)
        if not useNaN:
            correlation_matrix = correlation_matrix.fillna(0)
        return correlation_matrix

    def __restart(self) -> None:
        self.df = self.df_goal.copy()

    def GetData(self, date, shift:int, shiftHour:int, magnitude:int) -> pd.DataFrame:
        data_in_hour = []
        # Filtering by day and shift
        self.__filterByDate(date)
        self.__filterByShift(shift)
        data = self.__filterByHour(shiftHour)
        corr_matrix = self.__getCorrelationMatrix(data, magnitude, True)
        correlation_variables = corr_matrix.columns
        for column in correlation_variables:
            for row in correlation_variables:
                value = round(corr_matrix[column][row], 6)
                if not np.isnan(value) and column != row:
                    data_in_hour.append({
                        'datetime': self.selectedDate,
                        'source': column,
                        'target': row,
                        'weight': value
                    })
        self.__restart()
        return pd.DataFrame(data_in_hour)

    def GetDates(self):
        return self.df['date_time'].dt.date.unique()