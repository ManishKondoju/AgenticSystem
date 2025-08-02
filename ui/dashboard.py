import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import io
import streamlit as st
import pandas as pd
from agents.controller_agent import ControllerAgent
from agents.stats_agent import StatsAgent
from agents.visualization_agent import VisualizationAgent
from agents.anomaly_agent import AnomalyAgent
from agents.chat_agent import ChatAgent
from agents.data_quality_agent import DataQualityAgent
from agents.feature_generation_agent import FeatureGenerationAgent
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.express as px
import plotly.graph_objects as go

# 📌 Custom CSS Styling - Dark Themed Flip Cards
st.set_page_config(page_title="📊 Smart Data Analyzer", layout="wide")
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Helvetica', sans-serif;
            background-color: #1e1e1e;
            color: #f5f5f5;
        }

        h1, h2, h3 {
            font-family: 'Helvetica', sans-serif;
            color: #f5f5f5;
        }

        .block-container {
            padding-top: 2rem;
        }

        .stTabs [role="tab"] {
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 20px;
            margin-right: 8px;
            background-color: #2e2e2e;
            color: #ccc;
            transition: all 0.3s ease-in-out;
            border: none;
        }

        .stTabs [role="tab"]:hover {
            background-color: #444;
            color: #fff;
            transform: scale(1.03);
            cursor: pointer;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(to right, #1a2a6c, #b21f1f);
            color: white !important;
            font-weight: bold;
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        .hero-section {
            padding: 3rem;
            text-align: center;
            background: #121212;
            border-radius: 14px;
            color: white;
            margin-bottom: 3rem;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
            margin-bottom: 2rem;
            perspective: 1000px;
        }

        .flip-card {
            background-color: transparent;
            width: 100%;
            height: 200px;
            perspective: 1000px;
        }

        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.6s;
            transform-style: preserve-3d;
        }

        .flip-card:hover .flip-card-inner {
            transform: rotateY(180deg);
        }

        .flip-card-front, .flip-card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            background: #2e2e2e;
            padding: 1rem;
            color: #f5f5f5;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-direction: column;
        }

        .flip-card-back {
            transform: rotateY(180deg);
            background: #3a3a3a;
            color: #f5f5f5;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------ Main App ------------------
st.title("📊 Smart Data Analyzer")

st.markdown("""
<div class="hero-section">
    <h2>Welcome to Smart Data Analyzer 🚀</h2>
    <p>This project helps data analysts easily clean, explore, visualize, and extract insights from CSV datasets using AI agents and interactive components.</p>
    <div class="features-grid">
        <div class="flip-card"><div class="flip-card-inner">
            <div class="flip-card-front">🪜<br/>Auto Data Cleaning</div>
            <div class="flip-card-back">Automatically fix missing values, standardize data types, and remove inconsistencies.</div>
        </div></div>
        <div class="flip-card"><div class="flip-card-inner">
            <div class="flip-card-front">📈<br/>Summary Stats</div>
            <div class="flip-card-back">Quickly generate descriptive statistics for numeric and categorical features.</div>
        </div></div>
        <div class="flip-card"><div class="flip-card-inner">
            <div class="flip-card-front">📊<br/>Visualizations</div>
            <div class="flip-card-back">Create bar, scatter, pie charts, and drilldown visualizations in one click.</div>
        </div></div>
        <div class="flip-card"><div class="flip-card-inner">
            <div class="flip-card-front">🚨<br/>Anomaly Detection</div>
            <div class="flip-card-back">Detect outliers using z-score or Isolation Forest techniques.</div>
        </div></div>
        <div class="flip-card"><div class="flip-card-inner">
            <div class="flip-card-front">📋<br/>Data Quality Report</div>
            <div class="flip-card-back">Assess dataset quality via profiling metrics and validation rules.</div>
        </div></div>
        <div class="flip-card"><div class="flip-card-inner">
            <div class="flip-card-front">💬<br/>Chat with CSV</div>
            <div class="flip-card-back">Ask questions in natural language and get LLM-based insights instantly.</div>
        </div></div>
        <div class="flip-card"><div class="flip-card-inner">
            <div class="flip-card-front">➕<br/>Feature Generator</div>
            <div class="flip-card-back">Generate mathematical or temporal derived columns in a few clicks.</div>
        </div></div>
        <div class="flip-card"><div class="flip-card-inner">
            <div class="flip-card-front">🧪<br/>Interactive Playground</div>
            <div class="flip-card-back">Drag, group, and explore data dynamically using smart grids.</div>
        </div></div>
    </div>
</div>
""", unsafe_allow_html=True)

#uploaded_file = st.file_uploader("Upload a CSV file to get started", type=["csv"])
uploaded_file = st.file_uploader("Upload a CSV file to get started", type=["csv"])

if uploaded_file is not None:
    try:
        # Read bytes from uploaded file and decode safely
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        df = pd.read_csv(stringio)

        if df.empty or df.columns.size == 0:
            st.error("❌ Uploaded CSV has no data or no columns.")
            st.stop()

        st.success("✅ File uploaded successfully!")

    except pd.errors.EmptyDataError:
        st.error("❌ The uploaded CSV file is empty or unreadable.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Failed to read CSV: {e}")
        st.stop()

# -------------------- MAIN INTERFACE --------------------

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("🔍 Raw Data Preview")
    st.dataframe(df.head())

    controller = ControllerAgent()
    cleaned_df, logs = controller.execute(df)

    stats_agent = StatsAgent()
    stats = stats_agent.analyze(cleaned_df)

    vis_agent = VisualizationAgent()
    anomaly_agent = AnomalyAgent()
    chat_agent = ChatAgent(cleaned_df)
    quality_agent = DataQualityAgent()
    feature_agent = FeatureGenerationAgent()

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "🧹 Cleaned Data", "📈 Summary Stats", "🔗 Correlation",
        "📊 Visualizations", "🧪 Data Playground", "🚨 Anomaly Detection",
        "💬 Chat with CSV", "📋 Data Quality Report", "➕ Feature Generator"
    ])

    with tab1:
        st.dataframe(cleaned_df)

    with tab2:
        st.dataframe(stats["description"])

    with tab3:
        st.dataframe(stats["correlation"])

    with tab4:
        st.markdown("### 📊 Generate Custom Visualizations")
        numeric_cols = cleaned_df.select_dtypes(include="number").columns.tolist()
        cat_cols = cleaned_df.select_dtypes(include="object").columns.tolist()
        x_axis = st.selectbox("Select X-axis", options=numeric_cols + cat_cols)
        y_axis = st.selectbox("Select Y-axis (bar/scatter)", options=numeric_cols)
        chart_type = st.selectbox("Chart Type", ["Bar Chart", "Scatter Plot", "Pie Chart"])
        if st.button("Generate Chart"):
            if chart_type == "Bar Chart":
                fig = vis_agent.tool.create_custom_bar_chart(cleaned_df, x_axis, y_axis)
            elif chart_type == "Scatter Plot":
                fig = vis_agent.tool.create_custom_scatter_plot(cleaned_df, x_axis, y_axis)
            elif chart_type == "Pie Chart":
                fig = vis_agent.tool.create_custom_pie_chart(cleaned_df, x_axis)
            st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.markdown("### 🧪 Interactive Data Playground")
        gb = GridOptionsBuilder.from_dataframe(cleaned_df)
        gb.configure_pagination()
        gb.configure_default_column(editable=True, groupable=True)
        grid_options = gb.build()
        AgGrid(cleaned_df, gridOptions=grid_options, enable_enterprise_modules=False, height=400)

        st.markdown("#### 🔀 Group and Aggregate")
        group_col = st.selectbox("Group by column", options=cleaned_df.columns)
        agg_col = st.selectbox("Aggregate column", options=cleaned_df.select_dtypes(include='number').columns)
        agg_func = st.selectbox("Aggregation", ["sum", "mean", "count", "min", "max"])
        if st.button("Apply Grouping"):
            grouped = cleaned_df.groupby(group_col)[agg_col].agg(agg_func).reset_index()
            st.dataframe(grouped)
            st.plotly_chart(px.bar(grouped, x=group_col, y=agg_col, title=f"{agg_func.title()} of {agg_col} by {group_col}"), use_container_width=True)

    with tab6:
        st.markdown("### 🚨 Anomaly Detection")
        anomaly_col = st.selectbox("Column for anomaly detection", options=cleaned_df.select_dtypes(include='number').columns)
        if st.button("Detect Anomalies"):
            result_df, fig = anomaly_agent.detect(cleaned_df, anomaly_col)
            st.dataframe(result_df)
            st.plotly_chart(fig, use_container_width=True)

    with tab7:
        st.markdown("### 💬 Chat with CSV (LLM-powered)")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        user_input = st.chat_input("Ask a question about your data...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            response = chat_agent.answer(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

    with tab8:
        st.markdown("### 📋 Data Quality Report")
        report = quality_agent.generate_report(cleaned_df)
        st.dataframe(report)

    with tab9:
        st.markdown("### ➕ Derived Feature Generator")
        columns = cleaned_df.columns.tolist()
        feature_type = st.radio("Feature Type", ["Math", "Date"])
        if feature_type == "Math":
            col1 = st.selectbox("Select Column 1", options=columns)
            operation = st.selectbox("Operation", ["+", "-", "*", "/"])
            col2 = st.selectbox("Select Column 2", options=columns)
            new_col = st.text_input("New Column Name")
            if st.button("Generate Feature"):
                new_df = feature_agent.create_math_feature(cleaned_df, col1, col2, operation, new_col)
                cleaned_df[new_col] = new_df[new_col]
                st.success(f"Feature '{new_col}' created!")
                st.dataframe(cleaned_df.head())
        else:
            date_col = st.selectbox("Select Date Column", options=columns)
            date_part = st.selectbox("Date Part", ["year", "month", "day", "weekday"])
            new_col = st.text_input("New Column Name")
            if st.button("Extract Date Part"):
                new_df = feature_agent.create_date_feature(cleaned_df, date_col, date_part, new_col)
                cleaned_df[new_col] = new_df[new_col]
                st.success(f"Feature '{new_col}' created!")
                st.dataframe(cleaned_df.head())

    with st.expander("🧠 System Logs"):
        for log in logs:
            st.text(log)
