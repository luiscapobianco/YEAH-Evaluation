# Quick Start Guide - Performance Evaluation Analysis

## 5-Minute Setup

### Step 1: Place Your Files
Put all employee `.webarchive` files in this directory.

### Step 2: Set Up Environment (First Time Only)
```bash
# Navigate to this directory
cd "/Volumes/T7/Users/Shared/Mahisoft GD/Admin - Teams & Others/YEAH/2025"

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install requirements
pip install beautifulsoup4
```

### Step 3: Extract Data
```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Extract all webarchive files
python extract_evaluations.py . json_output/
```

This creates a `json_output/` directory with one JSON file per employee.

### Step 4: Analyze with LLM

#### In This Claude Code Session:

1. Read an employee's JSON file:
```
Read the file json_output/Alan_Reskin.json
```

2. Copy the main analysis prompt from [llm_prompt_template.md](llm_prompt_template.md), replace `{JSON_DATA}` with the JSON content, and paste it.

3. Ask follow-up questions about the employee.

4. Repeat for other employees.

---

## Example Workflow

### Scenario: Prepare for Committee Review of 5 Employees

```bash
# 1. Extract all data
source venv/bin/activate
python extract_evaluations.py . json_output/

# Output shows:
# ✓ Extracted data for: Alan Reskin
# ✓ Extracted data for: John Smith
# ✓ Extracted data for: Jane Doe
# ...
```

**Then in LLM:**

```
Please read these JSON files:
- json_output/Alan_Reskin.json
- json_output/John_Smith.json
- json_output/Jane_Doe.json

[After files are read, use the main analysis prompt for each employee]
```

---

## What You'll Get

### From the Extraction Script:
```json
{
  "employee": {
    "name": "Alan Reskin",
    "role": "QA Senior",
    "total_average": 3.3,
    "evaluations_received": 9
  },
  "evaluations": [
    {
      "evaluator_name": "Alberto Cols",
      "evaluator_type": "peer",
      "evaluation_average": 3.52,
      "competencies": {...},
      "strengths": [...],
      "weaknesses": [...]
    }
  ]
}
```

### From the LLM Analysis:
1. **Executive Summary** - 3-4 sentence overview
2. **Quantitative Analysis** - Scores by competency and evaluator type
3. **Qualitative Analysis** - Key strengths and development areas
4. **Competency Deep Dive** - Analysis of all 4 competencies
5. **Evaluator Comparison** - Self vs peer vs client perspectives
6. **Pattern Analysis** - Common themes across evaluators
7. **Notable Observations** - Highlights and concerns
8. **Committee Summary** - 1-page brief for decision-making

---

## Test Results: Alan Reskin

✅ **Successfully extracted 9 evaluations:**
- 1 Self-evaluation (Avg: 2.81)
- 5 Peer evaluations (Avg: 3.11)
- 3 Client evaluations (Avg: 3.83)

**Key Observation:** Client ratings (3.83) significantly higher than self-rating (2.81), suggesting strong external performance and possible under-self-assessment.

---

## Common Tasks

### Analyze Single Employee
```bash
source venv/bin/activate
python extract_evaluations.py "Employee Name.webarchive" "employee_data.json"
```

Then use the main analysis prompt in LLM.

### Compare Multiple Employees
After individual analysis, use the "Comparative Analysis Prompt" from [llm_prompt_template.md](llm_prompt_template.md).

### Quick Committee Brief
Use the "Quick Insights Prompt" to generate 200-word summaries for rapid review.

### Investigate Outliers
Use the "Outlier Investigation Prompt" when you notice unusual ratings.

### Focus on Client Feedback
Use the "Client Feedback Analysis Prompt" to deep-dive client perspectives.

---

## File Organization

```
2025/
├── QUICKSTART.md                  # This file
├── README.md                      # Full documentation
├── extract_evaluations.py         # Extraction script
├── llm_prompt_template.md         # LLM prompts
│
├── *.webarchive                   # Your input files
├── venv/                          # Python virtual environment
│
└── json_output/                   # Extracted data
    ├── Employee1.json
    ├── Employee2.json
    └── ...
```

---

## Tips

1. **Client Detection Works Automatically** - The script detects "(Client)" in evaluator roles
2. **Keep Originals** - Don't delete `.webarchive` files in case re-extraction is needed
3. **JSON is Portable** - You can copy JSON files to analyze on another machine
4. **Batch Processing** - Process all files at once: `python extract_evaluations.py . json_output/`
5. **Follow-up Questions** - Ask follow-up questions in the same LLM conversation for context

---

## Next Steps

1. ✅ Extraction script working
2. ✅ Tested with Alan Reskin (9 evaluations extracted successfully)
3. ⏭️ Extract your other employee evaluations
4. ⏭️ Analyze each employee with LLM
5. ⏭️ Generate committee summaries
6. ⏭️ Prepare for questions

---

## Need Help?

- **Full Documentation**: See [README.md](README.md)
- **HTML Structure**: See [Evaluation_Structure_Analysis.md](Evaluation_Structure_Analysis.md)
- **LLM Prompts**: See [llm_prompt_template.md](llm_prompt_template.md)
- **Troubleshooting**: See README.md [Troubleshooting Section](README.md#troubleshooting)

---

## Sample Commands Reference

```bash
# Setup (first time only)
python3 -m venv venv
source venv/bin/activate
pip install beautifulsoup4

# Extract single file
source venv/bin/activate
python extract_evaluations.py "Alan Reskin.webarchive" "alan_data.json"

# Extract all files in directory
source venv/bin/activate
python extract_evaluations.py . json_output/

# Verify extraction
python3 -c "
import json
with open('json_output/Alan_Reskin.json') as f:
    data = json.load(f)
    print(f\"Employee: {data['employee']['name']}\")
    print(f\"Evaluations: {len(data['evaluations'])}\")
"
```

---

**Ready to start?** Run the extraction command and you'll have structured data for LLM analysis in seconds!
