# ✅ FIXED Home.py - Custom Query Input Now Persists
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import folium
from streamlit.components.v1 import html
from pyvis.network import Network
from langchain.llms import Ollama
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json, os
from datetime import datetime
import requests

# --- Page Config ---
st.set_page_config(page_title="Security Investigator Copilot", layout="wide")

# --- Determine LLM URL (Docker-aware) ---
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")  # fallback for containers
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Sidebar ---
st.sidebar.title("🔐 SecCopilot Navigation")
st.sidebar.markdown("Use this panel to control data, LLMs, and views.")
llm_mode = st.sidebar.radio("Choose LLM Mode:", ["Local (Ollama)", "Cloud (OpenAI)"])
if st.sidebar.button("🔄 Regenerate Visual Files"):
    st.experimental_rerun()
if st.sidebar.button("📥 Download Prompt Log (CSV)"):
    try:
        logs = [json.loads(line) for line in open("query_log.json")]
        df = pd.DataFrame(logs)
        csv = df.to_csv(index=False).encode("utf-8")
        st.sidebar.download_button("Download CSV", csv, "prompt_log.csv", "text/csv")
    except Exception as e:
        st.sidebar.error("Log file not found or empty.")

# --- Tab Selector ---
tab = st.selectbox("Choose Section", ["Dashboard", "LLM Explorer", "Log Viewer"])

# Global Sample Data
data = pd.DataFrame({
    "User": ["alice", "bob", "charlie"],
    "Role": ["admin", "viewer", "editor"],
    "Service": ["S3", "EC2", "IAM"],
    "Access Level": ["Full", "Read", "Write"],
    "Risk Score": [85, 60, 75],
    "Location": ["Ashburn, VA", "Frankfurt, DE", "Singapore"],
    "Last Login": ["2024-05-27", "2024-05-28", "2024-05-28"]
})

# -------------------- TAB 1 --------------------
if tab == "Dashboard":
    st.title("📊 Security Risk Dashboard")
    st.subheader("Step 1: Threat Summary Metrics")
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7 = st.columns(1)[0]

    col1.metric("Threat Score %", "92.8%", "+2.1")
    col2.metric("Risk Score", "87.4", "-1.3")
    col3.metric("R-MMTD", "20 sec")
    col4.metric("R-MMTR", "65 min")
    col5.metric("Systems Impacted", "12")
    col6.metric("Users Impacted", "28")
    col7.metric("$ Value Impact", "$1,344", "$48/user")

    st.subheader("Step 2: IAM Entity Graph")
    with st.expander("Show Interactive Graph"):
        try:
            with open("streamlit_app/interactive_graph.html", 'r') as f:
                html(f.read(), height=500)
        except:
            st.warning("interactive_graph.html not found in streamlit_app/")

    st.subheader("Step 3: IAM Dataset View")
    st.dataframe(data, use_container_width=True)

    st.subheader("Step 4: Geo Attribution Map")
    with st.expander("Show Map"):
        try:
           with open("streamlit_app/geo_map.html", 'r') as f:
                html(f.read(), height=500)
        except:
            st.warning("geo_map.html not found in streamlit_app/")

# -------------------- TAB 2 --------------------
elif tab == "LLM Explorer":
    st.header("🤖 Step 5: LLM Data Exploration")
    example_queries = [
        "Which user has the highest risk score?",
        "List users with Full access",
        "How many users accessed IAM service?",
        "Which role has the most risky users?",
        "What is the average risk score by location?"
    ]

    query_choice = st.selectbox("Choose a preset query or write your own:", ["Custom..."] + example_queries)
    if query_choice == "Custom...":
        user_query = st.text_area("Type your custom security query:", key="custom_query")
    else:
        user_query = query_choice

    prompt = PromptTemplate.from_template(
        """
        You are an expert IAM security analyst. Based on the following CSV dataset:

        {data}

        Answer the user's question: {question}
        """
    )

    if st.button("Run Local SecPilot"):
        if user_query.strip():
            with st.spinner("Running selected LLM model..."):
                try:
                    if llm_mode == "Local (Ollama)":
                        if not requests.get(OLLAMA_HOST).ok:
                            raise ValueError("Ollama endpoint unreachable")
                        llm = Ollama(base_url=OLLAMA_HOST, model="mistral")
                    else:
                        if not OPENAI_API_KEY:
                            raise ValueError("Missing OpenAI API Key in environment.")
                        llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)

                    chain = LLMChain(llm=llm, prompt=prompt)
                    result = chain.run(data=data.to_csv(index=False), question=user_query)
                    st.success("Response:")
                    st.write(result)

                    log = {
                        "timestamp": datetime.now().isoformat(),
                        "query": user_query,
                        "response": result,
                        "mode": llm_mode
                    }
                    with open("query_log.json", "a") as f:
                        f.write(json.dumps(log) + "\n")

                except Exception as e:
                    st.error(f"❌ LLM connection failed: {e}")
        else:
            st.warning("Please enter a question.")

# -------------------- TAB 3 --------------------
elif tab == "Log Viewer":
    st.header("📑 LLM Prompt History")
    try:
        with open("query_log.json") as f:
            logs = [json.loads(line) for line in f if line.strip()]
            df = pd.DataFrame(logs)
            st.dataframe(df, use_container_width=True)
    except:
        st.warning("No prompt history found. Run some queries first.")
