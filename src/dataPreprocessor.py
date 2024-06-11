import pandas as pd
from datetime import time, timedelta

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
        elif shiftAsInt == 2:
            return 'Shift_II'
        elif shiftAsInt == 3:
            return 'Shift_III'
        else:
            raise Exception('__setHourShiftRange: shift should be [1,2,3]')

    def __filterByDate(self, date) -> None:
        self.df['only_date'] = self.df['date_time'].dt.date
        self.df.loc[(self.df['date_time'].dt.time >= time(0,0,0)) & 
                      (self.df['date_time'].dt.time < time(6,0,0)),'only_date'] = self.df['only_date'] - timedelta(days=1)
        self.selectedDate = pd.to_datetime(date).date()
        self.df = self.df[self.df['only_date'] == self.selectedDate]

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
        hour = 0 if hour >= HOURS_IN_SHIFT else hour
        return copy[copy['date_time'].dt.hour == self.selectedShiftHourRange[hour]]

    def __getCorrelationMatrix(self, data:pd.DataFrame, magnitude: float, useNaN = False) -> pd.DataFrame:
        correlation_matrix = data.select_dtypes(include='number').corr()
        mask = correlation_matrix.abs() >= magnitude
        correlation_matrix = correlation_matrix.where(mask)
        if not useNaN:
            correlation_matrix = correlation_matrix.fillna(0)
        return correlation_matrix
    
    def __filterByRunning(self,active=False):
        if active:
            self.df = self.df[self.df['runautomode_bool'] == 't']
        else:
            pass

    def __restart(self) -> None:
        self.df = self.df_goal.copy()

    def GetData(self, date, shift:int, shiftHour:int, magnitude:float, runningFilter=False) -> pd.DataFrame:
        # Filtering by day and shift
        self.__filterByDate(date)
        self.__filterByShift(shift)
        self.__filterByRunning(runningFilter)
        data = self.__filterByHour(shiftHour)
        corr_matrix = self.__getCorrelationMatrix(data, magnitude, False)
        self.__restart()
        return corr_matrix

    def GetDates(self):
        return self.df['date_time'].dt.date.unique()