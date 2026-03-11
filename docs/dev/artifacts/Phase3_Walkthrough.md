# Phase 3 Implementation Walkthrough

## Overview

This document provides a comprehensive walkthrough of the Phase 3 implementation for the TDC Agent Platform - Data & M&E Department.

**Implemented:** 2026-03-11

---

## Architecture

### Components Created

```
src/
├── tools/
│   ├── dhis2_tools.py         # DHIS2 API connector
│   └── data_processor.py       # Pandas data processing
├── agents/
│   └── data_agent.py          # Data Analyst Agent
```

---

## DHIS2 Tools (`src/tools/dhis2_tools.py`)

### Purpose
Connect to DHIS2 API for health data analytics and metadata retrieval.

### Environment Variables Required
```bash
DHIS2_BASE_URL=https://your-dhis2-instance.org
DHIS2_USERNAME=your_username
DHIS2_PASSWORD=your_password
```

### Tools Available

| Tool | Description |
|------|-------------|
| `fetch_dhis2_analytics` | Fetch analytics data from DHIS2 |
| `get_dhis2_metadata` | Fetch metadata (indicators, org units, etc.) |
| `list_dhis2_indicators` | List available indicators |

### Usage Example

```python
from src.tools.dhis2_tools import dhis2_tools

# Fetch ANC 4th Visit data for Sierra Leone 2023
result = await fetch_dhis2_analytics(
    indicators="ANC4Coverage",
    period="2023",
    org_unit="ImspTQPwCqd"
)

# Get list of indicators
indicators = await list_dhis2_indicators(category="ANC")
```

---

## Data Processor (`src/tools/data_processor.py`)

### Purpose
Local data processing using Pandas - ensures data privacy by processing locally.

### Tools Available

| Tool | Description |
|------|-------------|
| `clean_dataset` | Remove duplicates, fill nulls, drop columns |
| `detect_outliers` | Detect outliers using IQR or Z-score |
| `generate_statistics` | Generate descriptive statistics |

### Usage Example

```python
from src.tools.data_processor import data_processor_tools

# Clean dataset
result = await clean_dataset(
    file_path="/data/patient_data.csv",
    remove_duplicates=True,
    fill_nulls_method="mean",
    drop_columns="unused_col1,unused_col2"
)

# Detect outliers
outliers = await detect_outliers(
    file_path="/data/patient_data.csv",
    columns="age,height,weight",
    method="iqr",
    threshold=1.5
)

# Generate statistics
stats = await generate_statistics(file_path="/data/patient_data.csv")
```

### Output
Cleaned files are saved to `outputs/` directory.

---

## Data Analyst Agent (`src/agents/data_agent.py`)

### Role
**Senior Data Analyst** - Expert in DHIS2 and Health Information Systems.

### Agent Tasks

| Task | Description |
|------|-------------|
| `fetch_health_data` | Fetch data from DHIS2 |
| `analyze_dataset` | Full analysis with stats and outliers |
| `clean_data` | Clean CSV dataset |
| `check_data_quality` | Data quality assessment |
| `full_analysis` | Complete workflow |

### Integration

```python
from src.agents.data_agent import DataAnalystAgent
from crewai import Crew

agent = DataAnalystAgent()
task = agent.full_analysis(
    file_path="/data/health_data.csv",
    dhis2_indicators="ANC4Coverage,DeliveryBySkilled"
)

crew = Crew(
    agents=[agent.get_agent()],
    tasks=[task]
)

result = crew.kickoff()
```

---

## Dashboard Integration

### New Tab: Data Analysis

Located at: `dashboard/components/DataAnalysis.tsx`

**Features:**
- CSV file upload
- Three analysis tabs:
  - **Statistics** - Descriptive statistics
  - **Outliers** - Outlier detection
  - **Clean Data** - Data cleaning
- Results display with preview

### API Endpoint (Future)

```python
# POST /api/v1/data/analyze
# Form data:
# - file: CSV file
# - action: stats|outliers|clean
```

---

## Dependencies Added

```txt
pandas>=2.0.0
numpy>=1.24.0
```

---

## Privacy Considerations

- **Local Processing**: All CSV analysis uses Pandas locally
- **No Patient Data to LLM**: Only aggregate statistics go to LLM
- **DHIS2 Credentials**: Stored in environment variables, never logged

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `DHIS2 credentials not configured` | Missing env vars | Set DHIS2_BASE_URL, DHIS2_USERNAME, DHIS2_PASSWORD |
| `pandas not installed` | Missing dependency | pip install pandas |
| `File not found` | Invalid path | Check file path |
| `No numeric columns` | Wrong file type | Use CSV with numeric data |

---

## Testing

### Manual Test

1. Create a test CSV:
```csv
name,age,height,weight
John,25,175,70
Jane,30,165,60
...
```

2. Upload via Dashboard or API:
```bash
curl -X POST http://localhost:8000/api/v1/data/analyze \
  -F "file=@test.csv" \
  -F "action=stats"
```

3. Check output in `outputs/` directory.

### DHIS2 Test (requires credentials)

```bash
curl -X POST http://localhost:8000/api/v1/data/dhis2 \
  -H "Content-Type: application/json" \
  -d '{
    "indicators": "ANC4Coverage",
    "period": "2023",
    "org_unit": "ImspTQPwCqd"
  }'
```

---

## File Structure

```
src/
├── tools/
│   ├── dhis2_tools.py          # DHIS2 API connector
│   │   ├── fetch_dhis2_analytics()
│   │   ├── get_dhis2_metadata()
│   │   └── list_dhis2_indicators()
│   │
│   └── data_processor.py        # Pandas wrapper
│       ├── clean_dataset()
│       ├── detect_outliers()
│       └── generate_statistics()
│
└── agents/
    └── data_agent.py           # Data Analyst Agent
        ├── fetch_health_data()
        ├── analyze_dataset()
        ├── clean_data()
        ├── check_data_quality()
        └── full_analysis()

dashboard/
└── components/
    └── DataAnalysis.tsx        # Data Analysis UI
```
