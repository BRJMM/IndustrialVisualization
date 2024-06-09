import pandas as pd

class MachineSelector:
    def __init__(self, filepath) -> None:
        self.df_raw = pd.read_csv(filepath)

    def __dataPreparation(self) -> pd.DataFrame:
        self.df_raw_share_columns = self.df_raw[self.df_raw.columns[:3]]
        self.df_raw = self.df_raw.melt(self.df_raw.columns[:3], var_name='drumpress', value_name='value')
        self.df_raw[['drumpress','variable']] = self.df_raw['drumpress'].str.split(pat='_',n=1,expand=True)
        return self.df_raw

    def ExecuteSelection(self, machine:str) -> str:
        df_prep = self.__dataPreparation()
        machines = ['primary','secondary']
        if machine in machines:
            df_machine = df_prep[df_prep.drumpress == machine]
            df_machine = df_machine.pivot(index='date_time',columns='variable',values='value')
            df_machine = self.df_raw_share_columns.merge(df_machine,right_index=True, left_on='date_time')
            output_path = f'./{machine}_drumpress_db.csv'
            df_machine.to_csv(output_path, index=False)
            return output_path
        else:
            raise Exception('The inserted machine is not in the data frame')