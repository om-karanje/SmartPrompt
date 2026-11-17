# SmartPrompt

## Project Title
SmartPrompt: A Prompt Identification and Optimization System for Workplace Applications

## Problem Statement
Employees often write vague workplace prompts that leave out essential context, audience information, tone, output format, and constraints. This leads to weak, generic, or unprofessional AI responses. SmartPrompt helps users identify the prompt type, detect missing workplace-specific components, score the prompt, optimize it, and compare original and improved outputs.

## Motivation
Prompt engineering is a practical skill, especially in workplace contexts. The project demonstrates how structure, context, and explicit constraints can dramatically improve the usefulness of AI-generated work communication.

## Objectives
- Identify workplace prompt type automatically.
- Detect workplace domain and intent.
- Analyze missing prompt components using domain-aware gap analysis.
- Score prompts transparently from 0-100.
- Optimize prompts without inventing personal information.
- Compare original vs optimized outputs.
- Use IFEval-inspired constraint categories as a practical instruction-following layer.

## Key Features
- Prompt classification for email, leave request, project report, meeting summary, HR communication, and more.
- Domain-aware gap analysis with present, partial, and missing status.
- Transparent scoring by clarity, specificity, context, task definition, output format, constraints, and audience/tone.
- Constraint detection based on the IFEval taxonomy.
- Prompt optimization using placeholders for missing user-specific data.
- Original vs optimized response generation and evaluation.

## Unique Feature: Domain-Aware Gap Analysis
SmartPrompt does not only say that a prompt is poor. It explains which key parts are missing, such as role, task, context, objective, audience, tone, format, length, constraints, and required information. This makes the system explainable and suitable for a college prompt engineering project.

## System Architecture
- Frontend: React + Vite
- Backend: FastAPI + Python
- LLM integration: OpenRouter API
- Dataset: curated, system-ready workplace prompts in JSONL
- Storage: local session data only for demonstration purposes

## Workflow
1. User enters a workplace prompt.
2. The system checks all 11 prompt components, detects explicit constraints, and scores each component's contribution to a 100-point total.
3. The dataset retriever finds similar workplace examples and uses relevant structures as optional guidance while optimizing the prompt.
4. The original and optimized prompts are scored and displayed side by side.
5. On request, both prompts are sent to the configured LLM and their outputs are compared.

## Dataset Description
SmartPrompt uses backend/data/workplace_prompt_dataset.jsonl at runtime. It contains 500 records with stable IDs, labels, 15 workplace categories, structured constraints, and source metadata. The same records power sample prompts, dataset statistics, similar-example retrieval, and optional optimization guidance. The original IFEval source file remains in the repository as provenance; it is not loaded by the application.

## Why IFEval Is Used
IFEval-derived examples provide instruction-following patterns such as word counts, forbidden terms, required keywords, specific output formats, and casing requirements. Their expected constraints are normalized into a system-friendly schema. Newly authored workplace examples broaden the dataset beyond the original general-purpose prompts.

## Important Limitation
IFEval is not a workplace-specific dataset. It does not capture employee roles or enterprise workflows directly. SmartPrompt adapts the instruction taxonomy to workplace scenarios rather than claiming that the dataset itself is workplace-specific.

## Prompt Scoring Methodology
The project uses a transparent 0-100 scoring approach based on:
- Clarity (20)
- Specificity (20)
- Context (15)
- Task Definition (15)
- Output Format (10)
- Constraints (10)
- Audience & Tone (10)

Scores are calculated from real prompt analysis and missing components rather than hardcoded numbers.

## Gap Analysis Methodology
Each prompt is evaluated against key components:
- Role
- Task
- Context
- Objective
- Audience
- Tone
- Output Format
- Length
- Constraints
- Required Information
- Examples

Each component is labeled as present, partial, or missing.

## Constraint Detection
The detector extracts common count, required-term, forbidden-term, formatting, language, case, and structure constraints from the user's prompt. Dataset constraints support similar-example retrieval and supply optional structural guidance; constraints from a reference example are not presented as if the user requested them.

## Prompt Optimization Methodology
The optimizer preserves the original request verbatim, adds a structured workplace prompt template, and uses placeholders instead of inventing facts. When a sufficiently similar dataset example is found, its structure is offered as optional guidance.

## Scoring
The 0–100 score is the sum of contributions from Role, Task, Context, Objective, Audience, Tone, Output Format, Length, Constraints, Required Information, and Examples. Each contribution is weighted; present, partial, and missing components earn 100%, 50%, and 0% of their weight respectively.

## Original vs Optimized Comparison
The application compares the original prompt with the optimized prompt and then compares the generated outputs. This helps demonstrate whether prompt refinement leads to a better response.

## Output Evaluation
Generated original and optimized responses are evaluated using a lightweight automatic comparison that looks at relevance, completeness, structure, specificity, instruction adherence, and professional tone. The UI clearly labels this as automated LLM-based evaluation.

## Existing Manual Approach vs SmartPrompt
| Capability | Baseline / Manual Approach | SmartPrompt |
| --- | --- | --- |
| Prompt identification | Manual | Automated |
| Prompt scoring | Usually not structured | 0-100 scoring |
| Gap analysis | Manual | Domain-aware automated |
| Workplace context | User-dependent | Workplace-aware |
| Constraint detection | Manual | Automated |
| Prompt refinement | Manual | Automated |
| Before/after comparison | Manual | built-in |

## Gap Findings
The project addresses these practical gaps:
1. No systematic prompt identification.
2. Missing prompt components are not explicitly identified.
3. Lack of workplace-specific domain awareness.
4. Lack of transparent prompt scoring.
5. Lack of structured prompt refinement.
6. Lack of integrated before/after output evaluation.

## Folder Structure
```text
SmartPrompt/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── app/
│   ├── data/
│   ├── tests/
│   ├── .env
│   ├── .env.example
│   └── requirements.txt
├── .gitignore
├── README.md
└── .venv/
```

## Final Note
This project is designed as a practical, explainable mini-project suitable for a college prompt engineering course. It focuses on real-world workplace prompt quality improvement rather than on expensive ML model training.
