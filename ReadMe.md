# AI Regulatory Intelligence Platform  

## Carbon Border Adjustment Mechanism (CBAM) Assessment System

## Project Overview

The **AI-Native Regulatory Intelligence Platform** is a decision-support
system designed to automate regulatory assessments for the European
Union **Carbon Border Adjustment Mechanism (CBAM)**.

The platform combines deterministic regulatory logic with Large Language
Models (LLMs) to provide explainable, consultant-grade regulatory
assessments. Regulatory decisions are first established through a
Python-based rule engine using official CBAM Annex I product
classifications and EU destination rules. The current implementation
uses the **Groq API** with the **Llama-3.3-70B** model for high-speed
inference.

------------------------------------------------------------------------

# Objectives

-   Automate CBAM applicability assessments.
-   Reduce manual regulatory review time.
-   Generate consultant-quality explanations.
-   Produce structured JSON outputs.
-   Provide an intuitive HTML dashboard.
-   Build a modular architecture that can be extended to future
    regulations such as CSRD.

------------------------------------------------------------------------

# Technology Stack

  Component              Technology
  ---------------------- ---------------
  Programming Language   Python 3
  AI Provider            Groq API
  AI Model               Llama-3.3-70B
  Frontend               HTML
  Backend                Python
  Knowledge Base         Markdown
  Dataset                CSV + JSON
  Rule Engine            Custom Python
  Output Format          JSON

------------------------------------------------------------------------

# Project Structure

``` text
CBAM-CSRD-Assessment
│
├── agent/
│   ├── llm_client.py
│   ├── orchestrator.py
│   ├── output_parser.py
│   └── prompt_builder.py
│
├── engine/
│   ├── cbam_engine.py
│   ├── data_loader.py
│   └── models.py
│
├── data/
│   ├── cbam_annex1_cn_codes.csv
│   └── eu_countries.json
│
├── knowledge/
│   ├── cbam.md
│   └── csrd.md
│
├── templates/
│   └── index.html
│
├── app.py
└── requirements.txt
```

------------------------------------------------------------------------

# System Architecture

``` text
                    User
                      │
                      ▼
             HTML Dashboard
                      │
                      ▼
              Python Backend
                 (app.py)
                      │
                      ▼
             AI Orchestrator
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
CBAM Rule Engine             Prompt Builder
        │                           │
        ▼                           ▼
 Deterministic Context        Regulatory Prompt
        └─────────────┬─────────────┘
                      ▼
                Groq API : Llama-3/ Ollama : Qwen-3.5
          
                      │
                      ▼
              JSON Response
                      │
                      ▼
             Output Parser
                      │
                      ▼
          Dashboard Results
```

------------------------------------------------------------------------

# Processing Flow

1.  User enters company and product information through the dashboard.
2.  Python backend receives the request.
3.  CBAM Engine loads Annex I dataset and EU country list.
4.  Rule engine determines:
    -   CN Code Coverage
    -   EU Destination
    -   Final CBAM Applicability
5.  Prompt Builder combines company data, product data and deterministic
    context.
6.  Prompt is sent to **Groq (Llama-3.3-70B)**.
7.  LLM generates:
    -   Executive Summary
    -   Consultant Notes
    -   Recommendations
    -   Missing Information
    -   Risk Rating
8.  Output Parser validates the JSON response.
9.  Dashboard displays the assessment.

------------------------------------------------------------------------

# Component Flow

``` text
User
 │
 ▼
Dashboard (HTML)
 │
 ▼
app.py
 │
 ▼
AIOrchestrator
 │
 ├───────────────┐
 │               │
 ▼               ▼
CBAMEngine   PromptBuilder
 │               │
 ▼               │
Context──────────┘
 │
 ▼
LLM Client (Groq API)
 │
 ▼
Llama-3.3-70B
 │
 ▼
JSON
 │
 ▼
OutputParser
 │
 ▼
Dashboard
```

------------------------------------------------------------------------

# Current Status

## Completed

-   HTML Dashboard
-   Python Backend
-   CBAM Rule Engine
-   Groq LLM Integration
-   Prompt Builder
-   JSON Output Parser
-   Regulatory Knowledge Base
-   CN Code Dataset
-   EU Country Dataset
-   Consultant-style AI Reports

## Planned

-   CSRD Module
-   Multi-Regulation Dashboard
-   Real-world Dataset Validation
-   PDF Export
-   Authentication

------------------------------------------------------------------------

# Future Scope

The modular architecture supports future integration of:

-   CSRD
-   CSDDD
-   EUDR
-   EU Taxonomy
