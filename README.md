# Prompt Testing System for Multi-Agent Research Assistant

A comprehensive A/B testing framework for evaluating and optimizing prompt variants in your multi-agent marketing analysis system.

## Overview

This system allows you to:
- Test multiple prompt variants for each agent
- Measure performance across key metrics (consistency, specificity, actionability)
- Compare variants statistically
- Automatically determine the best-performing configuration
- Run interactive analysis sessions

## Project Structure

```
Research Assistant/
├── config/
│   └── prompt_variants.json      # Prompt variant configurations
├── orchestrator/
│   ├── __init__.py
│   ├── prompt_tester.py          # A/B testing framework
│   └── workflow_engine.py        # Main workflow orchestrator (existing)
├── agents/                        # Your existing agent implementations
│   ├── strategic_analyst.py
│   └── audience_evaluator.py
├── outputs/
│   └── tests/                    # A/B test results stored here
├── test_prompts.py               # Batch testing script
├── interactive.py                # Interactive console
└── README.md
```

## Setup Instructions

### 1. Prerequisites

Make sure you have Python 3.8+ installed and your environment is set up with:

```bash
pip install anthropic python-dotenv
```

### 2. Environment Configuration

Create a `.env` file in the project root with your Anthropic API key:

```
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Verify File Structure

Ensure all files are in place:
- [config/prompt_variants.json](config/prompt_variants.json)
- [orchestrator/prompt_tester.py](orchestrator/prompt_tester.py)
- [test_prompts.py](test_prompts.py)
- [interactive.py](interactive.py)

## Usage

### Batch A/B Testing

Run automated tests on all prompt variants:

```bash
python test_prompts.py
```

This will:
1. Test all variants for the strategic_analyst agent
2. Run 3 iterations per variant
3. Calculate performance metrics
4. Generate detailed reports
5. Identify the best-performing variant

**Output:** Results saved to `outputs/tests/`

### Interactive Mode

Start an interactive session for real-time testing:

```bash
python interactive.py
```

**Available Commands:**
```
>>> help           # Show all commands
>>> input          # Enter document interactively
>>> load file.txt  # Load from file
>>> analyze        # Run full analysis
>>> test           # A/B test prompt variants
>>> config         # Show current configuration
>>> history        # View past analyses
>>> quit           # Exit
```

## Prompt Variants

The system tests different prompt engineering approaches:

### Strategic Analyst Variants
1. **Expert Marketing Consultant** - Professional framing for technical accuracy
2. **Consumer Viewpoint** - Consumer perspective for authentic response prediction
3. **Competitive Intelligence Specialist** - Competitive framing to surface strategic gaps
4. **Direct Strategic Assessment** - Direct questioning for precision

### Audience Evaluator Variants
1. **Consumer Insights Specialist** - Professional behavioral analysis
2. **Target Audience Member** - First-person authentic response
3. **Skeptical Evaluator** - Critical analysis to surface objections

## Performance Metrics

Each variant is evaluated on:
- **Consistency** - Reproducibility across iterations (0-1)
- **Specificity Score** - Avoidance of generic language (0-1)
- **Actionability Score** - Concrete, implementable recommendations (0-1)
- **Technical Density** - Use of domain-specific terminology
- **Execution Time** - Processing speed (seconds)
- **Success Rate** - Percentage of successful executions

## Customizing Variants

Edit [config/prompt_variants.json](config/prompt_variants.json) to:
- Add new prompt variants
- Modify system prompts
- Adjust temperature settings
- Change hypothesis descriptions

Example:
```json
{
  "strategic_analyst": {
    "variants": {
      "v5_your_variant": {
        "name": "Your Custom Variant",
        "temperature": 0.3,
        "system_prompt": "Your custom prompt here...",
        "hypothesis": "Your hypothesis about performance",
        "expected_performance": "What you expect to see"
      }
    }
  }
}
```

## Reading Test Results

### JSON Output
Full results with raw data: `outputs/tests/ab_test_[agent]_[timestamp].json`

### Text Report
Human-readable summary: `outputs/tests/ab_test_[agent]_[timestamp]_report.txt`

The report includes:
- Winner announcement with composite score
- Per-variant performance breakdown
- Comparative rankings across all metrics
- Deployment recommendation

## Example Test Results

```
======================================================================
A/B TEST REPORT: strategic_analyst
======================================================================

Test Date: 2024-01-15T14:30:00

WINNER: Expert Marketing Consultant
Composite Score: 0.847

======================================================================
VARIANT PERFORMANCE COMPARISON
======================================================================

v1_expert_framed: Expert Marketing Consultant
----------------------------------------------------------------------
Hypothesis: Expert framing activates professional knowledge
Temperature: 0.3

Performance Metrics:
  - Consistency:        0.892
  - Specificity:        0.945
  - Actionability:      0.867
  - Technical Density:  0.723
  - Avg Execution Time: 2.34s
  - Success Rate:       100.0%
```

## Integration with Existing System

This testing framework integrates with your existing multi-agent system by:
1. Using the same agent classes (StrategicAnalyst, AudienceEvaluator)
2. Temporarily overriding system prompts for testing
3. Maintaining all existing configurations
4. Generating outputs in your standard format

No changes required to your existing agents!

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Ensure `.env` file exists in project root
- Verify the key is correctly formatted
- Try loading environment manually: `source .env`

### "ModuleNotFoundError: No module named 'agents'"
- Ensure you're running from the project root directory
- Verify `agents/` folder exists with your agent implementations
- Check `__init__.py` files are in place

### "No variants found for agent"
- Check [config/prompt_variants.json](config/prompt_variants.json) exists
- Verify JSON syntax is valid
- Ensure agent name matches exactly (e.g., 'strategic_analyst')

## Next Steps

1. **Run Initial Tests**: Use `python test_prompts.py` to establish baseline performance
2. **Analyze Results**: Review generated reports in `outputs/tests/`
3. **Deploy Winner**: Update your main config to use the best-performing variant
4. **Iterate**: Create new variants based on insights, test again
5. **Monitor**: Track performance over time with different document types

## Advanced Usage

### Custom Ground Truth Validation

Add expert-coded correct answers for accuracy measurement:

```python
ground_truth = {
    'strategic_assessment': 'Expected strategic insight',
    'key_strength': 'Expected strength',
    'key_weakness': 'Expected weakness'
}

results = tester.run_ab_test(
    agent_name='strategic_analyst',
    input_data=input_data,
    ground_truth=ground_truth,
    iterations=5
)
```

### Batch Testing Multiple Agents

```python
for agent in ['strategic_analyst', 'audience_evaluator']:
    results = tester.run_ab_test(
        agent_name=agent,
        input_data=input_data,
        iterations=3
    )
    tester.save_test_results(results)
```

## Research Foundation

This testing framework is based on the methodology from your dissertation:
- Within-subjects experimental design
- Multiple quality dimensions (specificity, actionability, technical precision)
- Comparative statistical analysis
- Expert ground truth validation option

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the example in [test_prompts.py](test_prompts.py)
3. Examine the detailed docstrings in [orchestrator/prompt_tester.py](orchestrator/prompt_tester.py)

## License

This is a research tool developed for your dissertation project.
