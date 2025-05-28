# 🛡️ macRAG SecCopilot (Stakeholder Pitch Edition)

macRAG SecCopilot is a local, secure, AI-driven assistant built to reduce **Mean Time To Detect (MTTD)** and **Mean Time To Respond (MTTR)** for security incidents using Retrieval-Augmented Generation (RAG), LangChain, and OpenAI.

---

## 📊 Architecture Overview

![RAG Architecture](docs/ragaidemo.png)

### Key Stages:
1. **Ingest:** Parse logs and incident reports (CloudTrail, Syslog, Microsoft Security).
2. **Retrieve:** Use vector search (FAISS) to find relevant context chunks.
3. **Augment:** Combine query with context to build full prompt.
4. **Generate:** Answer using OpenAI (ChatGPT/GPT-4) or Ollama (LLaMA, Mistral).

---

## 💡 Why It Matters

### 🚀 Business Benefits:
- **Up to 80% faster investigation time** for high-fidelity alerts
- **Data does not leave your machine** (RAG is fully localizable)
- Analysts get actionable summaries, risk scores, and playbooks in seconds

### 📉 Reduces:
- Alert fatigue
- Manual log correlation effort
- Time wasted in triage loops

---

## 🔍 Features Overview

| Feature                 | Description |
|------------------------|-------------|
| 🔥 Threat & Risk Scores | Based on parsed events and severity levels |
| 🧠 LangChain Chat Assistant | Ask “What triggered the alert?” and get a contextual answer |
| 🗂️ Tabbed Streamlit UI  | Home, Chat, Mindmap |
| 📥 Mindmap Generator    | Creates interactive incident mindmaps |
| ⏱️ MTTD & MTTR Estimates | Shows detection and recommended resolution times |
| 📄 Log Parsing          | Supports `.json`, `.csv`, `.log` file uploads |
| 📦 Markdown & HTML Export | Incident summaries exportable for reports |

---

## 🛠️ How to Run

```bash
# Step 1: Add your OpenAI API key to `.env`
cp .env.example .env
# Edit .env and fill in OPENAI_API_KEY=sk-...

# Step 2: Launch the app
./setup.sh
```

Then open [http://localhost:8501](http://localhost:8501)

---

## 🗂 Directory Structure

```
macRAG_SecCopilot/
├── streamlit_app/
│   ├── Home.py
│   ├── Chat.py
│   └── Mindmap.py
├── src/
├── notebooks/
├── data/
├── docs/
│   └── ragaidemo.png
├── .env / .env.example
├── requirements.txt
├── setup.sh
└── README.md
```

---

## 👥 Ideal For
- CISO demos
- Cybersecurity PoCs
- SOC modernization strategy