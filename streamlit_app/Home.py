
import streamlit as st
import pandas as pd
import random
import markdown2

# Streamlit page config
st.set_page_config(page_title="macRAG SecCopilot", layout="wide")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🏠 Home", "💬 Chat", "🧠 Mindmap"])

# --- HOME TAB ---
with tab1:
    st.title("macRAG SecCopilot Dashboard")
    st.markdown("AI-assisted analysis of security incidents with threat scoring and response optimization.")

    # Sample data
    df = pd.DataFrame({
        "Timestamp": ["2025-05-01 08:30", "2025-05-01 08:35", "2025-05-01 08:40"],
        "Event": ["SSH access detected", "Config file modified", "Root access granted"],
        "Severity": ["High", "Medium", "Critical"]
    })

    st.markdown("### 🚨 Incident Timeline")
    for _, row in df.iterrows():
        with st.expander(f"{row['Timestamp']} - {row['Event']}"):
            st.write(f"Severity: {row['Severity']}")

    st.markdown("### 📊 Risk Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Threat Score", f"{random.uniform(90, 99):.2f}%", "Critical")
    col2.metric("Risk Score", f"{random.uniform(80, 95):.2f}%", "High")
    col3.metric("MTTD", f"{random.randint(1, 4)} hours")
    col4.metric("Recommended MTTR", "Hours")

# --- CHAT TAB ---
with tab2:
    st.markdown("### 💬 Chat with SecCopilot")
    question = st.text_input("Ask your question about the incident:")
    if question:
        st.write("🤖 Copilot says:")
        st.success("Based on the logs, this incident likely originated from a misconfigured firewall rule exposing SSH.")

# --- MINDMAP TAB ---
with tab3:
    st.markdown("### 🧠 Incident Mindmap")

    # Create mock mindmap markdown
    markdown_text = '''
# Incident Mindmap
## Summary
- SSH brute-force attempt detected
- Root access granted
## Timeline
- 08:30 - SSH access
- 08:35 - Config modified
- 08:40 - Root login
## Recommendations
- Revoke credentials
- Patch access rules
- Enable MFA
'''

    st.markdown(markdown2.markdown(markdown_text))

    mindmap_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader"></script>
    </head>
    <body>
        <svg id="mindmap"></svg>
        <script>
            window.markmap.autoLoader.render("mindmap", `{markdown_text}`);
        </script>
    </body>
    </html>
    '''
    st.download_button("📥 Download Mindmap (HTML)", mindmap_html.encode("utf-8"), "incident_mindmap.html", "text/html")
