# 📊 LLM-Assisted PRA COREP Reporting Assistant (Prototype)

## 🚀 Overview

This project is a prototype **LLM-assisted regulatory reporting assistant** designed to support UK banks preparing **PRA COREP regulatory returns**.

The assistant demonstrates end-to-end automation of regulatory reporting workflows by combining:

- Retrieval Augmented Generation (RAG)
- Structured LLM extraction
- Compliance validation
- Explainability & audit logging
- COREP-style reporting template generation

---

## 🎯 Problem Statement

COREP regulatory reporting requires analysts to interpret complex PRA/EBA regulatory instructions and map them to reporting templates. This process is:

- Labour intensive  
- Error prone  
- Difficult to audit  

This prototype demonstrates how LLMs can assist analysts by automatically retrieving rules, extracting structured regulatory data, validating compliance, and generating reporting extracts.

---

## 🧠 Key Features

### ✅ Natural Language Reporting Scenario Input
Users can provide reporting scenarios in plain English.

---

### ✅ Regulatory Text Retrieval (RAG)
- Retrieves relevant COREP/PRA instruction documents
- Provides traceable evidence snippets
- Includes page references and confidence scoring

---

### ✅ Structured LLM Output
Outputs COREP metrics aligned to predefined schema:

- CET1 Capital
- AT1 Capital
- Tier 2 Capital
- Risk Weighted Assets
- Capital Ratios

---

### ✅ Compliance & Risk Validation
- Validates ratios against CRR rules
- Flags missing or low-confidence data
- Routes outputs for manual review when required

---

### ✅ Explainability Engine
Shows:

- Calculation formulas
- Values used
- Regulatory references

---

### ✅ Audit Logging
Every run generates audit metadata including:

- Model version
- Prompt version
- Evidence sources
- Compliance results
- Risk flags

---

### ✅ COREP-Style Reporting Extract
Maps structured output into a human-readable COREP reporting template.

---

### ✅ Streamlit UI
Interactive user interface to:

- Submit reporting scenarios
- View compliance results
- View audit evidence
- View COREP reporting output

---

## 🏗 Architecture

```
User Query
   ↓
Retriever (RAG)
   ↓
LLM Structured Extraction
   ↓
Compliance Validator
   ↓
Risk Flagging
   ↓
Audit Log Generator
   ↓
COREP Template Mapper
   ↓
Streamlit UI
```

---

## 📂 Project Structure

```
corep_assistant/
│
├── rag/                    # Retrieval logic
├── llm/                    # LLM generation + schema
├── audit/                  # Audit logging + compliance validation
├── template/               # COREP template mapping
├── pipeline/               # End-to-end orchestration
├── streamlit_app.py        # Streamlit UI
├── main.py                 # CLI execution
├── data/                   # COREP regulatory documents
└── audit_logs/             # Generated audit logs
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Bhavani-sakhamuri/corep-assistant.git
cd corep-assistant
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows:
```bash
.venv\Scripts\activate
```

Mac/Linux:
```bash
source .venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add Environment Variables

Create `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Running the Application

### Run Streamlit UI

```bash
streamlit run streamlit_app.py
```

---

### Run CLI Pipeline

```bash
python main.py
```

---

## 📑 Example Input

```
Bank reports:
CET1 = 120 million
AT1 = 20 million
Tier2 = 10 million
RWA = 900 million
```

---

## 📊 Example Output

- COREP capital metrics
- Compliance validation results
- Risk flags
- Evidence trace
- Audit log JSON
- COREP reporting extract

---

## 🔍 Compliance Logic

Based on CRR Articles:

- Article 92(1)(a) – CET1 Ratio
- Article 92(1)(c) – Total Capital Ratio
- Article 72 – Own Funds Calculation

---

## 🛠 Technologies Used

- Python
- LangChain / RAG
- Groq LLM (Llama-3.3-70B)
- Pydantic
- Streamlit
- Vector Database
- Regulatory Document Parsing

---

## 📌 Future Enhancements

- Multi-template COREP support
- XBRL taxonomy mapping
- Editable reporting UI
- Real-time regulatory updates

---

