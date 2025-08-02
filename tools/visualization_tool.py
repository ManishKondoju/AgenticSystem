import plotly.express as px
import pandas as pd

class VisualizationTool:
    def create_custom_bar_chart(self, df, x, y):
        return px.bar(df, x=x, y=y, title=f"Bar Chart: {x} vs {y}")

    def create_custom_scatter_plot(self, df, x, y):
        return px.scatter(df, x=x, y=y, title=f"Scatter Plot: {x} vs {y}")

    def create_custom_pie_chart(self, df, category_col):
        pie_data = df[category_col].value_counts().reset_index()
        pie_data.columns = [category_col, 'count']
        return px.pie(pie_data, names=category_col, values='count', title=f"Pie Chart: {category_col}")
