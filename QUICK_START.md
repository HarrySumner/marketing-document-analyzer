# Quick Start Guide

Get up and running with the Prompt Testing System in 5 minutes.

## Step 1: Install Dependencies

```bash
pip install anthropic python-dotenv
```

## Step 2: Set Up API Key

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_api_key_here
```

## Step 3: Run Your First Test

```bash
cd "C:\Users\harry\OneDrive\Desktop\Research Assistant"
python test_prompts.py
```

This will:
- Test 4 different prompt variants for the strategic analyst
- Run 3 iterations per variant
- Generate performance reports
- Identify the best-performing prompt

**Expected output:**
```
============================================================
A/B Testing: strategic_analyst
Iterations per variant: 3
============================================================

Testing v1_expert_framed: Expert Marketing Consultant
  Iteration 1/3 complete
  Iteration 2/3 complete
  Iteration 3/3 complete
  ✓ v1_expert_framed testing complete

[... continues for all variants ...]

======================================================================
WINNER:
  Expert Marketing Consultant
  Composite Score: 0.847
======================================================================
```

## Step 4: Try Interactive Mode

```bash
python interactive.py
```

**Quick workflow:**
```
>>> help                  # See all commands

>>> input                 # Enter test document
[Paste your marketing copy]
[Press Ctrl+Z then Enter on Windows, Ctrl+D on Mac/Linux]

>>> analyze               # Run analysis

>>> test                  # A/B test prompts
Select agent (1 or 2): 1
Number of iterations: 3

>>> history               # View past results

>>> quit                  # Exit
```

## Step 5: Review Results

Results are saved in `outputs/tests/`:
- **JSON file**: Full data for further analysis
- **TXT report**: Human-readable summary with recommendations

Example report location:
```
outputs/tests/ab_test_strategic_analyst_20240115_143000_report.txt
```

## What's Next?

1. **Customize Prompts**: Edit [config/prompt_variants.json](config/prompt_variants.json)
2. **Test Different Documents**: Try various marketing materials
3. **Compare Agents**: Test both strategic_analyst and audience_evaluator
4. **Deploy Winner**: Use the best-performing variant in production

## Common Commands

### Batch Testing
```bash
python test_prompts.py
```

### Interactive Analysis
```bash
python interactive.py
>>> input
>>> analyze
```

### Load from File
```bash
python interactive.py
>>> load marketing_copy.txt
>>> analyze
```

## Quick Customization

Want to add your own prompt variant? Edit `config/prompt_variants.json`:

```json
{
  "strategic_analyst": {
    "variants": {
      "v5_my_variant": {
        "name": "My Custom Prompt",
        "temperature": 0.3,
        "system_prompt": "Your custom prompt here...",
        "hypothesis": "Why you think this will work",
        "expected_performance": "What you expect"
      }
    }
  }
}
```

Then run `python test_prompts.py` to test it!

## Troubleshooting

**"ANTHROPIC_API_KEY not found"**
- Make sure `.env` file exists
- Check the API key is correct

**"No module named 'agents'"**
- Ensure you have the `agents/` folder with your agent implementations
- Run from the project root directory

**Need more help?**
- See [README.md](README.md) for detailed documentation
- Check example code in [test_prompts.py](test_prompts.py)

---

That's it! You're ready to optimize your prompts. 🚀
