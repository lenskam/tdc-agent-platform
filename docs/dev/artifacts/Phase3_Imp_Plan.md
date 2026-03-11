# Phase 3: Data & M&E Department

## Goal Description

Build the "Data Analyst Agent" capable of connecting to DHIS2, cleaning datasets, and generating insights.
This agent acts as a force multiplier for the M&E team, automating routine data quality checks and basic descriptive statistics.

## User Review Required

> [!WARNING]
>
> - **DHIS2 Credentials**: Must be stored in [.env](file:///home/deployer/projects/tdc-agent-platform/.env) and NEVER logged.
> - **Data Privacy**: Patient-level data should NOT be passed to external LLMs. We will use local processing (Pandas) for analysis, LLM only for code generation/interpretation of aggregate stats.

## Proposed Changes

### Tools Layer

#### [NEW] [src/tools/dhis2_tools.py](file:///home/deployer/projects/tdc-agent-platform/src/tools/dhis2_tools.py)

- `fetch_analytics(indicators, period, org_unit)`: Calls DHIS2 API.
- `get_metadata(type)`: Fetches Data Elements/Org Units.

#### [NEW] [src/tools/data_processor.py](file:///home/deployer/projects/tdc-agent-platform/src/tools/data_processor.py)

- Uses `pandas`.
- `clean_dataset(csv_path)`: Removes duplicates, fills nulls (configurable).
- `detect_outliers(csv_path)`: Uses Z-score or IQR.

### Agents

#### [NEW] [src/agents/data_agent.py](file:///home/deployer/projects/tdc-agent-platform/src/agents/data_agent.py)

- Role: "Senior Data Analyst".
- Backstory: Expert in DHIS2 and Health Information Systems.
- Logic: It writes Python code (using `CodeInterpreter` style or rigid tools) to analyze data.

### Dashboard

#### [MODIFY] [dashboard/app/page.tsx](file:///home/deployer/projects/tdc-agent-platform/dashboard/app/page.tsx)

- Add "Data Analysis" tab.
- File upload zone for CSVs.

## Verification Plan

### Automated Tests

- **Unit**: `pytest tests/tools/test_data_processor.py` (verify pandas logic).
- **Integration**: Mock DHIS2 API -> Agent fetches data -> returns summary.

### Manual Verification

- Configure [.env](file:///home/deployer/projects/tdc-agent-platform/.env) with a Demo DHIS2 instance.
- Ask Agent: "Fetch ANC 4th Visit data for Sierra Leone 2023".
- Verify the JSON/CSV is saved to `outputs/`.
