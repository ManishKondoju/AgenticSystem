import pandas as pd
import plotly.graph_objects as go
from scipy.stats import zscore

class AnomalyDetectorTool:
    def detect_anomalies(self, df, column):
        df_copy = df.copy()

        # Compute z-scores only for non-null values
        z_scores = zscore(df_copy[column].dropna())
        df_copy.loc[df_copy[column].notna(), 'z_score'] = z_scores
        df_copy['anomaly'] = (df_copy['z_score'].abs() > 3)

        # Plotly visualization
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_copy.index,
            y=df_copy[column],
            mode='lines+markers',
            name='Data',
            line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=df_copy[df_copy['anomaly']].index,
            y=df_copy[df_copy['anomaly']][column],
            mode='markers',
            name='Anomalies',
            marker=dict(color='red', size=10, symbol='x')
        ))
        fig.update_layout(
            title=f"Z-Score Based Anomaly Detection for '{column}'",
            xaxis_title="Index",
            yaxis_title=column,
            showlegend=True
        )

        return df_copy, fig
