# agents/narration_agent.py
from tools.narration_tool import NarrationTool

class NarrationAgent:
    def __init__(self):
        self.tool = NarrationTool()

    def describe(self, df):
        return self.tool.generate_summary(df)
