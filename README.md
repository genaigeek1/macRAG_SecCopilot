# 🛡️ macRAG SecCopilot

**macRAG SecCopilot** is a local, containerized **Retrieval-Augmented Generation (RAG)**-based AI Security Investigator designed to streamline the process of **security incident triage**, **alert analysis**, and **mean time to resolution (MTTR)** reduction.

---

## 📌 Key Benefits

- 🧠 **AI-augmented Chat** for incident interpretation
- 📊 **Risk Scoring** and **Anomaly Detection**
- 🗺️ **Markdown to Mindmap** generation for incident reports
- ⏱️ **MTTD/MTTR analytics** for leadership dashboards
- 🐳 **Self-healing Dockerized Setup** for Apple Silicon

---

## 🧠 Architecture

![macRAG Architecture](./docs/ragaidemo.png)

---

## 🚀 How to Run (Docker)

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Clean up existing containers
- Download Ollama + LLMs
- Launch Streamlit app at `http://localhost:8501`

---

## 🔍 Features Overview

| Feature                    | Description |
|----------------------------|-------------|
| 🔐 AI Assistant            | Ask “What happened before the alert?” or “How to prevent this?” |
| 📄 Markdown Summary        | LLM-generated incident summary |
| 🧠 Mindmap Export          | Visualize incident story as interactive mindmap |
| 📈 Risk Score              | Classifies threat severity |
| ⏱️ MTTR Metrics            | Auto-derived Mean Time To Detect / Resolve |
| 🛠️ Streamlit Tabs          | Home, Chat, Mindmap, Report |
| 🐳 Docker Ready            | Self-healing, fast rebuilds, Apple Silicon optimized |
| 🧪 Supports multiple LLMs  | Ollama, OpenAI, etc. via `.env` toggle |

---

## ⚙️ Configuration (.env)

Create a `.env` file or modify `.env.example`:

```env
LLM_BACKEND=ollama
VECTOR_DB=faiss
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
STREAMLIT_SERVER_PORT=8501
OPENAI_API_KEY=your-key-here  # (if using OpenAI backend)
```

---

## 📂 Directory Structure

```text
├── docker-compose.yml
├── setup.sh
├── .env.example
├── streamlit_app/
│   ├── Home.py
│   ├── chat.py
│   ├── report_mindmap.py
│   └── ...
├── src/
│   ├── loaders/
│   ├── chunkers/
│   ├── parsers/
│   └── utils/
├── data/
│   ├── mock_security_incidents.csv
│   └── ...
├── notebooks/
│   └── threat_analysis.ipynb
└── README.md  ← you are here
```

---

## 📥 Download Incident Mindmap

Click `📥 Generate Mindmap` in the Streamlit app to download `.html` and open in Chrome.

---

## 🧠 Example Use Cases

- Reducing **SOC analyst fatigue** with guided interpretation
- Helping CISO teams quantify **alert impact**
- Quickly reviewing **threat narratives** across time
- Integrating with **CloudTrail / Syslog / Sentinel** alerts

---

## 🧠 Step 1: Try These Security Investigation Chat Prompts

Here’s a curated list of smart, realistic questions you can ask in the Chat section of **macRAG SecCopilot** to simulate stakeholder usage or demonstrate LLM-powered investigation value:

---

### 🔍 Threat Investigation Questions
- “What happened before this alert?”
- “Why is this login attempt flagged?”
- “Was this IP seen in past incidents?”
- “Show me events 5 minutes before and after the alert.”
- “When did the suspicious user activity start?”
- “Where was this user logged in from?”
- “Has this user ever accessed from this country before?”
- “Which sensitive files were accessed?”
- “Was data exfiltration attempted?”

### 🛡️ Severity & Risk
- “What is the risk score of this incident?”
- “What factors increased the risk?”
- “Is this a false positive?”
- “How severe is this threat compared to others today?”

### 🛠 Remediation Guidance
- “How can we prevent this type of alert?”
- “What controls should be enabled?”
- “Which playbook applies here?”
- “Recommend a response plan.”

### 📊 Incident Report Summary
- “Summarize this incident.”
- “Explain this alert like I’m a CISO.”
- “How often does this type of alert occur?”
- “Is this part of a pattern?”

### 🧠 Bonus Smart Prompts
- “Link this alert to any past similar alerts.”
- “What user behaviors preceded this event?”
- “Generate a mindmap for this threat.”

---

## 📈 Future Enhancements

- LangSmith + Weights & Biases observability
- NIST tagging and MITRE ATT&CK classification
- CI/CD integration and test automation

---

## 🤝 Contributors

Built by [Saurabh Chhatwal](https://www.linkedin.com/in/genaigeek/), powered by LangChain and OLLAMA

---

## 🛑 License

MIT License — use freely with attribution.