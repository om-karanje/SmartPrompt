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
- Dataset: JSONL IFEval-inspired instruction data
- Storage: local session data only for demonstration purposes

## Workflow
1. User enters a workplace prompt.
2. The system identifies the prompt type and workplace domain.
3. Required constraints and instruction patterns are detected.
4. A gap analysis shows missing components.
5. The prompt is scored.
6. The prompt is optimized.
7. The optimized prompt is scored again.
8. Original and improved prompts are sent to the LLM.
9. Outputs are compared and evaluated.

## Dataset Description
The project uses the dataset in backend/data/ifeval_input_data.jsonl. It is not a workplace-specific dataset; instead, it acts as an instruction-following and constraint taxonomy layer. SmartPrompt adds workplace logic on top of it.

## Why IFEval Is Used
IFEval provides realistic instruction-following patterns such as word counts, forbidden terms, required keywords, specific output formats, and casing requirements. These are useful for teaching prompt engineering and constraint detection.

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
The constraint detector uses patterns derived from the IFEval-style instruction taxonomy, including word count, sentence count, required keywords, forbidden words, formatting, capitalization, language, bullet lists, title requirements, and output structure.

## Prompt Optimization Methodology
The optimizer preserves the original intent while adding missing context, audience, tone, structure, and useful placeholders. It does not invent personal data and keeps explicit user requirements intact.

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

## Technology Stack
- Frontend: React, Vite, JavaScript, CSS
- Backend: Python, FastAPI, Uvicorn, Pydantic, python-dotenv, httpx
- Dataset: JSONL
- LLM: OpenRouter API

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

## Installation
1. Clone the project.
2. Create the Python venv and install dependencies.
3. Install frontend dependencies using npm.

## Environment Variables
Create backend/.env with:
```env
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=google/gemini-2.5-flash
```
The real key should never be committed to git or added to the frontend.

## OpenRouter Configuration
The project uses the OpenRouter model selected via the backend environment. All AI model calls are routed through the backend service layer.

## Running Backend
```bash
cd backend
../.venv/Scripts/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Running Frontend
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

## API Endpoints
- POST /api/analyze
- POST /api/generate
- POST /api/compare
- GET /api/examples
- GET /api/statistics

## Example Prompts
- Write an email to my manager.
- Write a leave request.
- Make a report about my project.
- Summarize this meeting.
- Write a message to HR.
- Create a presentation outline for my project.

## Testing
Run:
```bash
cd SmartPrompt/backend
../.venv/Scripts/python -m pytest tests -q
```

## Limitations
- The app does not train a custom model.
- The evaluation is lightweight and explainable rather than a formal benchmark.
- Prompt classification is rule-assisted and heuristic, not a trained ML classifier.
- OpenRouter availability depends on the configured API key and network access.

## Future Scope
- Education-specific prompts
- Healthcare-specific prompts
- Finance-specific prompts
- Customer support prompts
- Multilingual optimization
- Personalized prompt libraries
- Prompt history
- Browser extension
- Enterprise deployment
- Advanced human evaluation

## Final Note
This project is designed as a practical, explainable mini-project suitable for a college prompt engineering course. It focuses on real-world workplace prompt quality improvement rather than on expensive ML model training.
