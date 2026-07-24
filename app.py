import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Serverless AutoML Stream Engine", layout="wide")

st.title("Serverless AutoML Stream Pipeline")
st.caption("Real-Time Data Stream Mining & Dynamic Hyperparameter Optimization")

st.sidebar.header("Stream Mining Configuration")
selected_stream = st.sidebar.selectbox("High-Velocity Data Stream", ["Global Supply Chain IoT Telemetry", "High-Frequency Financial Ticks", "Smart Grid Energy Load"])
volatility_shock = st.sidebar.slider("Simulate Data Volatility (Concept Drift)", 1.0, 5.0, 3.5)
run_simulation = st.sidebar.button("Initialize Serverless AutoML Engine")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: Stream Replication -> AWS Lambda Parallel Eval -> Hot-Swap")

if run_simulation:
    st.subheader(f"Active Continuous Learning Model: {selected_stream}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_velocity = col1.empty()
    metric_base_acc = col2.empty()
    metric_auto_acc = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(1414)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    base_accuracy = []
    automl_accuracy = []
    learning_rates = []
    
    current_base = 92.0
    current_auto = 92.0
    current_lr = 0.01
    
    for i in range(100):
        velocity = int(np.random.uniform(20000, 35000))
        
        if i < 30:
            current_base = 92.0 + np.random.uniform(-1.0, 1.0)
            current_auto = 92.5 + np.random.uniform(-0.8, 0.8)
            current_lr = 0.01
            status = "STATIONARY STREAM"
        elif i >= 30 and i < 60:
            current_base = current_base - (1.5 * volatility_shock) + np.random.uniform(-2.0, 2.0)
            current_auto = current_auto - (0.5 * volatility_shock) + np.random.uniform(-1.0, 1.0)
            current_lr = 0.05 + np.random.uniform(-0.01, 0.01)
            status = "DRIFT DETECTED - EVALUATING"
        else:
            current_base = current_base + np.random.uniform(-1.5, 1.5)
            current_auto = min(96.0, current_auto + 2.0 + np.random.uniform(-0.5, 0.5))
            current_lr = 0.02 + np.random.uniform(-0.005, 0.005)
            status = "AUTOML OPTIMIZED"
            
        base_accuracy.append(max(0, current_base))
        automl_accuracy.append(current_auto)
        learning_rates.append(current_lr)
        
        metric_velocity.metric("Stream Velocity", f"{velocity:,} Nodes/s")
        metric_base_acc.metric("Static Model Accuracy", f"{max(0, current_base):.1f}%")
        metric_auto_acc.metric("AutoML Optimized Accuracy", f"{current_auto:.1f}%", f"+{(current_auto - max(0, current_base)):.1f}% Yield")
        
        if status == "DRIFT DETECTED - EVALUATING":
            metric_status.metric("Serverless Orchestration", status, "Spawning AWS Lambdas")
        elif status == "AUTOML OPTIMIZED":
            metric_status.metric("Serverless Orchestration", status, "Hot-Swap Complete")
        else:
            metric_status.metric("Serverless Orchestration", status, "Normal")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=base_accuracy, mode='lines', name='Static Hyperparameters', line=dict(color='gray', dash='dash')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=automl_accuracy, mode='lines', name='Serverless AutoML Config', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=learning_rates, mode='lines', name='Dynamic Learning Rate', yaxis='y2', line=dict(color='purple', dash='dot')))
        
        fig.update_layout(
            title="Data Stream Mining: Static vs Automated Machine Learning (AutoML) Adaptation",
            xaxis=dict(title="High-Frequency Stream Timestamp"),
            yaxis=dict(title="Predictive Accuracy (%)", range=[min(50, min(base_accuracy)-10), 100]),
            yaxis2=dict(title="Active Learning Rate", overlaying='y', side='right', range=[0, 0.1]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if status == "DRIFT DETECTED - EVALUATING":
            log_placeholder.warning(f"AUTOML ALERT: Severe volatility detected at {time_steps[i].strftime('%H:%M:%S')}. Duplicating data stream. Spawning 50 ephemeral AWS Lambda nodes for parallel hyperparameter evaluation.")
        elif status == "AUTOML OPTIMIZED" and i == 60:
            log_placeholder.success(f"ORCHESTRATION SUCCESS: Optimal configuration identified. Dynamic hot-swap executed without blocking ingestion pipeline. Accuracy recovering.")
        elif status == "STATIONARY STREAM" and i % 5 == 0:
            log_placeholder.info(f"Log: Telemetry tick {i} ingested. Primary inference engine operating at stable baseline efficiency.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The serverless cloud pipeline successfully executed Automated Machine Learning on data in motion, preventing predictive collapse.")
else:
    st.info("Click 'Initialize Serverless AutoML Engine' in the sidebar to simulate dynamic optimization of streaming data.")