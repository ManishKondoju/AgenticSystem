from transformers import pipeline
import pandas as pd

class ChatAgent:
    def __init__(self, df: pd.DataFrame):
        # Convert all values to string to avoid Tapas dtype issues
        self.df = df.head(20).astype(str)
        self.qa_pipeline = pipeline("table-question-answering", model="google/tapas-large-finetuned-wtq")

    def answer(self, question: str) -> str:
        try:
            result = self.qa_pipeline(table=self.df, query=question)
            return result['answer']
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
