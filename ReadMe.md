# AI-Native Regulatory Intelligence Platform

## Overview

The AI-Native Regulatory Intelligence Platform is designed to automate regulatory assessments for sustainability regulations using a combination of deterministic rule engines and Large Language Models (LLMs).

The project currently supports:

- Carbon Border Adjustment Mechanism (CBAM)
- Corporate Sustainability Reporting Directive (CSRD) *(under development)*

The platform combines deterministic regulatory logic with AI-generated consultant-style explanations.

---

## Architecture

```
                +---------------------+
                |   Company Data      |
                |   Product Data      |
                +----------+----------+
                           |
                           v
                 +--------------------+
                 |  Deterministic     |
                 |   Rule Engine      |
                 +--------------------+
                           |
             Product Context / Rules
                           |
                           v
                 +--------------------+
                 | Prompt Builder     |
                 +--------------------+
                           |
                           v
                 +--------------------+
                 | Ollama (Qwen3:4B)  |
                 +--------------------+
                           |
                           v
                 +--------------------+
                 | JSON Output        |
                 +--------------------+
                           |
                           v
                 +--------------------+
                 | Output Parser      |
                 +--------------------+
                           |
                           v
                 Assessment Output
```

---

# Project Structure

```
project/
│
├── agent/
│   ├── ollama_client.py
│   ├── orchestrator.py
│   ├── output_parser.py
│   └── prompt_builder.py
│
├── engine/
│   ├── cbam_engine.py
│   ├── data_loader.py
│   └── models.py
│
├── knowledge/
│   ├── cbam/
│   └── csrd/
│
├── data/
│   ├── cbam_rules.csv
│   └── eu_countries.csv
│
├── app.py
└── README.md
```

---

# Current Features

## CBAM

Implemented:

- Deterministic CN Code lookup
- EU Member State lookup
- Product coverage determination
- Legal reference lookup
- Sector identification
- AI-generated consultant explanation
- JSON structured output
- Output parser
- Local LLM inference using Ollama
- Deterministic applicability logic

---

## CSRD

Current Status

- Project structure created
- Knowledge base preparation

Pending:

- Rule engine
- Prompt builder
- Assessment logic
- Testing

---

# Technologies Used

- Python 3.11+
- Ollama
- Qwen3:4B
- Dataclasses
- JSON
- CSV

---

# Installation

Clone the repository

```bash
git clone <repository-url>
cd project
```

Install dependencies

```bash
pip install ollama
```

Install the LLM

```bash
ollama pull qwen3:4b
```

Start Ollama

```bash
ollama serve
```

Run the application

```bash
python app.py
```

---

# Workflow

```
Company Data
      │
      ▼
Product Data
      │
      ▼
CBAM Rule Engine
      │
      ▼
Prompt Builder
      │
      ▼
Qwen3 (Ollama)
      │
      ▼
JSON Response
      │
      ▼
Output Parser
      │
      ▼
Assessment Output
```

---

# Output

The application returns a structured assessment including:

- Executive Summary
- CBAM Assessment
- Confidence Score
- Reasoning
- Regulatory References
- Recommendations
- Missing Information
- Consultant Notes
- Risk Rating

---

# Future Enhancements

- CSRD assessment engine
- Excel integration
- Dashboard
- Multi-regulation support
- Real-world dataset validation
- Audit logging

---

# Current Limitations

- Excel integration pending
- Validation on real client datasets pending
- CSRD module under development

---

# License

For educational and research purposes.

---

# Author

Yash Khanna

AI-Native Regulatory Intelligence Platform