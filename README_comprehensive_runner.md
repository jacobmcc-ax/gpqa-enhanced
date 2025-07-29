# Comprehensive Baseline Runner

This script allows you to run multiple configurations of the GPQA baseline experiments efficiently.

## Quick Start

### 1. Basic Usage
```bash
# Run a simple test with just one model and prompt type
./run_baseline_comprehensive.sh -m claude-sonnet-4-20250514 -p chain_of_thought -e 5 -s 0

# Run all configurations (WARNING: This will run 500+ experiments!)
./run_baseline_comprehensive.sh
```

### 2. Customized Experiments
```bash
# Test multiple models with specific prompt types
./run_baseline_comprehensive.sh -m claude-sonnet-4-20250514,claude-3-5-sonnet-20241022 -p zero_shot,chain_of_thought

# Test with different dataset sizes
./run_baseline_comprehensive.sh -e 5,10,20 -s 0,1

# Enable verbose output and overwrite cache
./run_baseline_comprehensive.sh -v -o -m claude-sonnet-4-20250514

# Save simplified results log
./run_baseline_comprehensive.sh -r -m claude-sonnet-4-20250514 -p chain_of_thought -e 10
```

### 3. Using Configuration Files
```bash
# Create your own config file
cp example_config.sh my_config.sh
# Edit my_config.sh with your desired settings

# Run with your config
./run_baseline_comprehensive.sh -c my_config.sh
```

### 4. Complex Multi-Model Experiments
```bash
# Compare multiple Claude models with chain of thought
./run_baseline_comprehensive.sh -o -r -p -m claude-sonnet-4-20250514,claude-opus-4-20250514 -p chain_of_thought -e 10,20

# Test different prompt types across multiple models
./run_baseline_comprehensive.sh -o -r -p -m claude-sonnet-4-20250514,claude-opus-4-20250514 -p chain_of_thought,zero_shot,5_shot -e 10,20

# Comprehensive comparison with multiple seeds
./run_baseline_comprehensive.sh -o -r -p -a -m claude-sonnet-4-20250514,claude-opus-4-20250514 -p chain_of_thought,zero_shot -e 10,20 -s 0,1,2

# Test specific models on specific datasets
./run_baseline_comprehensive.sh -o -r -p -m claude-sonnet-4-20250514 -p chain_of_thought -d dataset/gpqa_main.csv,dataset/gpqa_experts.csv -e 20
```

### 5. Quick Testing Examples
```bash
# Quick test with small sample size
./run_baseline_comprehensive.sh -o -r -p -m claude-sonnet-4-20250514 -p chain_of_thought -e 5

# Test multiple prompt types quickly
./run_baseline_comprehensive.sh -o -r -p -m claude-sonnet-4-20250514 -p chain_of_thought,zero_shot,5_shot -e 5

# Compare models with minimal examples
./run_baseline_comprehensive.sh -o -r -p -m claude-sonnet-4-20250514,claude-opus-4-20250514 -p chain_of_thought -e 5
```

### 6. Production Runs
```bash
# Full evaluation with all models and prompt types
./run_baseline_comprehensive.sh -o -r -p -a -m claude-sonnet-4-20250514,claude-opus-4-20250514,claude-3-5-sonnet-20241022 -p chain_of_thought,zero_shot,5_shot,self_consistency -e 50,100 -s 0,1,2

# Large-scale comparison with multiple seeds
./run_baseline_comprehensive.sh -o -r -p -a -m claude-sonnet-4-20250514,claude-opus-4-20250514 -p chain_of_thought,zero_shot -e 100 -s 0,1,2,3,4
```

## Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-m, --models` | Specify models to test | `-m claude-sonnet-4-20250514,gpt-4` |
| `-p, --prompt-types` | Specify prompt types | `-p zero_shot,chain_of_thought` |
| `-d, --datasets` | Specify datasets | `-d dataset/gpqa_main.csv` |
| `-e, --max-examples` | Specify number of examples | `-e 5,10,20` |
| `-s, --seeds` | Specify random seeds | `-s 0,1,2` |
| `-v, --verbose` | Enable verbose output | `-v` |
| `-o, --overwrite-cache` | Overwrite existing cache | `-o` |
| `-r, --save-results` | Save simplified results to CSV | `-r` |
| `-p, --show-plot` | Generate plots after saving results | `-p` |
| `-a, --additional-plots` | Include additional analysis plots | `-a` |
| `-c, --config` | Load config from file | `-c my_config.sh` |
| `-h, --help` | Show help message | `-h` |

## Available Models

### Anthropic Models
- `claude-2`
- `claude-3-5-sonnet-20241022`
- `claude-3-5-haiku-20241022`
- `claude-3-opus-20240229`
- `claude-sonnet-4-20250514`
- `claude-opus-4-20250514`

### OpenAI Models
- `text-ada-001`
- `text-babbage-001`
- `text-curie-001`
- `text-davinci-002`
- `text-davinci-003`
- `gpt-3.5-turbo-16k-0613`
- `gpt-4`
- `gpt-4-1106-preview`

## Available Prompt Types

- `zero_shot` - Basic zero-shot prompting
- `chain_of_thought` - Chain-of-thought reasoning
- `5_shot` - 5-shot prompting with examples
- `self_consistency` - Self-consistency sampling (20 samples)
- `zero_shot_chain_of_thought` - Zero-shot with generated reasoning
- `retrieval` - Retrieval-augmented generation
- `retrieval_content` - Retrieval with URL content

## Available Datasets

- `dataset/gpqa_main.csv`
- `dataset/gpqa_extended.csv`
- `dataset/gpqa_experts.csv`
- `dataset/gpqa_diamond.csv`

## Output and Logging

### Log Files
- Individual experiment logs: `logs/{model}_{prompt_type}_{examples}ex_seed{seed}_{timestamp}.log`
- Summary file: `logs/experiment_summary_{timestamp}.txt`

### Simplified Results CSV
When using the `-r` or `--save-results` flag, the script creates a simplified CSV file with the format:
`tmp_logs/{day}_{month}_{year}/{hour}_{minute}_{second}_{max_examples}_test.csv`

This CSV file contains only the essential metrics with the following columns:
- `num_questions_asked`: Total number of questions processed
- `num_questions_correct`: Number of questions answered correctly
- `num_questions_incorrect`: Number of questions answered incorrectly
- `num_questions_not_answered`: Number of questions that didn't get answered
- `correct_question_ids`: List of question IDs answered correctly (as string)
- `incorrect_question_ids`: List of question IDs answered incorrectly (as string)

**Note**: When `save_results=False`, no logging or CSV files are created. When `save_results=True`, only the simplified results CSV is created in the `tmp_logs` directory.

### CSV Results
- No CSV files are created when using the simplified results mode (`save_results=True`)
- When `save_results=False`, no files are created at all

## Performance Considerations

### Time Estimates
- **Zero-shot**: ~30-60 seconds per experiment
- **Chain-of-thought**: ~60-120 seconds per experiment
- **Self-consistency**: ~10-20 minutes per experiment (20 samples)
- **5-shot**: ~60-120 seconds per experiment

### Cost Estimates
- **Claude models**: ~$0.01-0.05 per experiment
- **GPT models**: ~$0.01-0.10 per experiment
- **Self-consistency**: 20x the cost of single experiments

### Recommended Workflows

#### 1. Quick Testing (5-10 minutes)
```bash
./run_baseline_comprehensive.sh -m claude-sonnet-4-20250514 -p zero_shot,chain_of_thought -e 5 -s 0
```

#### 2. Medium Scale (1-2 hours)
```bash
./run_baseline_comprehensive.sh -m claude-sonnet-4-20250514,claude-3-5-sonnet-20241022 -p zero_shot,chain_of_thought,5_shot -e 10,20 -s 0,1
```

#### 3. Full Scale (8+ hours)
```bash
./run_baseline_comprehensive.sh -c example_config.sh
```

## Tips and Best Practices

1. **Start small**: Always test with a few examples first
2. **Use cache**: Don't use `-o` unless you want to regenerate results
3. **Monitor costs**: Self-consistency experiments are expensive
4. **Check logs**: Review log files for any errors or issues
5. **Use timeouts**: The script has 1-hour timeouts per experiment
6. **API limits**: The script includes delays to respect API rate limits

## Troubleshooting

### Common Issues

1. **Permission denied**: Make sure the script is executable
   ```bash
   chmod +x run_baseline_comprehensive.sh
   ```

2. **API key not found**: Ensure your environment variables are set
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   export OPENAI_API_KEY="your-key-here"
   ```

3. **Dataset not found**: Check that dataset files exist in the correct location

4. **Timeout errors**: Some experiments (especially self-consistency) may take longer than 1 hour

### Getting Help
```bash
./run_baseline_comprehensive.sh --help
```

## Example Configurations

### Minimal Test
```bash
./run_baseline_comprehensive.sh -m claude-sonnet-4-20250514 -p zero_shot -e 5 -s 0
```

### Model Comparison
```bash
./run_baseline_comprehensive.sh -m claude-sonnet-4-20250514,claude-3-5-sonnet-20241022,gpt-4 -p zero_shot,chain_of_thought -e 20 -s 0,1,2
```

### Prompt Type Analysis
```bash
./run_baseline_comprehensive.sh -m claude-sonnet-4-20250514 -p zero_shot,chain_of_thought,5_shot,self_consistency -e 10 -s 0
``` 