from tools.anomaly_detector_tool import AnomalyDetectorTool

class AnomalyAgent:
    def __init__(self):
        self.tool = AnomalyDetectorTool()

    def detect(self, df, column):
        return self.tool.detect_anomalies(df, column)
