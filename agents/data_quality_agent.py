import pandas as pd

class DataQualityAgent:
    def __init__(self):
        pass

    def generate_report(self, df: pd.DataFrame) -> pd.DataFrame:
        report = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes.values,
            'Missing Values': df.isnull().sum().values,
            'Missing %': (df.isnull().sum() / len(df) * 100).round(2).values,
            'Unique Values': df.nunique().values,
            'Min': [df[col].min() if pd.api.types.is_numeric_dtype(df[col]) else '' for col in df.columns],
            'Max': [df[col].max() if pd.api.types.is_numeric_dtype(df[col]) else '' for col in df.columns],
            'Sample Value': [df[col].dropna().iloc[0] if not df[col].dropna().empty else '' for col in df.columns],
        })

        return report
