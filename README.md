# Performance Evaluation Analysis System

A comprehensive system for extracting, analyzing, and reporting on year-end performance evaluations.

## Overview

This system processes webarchive files containing employee performance evaluations and uses LLM analysis to generate comprehensive performance reviews, identify strengths and weaknesses, compare evaluator perspectives, and flag outliers.

## Components

1. **extract_evaluations.py** - Python script to extract structured data from webarchive files
2. **llm_prompt_template.md** - Comprehensive LLM prompt templates for analysis
3. **Evaluation_Structure_Analysis.md** - Documentation of the HTML structure

## Quick Start

### Prerequisites

```bash
# Install required Python packages
pip install beautifulsoup4
```

### Step 1: Extract Evaluation Data

Place all your `.webarchive` evaluation files in the current directory, then run:

```bash
# Process all webarchive files in current directory
python extract_evaluations.py . json_output/
```

This will:
- Find all `.webarchive` files in the current directory
- Extract evaluation data from each file
- Save JSON files to `json_output/` directory
- Print summary of each employee processed

**Single file example:**
```bash
python extract_evaluations.py "Alan Reskin.webarchive" "alan_data.json"
```

### Step 2: Analyze with LLM

#### Option A: Using Claude Code (Current Session)

1. Read the JSON file:
```
Read the file json_output/Alan_Reskin.json
```

2. Use the main analysis prompt from [llm_prompt_template.md](llm_prompt_template.md#main-analysis-prompt) with the JSON data

3. Ask follow-up questions as needed

#### Option B: Using Claude.ai Web Interface

1. Copy the JSON content from `json_output/Employee_Name.json`
2. Use the system prompt from [llm_prompt_template.md](llm_prompt_template.md#system-prompt-for-llm)
3. Paste the main analysis prompt with the JSON data
4. Ask follow-up questions in the same conversation

#### Option C: Using API

```python
import anthropic
import json

# Load evaluation data
with open('json_output/Alan_Reskin.json', 'r') as f:
    eval_data = json.load(f)

# Create client
client = anthropic.Anthropic(api_key="your-api-key")

# Read prompt template
with open('llm_prompt_template.md', 'r') as f:
    prompt_template = f.read()

# Format prompt with data
prompt = prompt_template.replace('{JSON_DATA}', json.dumps(eval_data, indent=2))

# Get analysis
message = client.messages.create(
    model="claude-sonnet-4",
    max_tokens=8000,
    messages=[{"role": "user", "content": prompt}]
)

print(message.content)
```

### Step 3: Committee Presentation

Generate outputs for committee review:

1. **Individual Analysis** - Full analysis for each employee
2. **Quick Briefings** - 200-word summaries using the quick insights prompt
3. **Comparative Analysis** - Compare multiple employees
4. **Development Plans** - Detailed development recommendations

## Workflow Examples

### Example 1: Analyze Single Employee

```bash
# Extract data
python extract_evaluations.py "Alan Reskin.webarchive" "alan_data.json"

# Review the JSON (optional)
cat alan_data.json | jq '.'

# Use LLM to analyze (copy-paste JSON into LLM with main analysis prompt)
```

### Example 2: Process Entire Team

```bash
# Place all webarchive files in 2025_evaluations/ directory
mkdir -p 2025_evaluations json_output analysis_output

# Copy webarchive files
cp *.webarchive 2025_evaluations/

# Extract all
python extract_evaluations.py 2025_evaluations/ json_output/

# Analyze each employee sequentially with LLM
# Save each analysis to analysis_output/
```

### Example 3: Identify Client vs Peer Discrepancies

1. Extract and analyze employee data
2. Use the "Client Feedback Analysis Prompt" from the template
3. Review CUSTOMER CHAMPION competency specifically
4. Flag employees with >0.5 point gaps

## Understanding the Output

### JSON Structure

```json
{
  "employee": {
    "name": "Employee Name",
    "role": "Job Title",
    "total_average": 3.2,
    "evaluations_received": 9,
    "evaluations_given": 5
  },
  "evaluations": [
    {
      "evaluator_name": "Evaluator Name",
      "evaluator_role": "Evaluator Role",
      "evaluator_type": "self|peer|client",
      "evaluation_average": 3.5,
      "competencies": {
        "TECH EXCELLENCE": [questions...],
        "TEAMWORK": [questions...],
        "CUSTOMER CHAMPION": [questions...],
        "GROWTH MINDSET": [questions...]
      },
      "strengths": ["strength1", "strength2"],
      "weaknesses": ["weakness1", "weakness2"],
      "additional_thoughts": "Free text..."
    }
  ]
}
```

### Rating Scale

- **4 stars**: Exceptional - Exceeds expectations significantly
- **3 stars**: Strong - Consistently meets and often exceeds expectations
- **2 stars**: Developing - Meets some expectations, needs improvement
- **1 star**: Below expectations - Significant development needed
- **0 stars**: Not demonstrated or not applicable

### Evaluator Types

The system automatically categorizes evaluators:
- **self**: Employee's self-evaluation
- **peer**: Colleague/team member evaluation
- **client**: Currently marked as "peer" (you may need to customize this)

To customize client identification, edit the `determine_evaluator_type()` method in `extract_evaluations.py`.

## Advanced Usage

### Customizing Client Detection

Edit `extract_evaluations.py` at line ~167:

```python
def determine_evaluator_type(self, evaluator_name: str, employee_name: str) -> str:
    """Determine if evaluator is self, peer, or client"""
    if evaluator_name.lower() == employee_name.lower():
        return "self"

    # Add your client detection logic here
    # Example: check if evaluator_name contains certain keywords
    client_keywords = ['client', 'customer', 'partner']
    if any(keyword in evaluator_name.lower() for keyword in client_keywords):
        return "client"

    # Or: maintain a list of known client names
    known_clients = ['Client Name 1', 'Client Name 2']
    if evaluator_name in known_clients:
        return "client"

    return "peer"
```

### Batch Processing Script

Create `process_all.sh`:

```bash
#!/bin/bash

# Extract all evaluations
python extract_evaluations.py . json_output/

# Create analysis directory
mkdir -p analysis_output

# List all JSON files
for json_file in json_output/*.json; do
    employee_name=$(basename "$json_file" .json)
    echo "Processing: $employee_name"

    # Here you would call your LLM API
    # For now, just list the files
    echo "  - JSON: $json_file"
    echo "  - Output: analysis_output/${employee_name}_analysis.md"
done

echo "Done! Review json_output/ for data and analysis_output/ for analyses"
```

### Filtering Evaluations

If you want to analyze only certain evaluations, you can filter the JSON:

```python
import json

# Load data
with open('json_output/Alan_Reskin.json', 'r') as f:
    data = json.load(f)

# Filter to only peer evaluations
peer_evals = [e for e in data['evaluations'] if e['evaluator_type'] == 'peer']
data['evaluations'] = peer_evals

# Save filtered data
with open('alan_peers_only.json', 'w') as f:
    json.dump(data, f, indent=2)
```

## LLM Prompt Templates

The [llm_prompt_template.md](llm_prompt_template.md) file contains multiple prompt templates:

1. **Main Analysis Prompt** - Comprehensive year-end review (use this first)
2. **Follow-up Question Prompt** - Ask specific questions about an employee
3. **Comparative Analysis Prompt** - Compare multiple employees
4. **Quick Insights Prompt** - Generate 200-word briefing summaries
5. **Outlier Investigation Prompt** - Deep dive into unusual ratings
6. **Client Feedback Analysis Prompt** - Focus on client perception
7. **Development Plan Prompt** - Create actionable development plans

### Using Prompts

1. Open [llm_prompt_template.md](llm_prompt_template.md)
2. Copy the relevant prompt template
3. Replace `{JSON_DATA}` with your employee's JSON data
4. Replace `{EMPLOYEE_NAME}` with the employee's name
5. Paste into LLM interface

## Troubleshooting

### Issue: "No module named 'bs4'"

**Solution:**
```bash
pip install beautifulsoup4
```

### Issue: "Error processing webarchive: not in gzip format"

**Cause:** File might be a binary plist that couldn't be read

**Solution:**
```bash
# Try converting with plutil first
plutil -convert xml1 "Problem File.webarchive"
```

### Issue: "Extracted 0 evaluations"

**Cause:** The HTML structure might be different or data wasn't loaded

**Solution:**
1. Open the webarchive in Safari
2. Make sure all evaluation panels are expanded (click to expand them)
3. Save as webarchive again
4. Try extracting again

### Issue: Wrong evaluator types (all showing as "peer")

**Solution:** Customize the `determine_evaluator_type()` method as shown in [Advanced Usage](#customizing-client-detection)

### Issue: Missing notes or incomplete data

**Cause:** Notes might be in a different HTML structure

**Solution:**
1. Check the HTML manually: `grep -A 5 "View note" extracted_content.html`
2. Adjust the `extract_note()` method in `extract_evaluations.py` if needed

## Best Practices

### For Data Extraction

1. **Verify webarchive completeness**: Open in Safari first to ensure all data loaded
2. **Expand all panels**: Make sure all evaluation sections are expanded before saving
3. **Check JSON output**: Review the JSON to ensure all evaluations were captured
4. **Backup originals**: Keep original webarchive files

### For LLM Analysis

1. **Start with main analysis**: Always run the comprehensive analysis first
2. **Save outputs**: Save each analysis as markdown for committee review
3. **Ask follow-ups in context**: Keep follow-up questions in the same conversation
4. **Compare after individual**: Analyze individuals before doing comparisons
5. **Review for accuracy**: Verify LLM conclusions match the data

### For Committee Preparation

1. **Quick briefs first**: Generate 200-word summaries for quick review
2. **Flag outliers early**: Use outlier investigation for concerning ratings
3. **Group by role**: Compare employees within similar roles/seniority
4. **Prepare FAQs**: Anticipate questions about specific employees
5. **Have data ready**: Keep JSON files handy for deep-dive questions

## Files in This System

```
.
├── README.md                          # This file
├── extract_evaluations.py             # Data extraction script
├── llm_prompt_template.md             # LLM analysis prompts
├── Evaluation_Structure_Analysis.md   # HTML structure documentation
│
├── *.webarchive                       # Input: Evaluation files
├── json_output/                       # Output: Extracted JSON data
│   ├── Employee1.json
│   ├── Employee2.json
│   └── ...
│
└── analysis_output/                   # Output: LLM analyses (you create these)
    ├── Employee1_analysis.md
    ├── Employee1_quick_brief.md
    ├── team_comparison.md
    └── ...
```

## Support and Customization

### Modifying the Extraction Script

The extraction script is modular. Key methods to customize:

- `extract_employee_info()` - Employee header data
- `extract_questions()` - Question/rating extraction
- `extract_note()` - Note extraction logic
- `determine_evaluator_type()` - Evaluator classification
- `extract_strengths_weaknesses()` - Strengths/weaknesses lists

### Adding New Analysis Types

To add new analysis prompts:

1. Edit [llm_prompt_template.md](llm_prompt_template.md)
2. Add a new section with your prompt template
3. Include clear instructions for the LLM
4. Document expected input format
5. Document expected output format

### Integration with Other Tools

The JSON output can be integrated with:

- **Excel/Google Sheets**: Import JSON for dashboards
- **Power BI**: Visualize evaluation trends
- **HRIS Systems**: Import back into HR platforms
- **Slack/Email**: Automated reporting
- **Custom Dashboards**: Build web interfaces

## Example Output

See [llm_prompt_template.md](llm_prompt_template.md) for detailed output format examples.

A typical main analysis output includes:

1. Executive Summary (3-4 sentences)
2. Quantitative Analysis (scores, ranges, distributions)
3. Qualitative Analysis (themes, patterns, examples)
4. Competency Deep Dive (all 4 competencies)
5. Evaluator Comparison (self vs peer vs client)
6. Pattern Analysis (frequency of themes)
7. Notable Observations (highlights and concerns)
8. Contextual Insights (role appropriateness, trajectory)
9. Summary for Committee (1-page brief)

## Tips for Effective Analysis

1. **Look for patterns**: Single low score might be outlier, consistent scores are patterns
2. **Read the notes**: Quantitative scores don't tell the whole story
3. **Compare evaluator types**: Gaps between self and others reveal self-awareness
4. **Consider role level**: A 3.0 might be great for junior, concerning for senior
5. **Watch for consensus**: When all evaluators agree, pay attention
6. **Flag contradictions**: When ratings and notes don't align, investigate
7. **Context matters**: Additional thoughts often provide critical context
8. **Don't over-interpret**: Sometimes a score is just a score

## Next Steps

1. **Extract your data**: Run the extraction script on your webarchive files
2. **Review JSON output**: Ensure data quality and completeness
3. **Run initial analysis**: Use the main analysis prompt for each employee
4. **Generate quick briefs**: Create committee-ready summaries
5. **Identify focus areas**: Use comparative analysis for team insights
6. **Prepare follow-ups**: Anticipate and prepare for committee questions
7. **Create action plans**: Use development plan prompt for those who need it

## Questions or Issues?

If you encounter issues or need customizations:

1. Check [Troubleshooting](#troubleshooting) section
2. Review [Evaluation_Structure_Analysis.md](Evaluation_Structure_Analysis.md) for HTML structure
3. Modify the extraction script as needed
4. Test with a single employee file first before batch processing

---

**Version**: 1.0
**Last Updated**: 2025-11-26
**Compatible with**: macOS webarchive format, Python 3.7+
