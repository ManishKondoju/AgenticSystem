import pandas as pd
from transformers import pipeline

class NarrationTool:
    def __init__(self):
        self.model_id = "tiiuae/falcon-rw-1b"
        try:
            self.pipe = pipeline("text-generation", model=self.model_id, max_new_tokens=120)
        except Exception as e:
            print(f"❌ Model loading failed: {e}")
            self.pipe = None

    def generate_summary(self, df: pd.DataFrame) -> str:
        if self.pipe is None:
            return "🚫 Model not loaded. Summary not available."

        try:
            num_rows, num_cols = df.shape
            sample_columns = ", ".join(df.columns[:5]) + ("..." if len(df.columns) > 5 else "")
            types_raw = df.dtypes.value_counts().to_dict()
            types = ", ".join([f"{v} {str(k).split('.')[-1]} columns" for k, v in types_raw.items()])

            prompt = (
                f"The dataset has {num_rows} rows and {num_cols} columns. "
                f"Example columns are: {sample_columns}. "
                f"Column types: {types}. "
                f"What is this dataset about and how might it be used? Give a short paragraph."
            )

            print("🟡 Prompt to model:\n", prompt)
            output = self.pipe(prompt)
            summary = output[0]["generated_text"]
            print("✅ Model response:\n", summary)
            return summary.strip()

        except Exception as e:
            print(f"⚠️ Summary generation failed: {e}")
            return "⚠️ Summary generation failed."
