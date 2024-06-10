import pandas as pd
import numpy as np
from datetime import time

HOURS_IN_SHIFT = 1440

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
        elif shiftAsInt == 2:
            return 'Shift_II'
        elif shiftAsInt == 3:
            return 'Shift_III'
        else:
            raise Exception('__setHourShiftRange: shift should be [1,2,3]')

    def __filterByDate(self, date) -> None:
        self.selectedDate = pd.to_datetime(date).date()
        self.df = self.df[self.df['date_time'].dt.date == self.selectedDate]

    def __setHourShiftRange(self, shiftAsInt: int) -> None:

        #shift I
        start_I = 6*60
        end_I = 13*60 + 59
        numbers_range_I = range(start_I, end_I + 1)
        shift_I_minutes = list(numbers_range_I)
        #shift II
        start_II = 14*60
        end_II = 21*60 + 59
        numbers_range_II = range(start_II, end_II + 1)
        shift_II_minutes = list(numbers_range_II)
        #shift III
        start_IIIa = 22*60
        end_IIIa = 23*60 + 59
        numbers_range_IIIa = range(start_IIIa, end_IIIa + 1)

        start_IIIb = 0*60
        end_IIIb = 5*60 + 59
        numbers_range_IIIb = range(start_IIIb, end_IIIb + 1)

        shift_III_minutes = list(numbers_range_IIIa) + list(numbers_range_IIIb)

        if shiftAsInt == 1:
            self.selectedShiftHourRange = shift_I_minutes
        elif shiftAsInt == 2:
            self.selectedShiftHourRange = shift_II_minutes
        elif shiftAsInt == 3:
            self.selectedShiftHourRange = shift_III_minutes
        else:
            raise Exception('__setHourShiftRange: shift should be [1,2,3]')

    def __filterByShift(self, shiftAsInt: int) -> None:
        self.__setHourShiftRange(shiftAsInt)
        self.selectedShift = self.__shiftIntToString(shiftAsInt)
        self.df = self.df[self.df['shift'] == self.selectedShift]

    def __filterByHour(self, hour:int) -> pd.DataFrame:
        copy = self.df.copy()
        hour = 0 if hour >= HOURS_IN_SHIFT else hour
        return copy[(copy['date_time'].dt.hour*60 + copy['date_time'].dt.minute) == self.selectedShiftHourRange[hour]]

    def __getCorrelationMatrix(self, data:pd.DataFrame, magnitude: float, useNaN = False) -> pd.DataFrame:
        correlation_matrix = data.select_dtypes(include='number').corr()
        mask = correlation_matrix.abs() >= magnitude
        correlation_matrix = correlation_matrix.where(mask)
        if not useNaN:
            correlation_matrix = correlation_matrix.fillna(0)
        return correlation_matrix

    def __restart(self) -> None:
        self.df = self.df_goal.copy()

    def GetData(self, date, shift:int, shiftHour:int, magnitude:float) -> pd.DataFrame:
        # Filtering by day and shift
        self.__filterByDate(date)
        self.__filterByShift(shift)
        data = self.__filterByHour(shiftHour)
        corr_matrix = self.__getCorrelationMatrix(data, magnitude, False)
        self.__restart()
        return corr_matrix

    def GetDates(self):
        return self.df['date_time'].dt.date.unique()