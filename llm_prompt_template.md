# LLM Prompt Template for Performance Review Analysis

## System Prompt for LLM

You are an expert HR analyst specializing in year-end performance reviews. You have been provided with structured evaluation data extracted from a company's performance review system. Your role is to analyze this data and provide comprehensive, objective insights for management committee presentations.

The evaluation system uses a 4-point scale (0-4 stars) across 4 key competency areas:
1. TECH EXCELLENCE
2. TEAMWORK
3. CUSTOMER CHAMPION
4. GROWTH MINDSET

Each evaluation includes:
- Ratings for multiple questions within each competency
- Optional notes providing context
- Identified strengths and weaknesses
- Additional thoughts from evaluators

Your analysis should be:
- **Objective and data-driven**: Base conclusions on patterns in the data
- **Balanced**: Highlight both strengths and development areas
- **Specific**: Reference actual scores, quotes, and examples
- **Actionable**: Identify clear themes and patterns
- **Comparative**: Note differences between self, peer, and client evaluations
- **Outlier-aware**: Flag any significant discrepancies or unusual ratings

---

## Main Analysis Prompt

```
Please analyze the following year-end performance evaluation data and provide a comprehensive performance review.

EMPLOYEE DATA:
{JSON_DATA}

Please provide the following analysis:

## 1. EXECUTIVE SUMMARY
Provide a 3-4 sentence overview of the employee's overall performance, key strengths, and primary development areas.

## 2. QUANTITATIVE ANALYSIS

### Overall Metrics
- Total Average Score: [X.XX / 4.0]
- Number of Evaluations: [X self, Y peer, Z client]
- Score Range: [min - max]
- Standard Deviation: [if significant variance exists]

### Competency Breakdown
For each of the 4 competencies, provide:
- Average score
- Score range across evaluators
- Comparison to overall average
- Brief interpretation (strength/development area)

### Score Distribution by Evaluator Type
Compare averages across:
- Self-evaluation
- Peer evaluations
- Client evaluations (if applicable)

Identify any significant gaps (>0.5 points) between evaluator types.

## 3. QUALITATIVE ANALYSIS

### Key Strengths (Top 3-5)
For each strength:
- Theme/pattern identified
- Supporting evidence from evaluations (quotes, ratings, frequency mentioned)
- Which evaluator types emphasized this
- Specific examples from notes

### Development Areas (Top 3-5)
For each area:
- Theme/pattern identified
- Supporting evidence
- Which evaluator types emphasized this
- Specific examples from notes
- Severity assessment (critical/moderate/minor)

### Competency Deep Dive

#### TECH EXCELLENCE
- Overall assessment
- Specific strengths within this competency
- Specific development areas
- Notable quotes from evaluators
- Comparison: self vs others

#### TEAMWORK
- Overall assessment
- Specific strengths within this competency
- Specific development areas
- Notable quotes from evaluators
- Comparison: self vs others

#### CUSTOMER CHAMPION
- Overall assessment
- Specific strengths within this competency
- Specific development areas
- Notable quotes from evaluators
- Comparison: self vs others

#### GROWTH MINDSET
- Overall assessment
- Specific strengths within this competency
- Specific development areas
- Notable quotes from evaluators
- Comparison: self vs others

## 4. EVALUATOR COMPARISON ANALYSIS

### Self vs Peer Assessment
- Overall score difference: [X.XX]
- Areas where self-rating is higher than peers (if any)
- Areas where self-rating is lower than peers (if any)
- Self-awareness assessment

### Peer vs Client Assessment (if applicable)
- Overall score difference
- Notable differences in perception
- Implications for customer relationships

### Consensus vs Outliers
- Areas of strong consensus (all evaluators agree)
- Outlier ratings (significant deviations from average)
- Possible explanations for outliers

## 5. PATTERN ANALYSIS

### Strengths Mentioned Most Frequently
List strengths mentioned by multiple evaluators with frequency count.

### Weaknesses Mentioned Most Frequently
List weaknesses mentioned by multiple evaluators with frequency count.

### Emergent Themes
Identify 2-3 overarching themes from the evaluation data that weren't explicitly asked about.

## 6. NOTABLE OBSERVATIONS

### Positive Highlights
- Exceptional ratings (4/4 stars consistently)
- Particularly insightful positive feedback
- Evidence of growth or improvement

### Areas of Concern
- Consistently low ratings (≤2/4 stars)
- Red flags in evaluator comments
- Skill gaps for role level

### Contradictions or Inconsistencies
- Areas where evaluators strongly disagree
- Misalignments between ratings and written feedback
- Gaps between different competency areas

## 7. CONTEXTUAL INSIGHTS

### Role Appropriateness
- Are ratings appropriate for the employee's role level?
- Does performance align with seniority expectations?

### Development Trajectory
- Signs of growth mindset and improvement potential
- Areas where employee seems stuck or plateaued

## 8. SUMMARY FOR COMMITTEE

Provide a concise 1-page summary suitable for management committee review, including:
- Overall performance rating (Exceeds/Meets/Below Expectations)
- Top 3 strengths
- Top 3 development areas
- Key recommendation (promote/maintain/develop/concern)
- Suggested focus areas for next review cycle

---

## IMPORTANT GUIDELINES

1. **Be specific**: Always reference actual scores and quote evaluators when making points
2. **Show your work**: Explain how you arrived at conclusions
3. **Stay objective**: Avoid assumptions not supported by the data
4. **Respect confidentiality**: Treat all information professionally
5. **Flag data quality issues**: Note if evaluations seem incomplete or inconsistent
6. **Use appropriate tone**: Professional, constructive, and balanced
7. **Provide context**: Explain what ratings mean in practical terms
```

---

## Follow-up Question Prompt Template

```
I have a follow-up question about {EMPLOYEE_NAME}'s evaluation:

{USER_QUESTION}

Please reference specific data from the evaluation in your response, including:
- Relevant scores and ratings
- Direct quotes from evaluators when applicable
- Comparisons across evaluator types if relevant
- Specific competency areas affected

Keep your response focused and data-driven.
```

---

## Comparative Analysis Prompt (for multiple employees)

```
Please compare the performance evaluations of the following employees:

{LIST_OF_EMPLOYEE_NAMES}

Provide a comparative analysis including:

## 1. OVERALL RANKING
Rank employees by total average score with context.

## 2. COMPETENCY COMPARISON
For each of the 4 competencies, show how each employee compares.

## 3. STRENGTHS COMPARISON
- Who are the strongest performers in each competency area?
- Are there common strengths across high performers?
- Unique strengths of individual contributors

## 4. DEVELOPMENT AREAS COMPARISON
- Common development areas across the group
- Individual-specific challenges
- Critical gaps vs minor development areas

## 5. EVALUATION QUALITY
- Who has the most comprehensive feedback?
- Any concerns about evaluation completeness or quality?

## 6. ROLE-BASED OBSERVATIONS
Group employees by role/seniority and compare within role groups.

## 7. RECOMMENDATIONS
- Who is ready for promotion?
- Who needs performance improvement plan?
- Who is performing at expected level?

Keep this analysis objective and reference specific data points.
```

---

## Quick Insights Prompt (for rapid committee prep)

```
Provide a quick 5-minute briefing summary for {EMPLOYEE_NAME}:

1. One-sentence performance summary
2. Overall score and percentile (if multiple employees)
3. Top 2 strengths
4. Top 2 development areas
5. Self-awareness check (self vs peer scores)
6. One key recommendation
7. Any red flags or concerns

Keep this to 200 words or less.
```

---

## Outlier Investigation Prompt

```
I noticed {SPECIFIC_OBSERVATION} in {EMPLOYEE_NAME}'s evaluation.

Please investigate this outlier:

1. What is the specific data point?
2. How does it compare to:
   - The employee's other ratings
   - Ratings from other evaluators
   - Expected performance for their role
3. Are there notes or comments that explain this?
4. Are there related patterns in the data?
5. What are possible explanations?
6. Does this require attention or is it explainable?

Provide a focused analysis with supporting evidence.
```

---

## Client Feedback Analysis Prompt (when applicable)

```
Please analyze the client feedback specifically for {EMPLOYEE_NAME}:

1. How do client ratings differ from internal (self + peer) ratings?
2. What competencies do clients rate higher/lower?
3. What themes emerge from client-specific comments?
4. Are there any concerns in client-facing competencies?
5. What does this tell us about client relationship effectiveness?
6. Recommendations for improving client satisfaction

Focus on CUSTOMER CHAMPION and TEAMWORK competencies particularly.
```

---

## Development Plan Prompt

```
Based on {EMPLOYEE_NAME}'s evaluation, create a development plan:

1. **Priority Development Areas** (top 3)
   - Specific skill/competency
   - Current level (from evaluation data)
   - Target level
   - Evidence from evaluation

2. **Recommended Actions** for each area:
   - Training or learning resources
   - On-the-job development opportunities
   - Mentoring or coaching suggestions
   - Specific behavioral changes

3. **Leveraging Strengths**
   - How to use their strengths to address weaknesses
   - Opportunities to showcase strengths more

4. **Timeline and Milestones**
   - 90-day goals
   - 6-month checkpoints
   - Year-end objectives

5. **Success Metrics**
   - How to measure improvement
   - What should change in next evaluation cycle

Base all recommendations on specific evaluation data.
```

---

## Notes for LLM Usage

### Input Format
The LLM expects JSON data in this structure:
```json
{
  "employee": {
    "name": "John Doe",
    "role": "Senior Developer",
    "total_average": 3.2,
    "evaluations_received": 9,
    "evaluations_given": 5
  },
  "evaluations": [
    {
      "evaluator_name": "John Doe",
      "evaluator_role": "Senior Developer",
      "evaluator_type": "self",
      "evaluation_average": 3.5,
      "competencies": {
        "TECH EXCELLENCE": [
          {
            "question": "...",
            "stars": 3,
            "level_description": "...",
            "note": "..."
          }
        ],
        "TEAMWORK": [...],
        "CUSTOMER CHAMPION": [...],
        "GROWTH MINDSET": [...]
      },
      "strengths": ["...", "..."],
      "weaknesses": ["...", "..."],
      "additional_thoughts": "..."
    }
  ]
}
```

### Token Considerations
- Full analysis for a single employee with 9 evaluations: ~3,000-5,000 tokens output
- Multiple employee comparison: ~1,000-2,000 tokens per employee
- Follow-up questions: ~500-1,500 tokens
- Use Claude Sonnet or Opus for best analysis quality
- Can use Haiku for quick insights

### Best Practices
1. **Load all employee JSON files first** before starting analysis
2. **Process employees sequentially** for committee presentation
3. **Ask follow-up questions** in the same conversation to maintain context
4. **Save analysis outputs** as markdown files for committee review
5. **Compare employees** only after individual analysis is complete

### Example Workflow
1. Extract data: `python extract_evaluations.py . json_output/`
2. Load JSON data into LLM conversation
3. Request main analysis for each employee
4. Ask follow-up questions as needed
5. Request comparative analysis for team/role groups
6. Generate quick briefing summaries for committee
