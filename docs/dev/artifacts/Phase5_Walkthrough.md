# Phase 5 Implementation Walkthrough

## Overview
Phase 5 adds a Training Agent that transforms technical documentation into user-friendly training materials and provides Level 1 Helpdesk support.

## Components Implemented

### 1. Content Creator Tools (`src/tools/content_creator.py`)
- **`generate_quiz(topic, difficulty, num_questions)`**: Creates JSON quiz with multiple choice questions
- **`create_user_manual_section(feature_name, technical_details, audience)`**: Transforms tech docs to plain language
- **`generate_training_outline(topic, duration_minutes)`**: Creates training session outlines
- **`create_sop_from_process(process_name, steps)`**: Creates Standard Operating Procedures

### 2. Knowledge Search Tools (`src/tools/knowledge_search.py`)
- Uses ChromaDB for semantic search
- **`search_help_docs(query, n_results)`**: Searches SOPs and help documentation
- **`add_help_document(title, content, category)`**: Adds documents to knowledge base
- **`list_help_categories()`**: Lists available categories

### 3. Training Agent (`src/agents/training_agent.py`)
- Role: "Technical Trainer" with pedagogy and simplification expertise
- Methods:
  - `generate_quiz()` - Quiz generation task
  - `create_user_manual()` - Manual creation task
  - `create_training_outline()` - Training outline task
  - `helpdesk_query()` - Helpdesk Q&A task
  - `full_training_session()` - Complete training package

### 4. Dashboard Integration
- Added "Training Center" tab in dashboard
- Features:
  - Generate Quiz (with difficulty selection)
  - User Manual (placeholder for future)
  - Helpdesk Q&A

### 5. API Routes (`src/api/routes/training_routes.py`)
- `POST /api/v1/agents/training/quiz` - Generate quiz
- `POST /api/v1/agents/training/helpdesk` - Helpdesk query
- `POST /api/v1/agents/training/manual` - Create manual
- `POST /api/v1/agents/training/outline` - Create training outline

## Usage

### Generate a Quiz
```bash
curl -X POST http://localhost:8000/api/v1/agents/training/quiz \
  -H "Content-Type: application/json" \
  -d '{"topic": "DHIS2 data entry", "difficulty": "medium", "num_questions": 5}'
```

### Ask Helpdesk
```bash
curl -X POST http://localhost:8000/api/v1/agents/training/helpdesk \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I reset my password?"}'
```

## Testing
Run: `docker-compose up --build`
Access dashboard at: http://localhost:3000
Navigate to "Training Center" tab
