import pandas as pd

class StatsAgent:
    def __init__(self):
        self.name = "StatsAgent"

    def analyze(self, df: pd.DataFrame):
        description = df.describe(include='all').transpose()
        correlation = df.corr(numeric_only=True)
        return {
            "description": description,
            "correlation": correlation
        }
