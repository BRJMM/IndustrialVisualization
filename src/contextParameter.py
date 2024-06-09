class ContextParameter:
    def __init__(self) -> None:
        self.curr_date = ''
        self.curr_shift = ''
        self.curr_corr_threshold = 0.0
        self.curr_corr_change = 0.0

        self.prev_date = ''
        self.prev_shift = ''
        self.prev_corr_threshold = 0.0
        self.prev_corr_change = 0.0

    def __get_prev_str(self) -> str:
        return str(self.prev_date+self.prev_shift+str(self.prev_corr_threshold)+str(self.prev_corr_change))

    def __get_curr_str(self) -> str:
        return str(self.curr_date+self.curr_shift+str(self.curr_corr_threshold)+str(self.curr_corr_change))
    
    def SetState(self, date: str, shift: str, corr_threshold: float, corr_change: float) -> None:
        self.prev_date = self.curr_date
        self.curr_date = date

        self.prev_shift = self.curr_shift
        self.curr_shift = shift

        self.prev_corr_threshold = self.curr_corr_threshold
        self.curr_corr_threshold = corr_threshold

        self.prev_corr_change = self.curr_corr_change
        self.curr_corr_change = corr_change
    
    def HasAnyChanged(self) -> bool:
        return self.__get_prev_str() != self.__get_curr_str()