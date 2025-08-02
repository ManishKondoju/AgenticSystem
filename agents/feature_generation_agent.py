# agents/feature_generation_agent.py

import pandas as pd

class FeatureGenerationAgent:
    def create_math_feature(self, df, col1, col2, operation, new_col):
        df_copy = df.copy()
        try:
            if operation == '+':
                df_copy[new_col] = df_copy[col1] + df_copy[col2]
            elif operation == '-':
                df_copy[new_col] = df_copy[col1] - df_copy[col2]
            elif operation == '*':
                df_copy[new_col] = df_copy[col1] * df_copy[col2]
            elif operation == '/':
                df_copy[new_col] = df_copy[col1] / df_copy[col2]
        except Exception as e:
            print(f"❌ Error creating math feature: {e}")
        return df_copy

    def create_date_feature(self, df, date_col, part, new_col):
        df_copy = df.copy()
        try:
            df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
            if part == 'year':
                df_copy[new_col] = df_copy[date_col].dt.year
            elif part == 'month':
                df_copy[new_col] = df_copy[date_col].dt.month
            elif part == 'day':
                df_copy[new_col] = df_copy[date_col].dt.day
            elif part == 'weekday':
                df_copy[new_col] = df_copy[date_col].dt.day_name()
        except Exception as e:
            print(f"❌ Error extracting date feature: {e}")
        return df_copy
