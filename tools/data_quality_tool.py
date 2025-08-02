import pandas as pd

class DataQualityTool:
    def generate_report(self, df: pd.DataFrame) -> pd.DataFrame:
        report = pd.DataFrame(index=df.columns)

        report['Data Type'] = df.dtypes
        report['Missing Values'] = df.isnull().sum()
        report['% Missing'] = (df.isnull().sum() / len(df)) * 100
        report['Unique Values'] = df.nunique()
        report['Duplicates'] = df.duplicated().sum()
        report['Constant Column'] = df.nunique() == 1
        report['Mean'] = df.select_dtypes(include='number').mean()
        report['Std Dev'] = df.select_dtypes(include='number').std()
        report['Min'] = df.select_dtypes(include='number').min()
        report['Max'] = df.select_dtypes(include='number').max()

        return report
