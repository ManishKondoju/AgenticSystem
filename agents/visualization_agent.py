import pandas as pd
from tools.visualization_tool import VisualizationTool

class VisualizationAgent:
    def __init__(self):
        self.tool = VisualizationTool()

    def generate_all(self, df: pd.DataFrame):
        return {
            "bar": self.tool.create_bar_chart(df),
            "pie": self.tool.create_pie_chart(df),
            "scatter": self.tool.create_scatter_plot(df),
            "heatmap": self.tool.create_correlation_heatmap(df)
        }
