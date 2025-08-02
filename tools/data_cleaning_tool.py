import pandas as pd

class DataCleaningTool:
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.dropna(axis=0, how='all', inplace=True)
        df.fillna(method='ffill', inplace=True)
        return df
