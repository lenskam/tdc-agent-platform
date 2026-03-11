# Phase 5: Training & Research

## Goal Description

Create the "Training Agent" to democratize knowledge and support field staff.
This agent transforms technical documentation into user-friendly manuals, quizzes, and training slides. It also acts as a Level 1 Helpdesk for end-users.

## User Review Required

> [!NOTE]
>
> - **Input Format**: The agent needs access to specific technical specs (PDFs, Config JSONs) to generate accurate training materials.
> - **Output Format**: We will target Markdown and PDF outputs initially. Slide generation (PPTX) may require specialized libraries like `python-pptx`.

## Proposed Changes

### Tools Layer

#### [NEW] [src/tools/content_creator.py](file:///home/deployer/projects/tdc-agent-platform/src/tools/content_creator.py)

- `generate_quiz(topic, difficulty)`: Returns JSON with Questions/Answers.
- `create_user_manual_section(feature_name, technical_details)`: Rewrites tech-speak to plain English.

#### [NEW] [src/tools/knowledge_search.py](file:///home/deployer/projects/tdc-agent-platform/src/tools/knowledge_search.py)

- Simplified RAG for user manuals and SOPs.
- `search_help_docs(query)`

### Agents

#### [NEW] [src/agents/training_agent.py](file:///home/deployer/projects/tdc-agent-platform/src/agents/training_agent.py)

- Role: "Technical Trainer".
- Capabilities: Pedagogy, simplification, empathy.
- Logic: `assess_audience_level` -> `retrieve_content` -> `adapt_content`.

### Dashboard

#### [MODIFY] [dashboard/app/page.tsx](file:///home/deployer/projects/tdc-agent-platform/dashboard/app/page.tsx)

- Add "Training Center" tab.
- Content: "Generate Quiz", "Ask Helpdesk".

## Verification Plan

### Automated Tests

- **Unit**: `pytest tests/tools/test_content_creator.py` (Validate JSON schema of quizzes).
- **Integration**: Provide technical JSON of a form -> Agent generates a "How to fill this form" guide.

### Manual Verification

- Upload a JSON config of a DHIS2 Data Set.
- Ask Agent: "Create a 5-question quiz for data entry clerks about this dataset."
- Review the quiz for accuracy and clarity.
- Ask Agent: "How do I reset my password?" (Verify it finds the standard SOP).
