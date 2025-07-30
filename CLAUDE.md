# GPQA Evaluation System - Claude Development Guide

This is a comprehensive evaluation framework for the GPQA (Graduate-Level Google-Proof Q&A) benchmark, supporting multiple language models, prompt strategies, and analysis workflows.

## High-Level Architecture

The GPQA system is built around a modular evaluation pipeline that supports:

- **Multiple Model APIs**: OpenAI (GPT-3.5, GPT-4) and Anthropic (Claude models)
- **Diverse Prompt Strategies**: Zero-shot, few-shot, chain-of-thought, self-consistency, and retrieval-augmented approaches  
- **Comprehensive Evaluation**: Detailed logging, caching, visualization, and statistical analysis
- **Flexible Data Handling**: Support for different GPQA dataset variants with shuffled answer choices

### Core Components

1. **`baselines/run_baseline.py`** - Main evaluation orchestrator with `AnswerPredictor` class
2. **`baselines/utils.py`** - Shared utilities for model calls, prompt generation, and data loading
3. **`baselines/open_book.py`** - Retrieval-augmented evaluation using Bing search
4. **`plotter.py`** - Response time and performance visualization
5. **`visualize_accuracy.py`** - Weights & Biases integration for experiment tracking
6. **`run_baseline_comprehensive.sh`** - Batch experiment runner with extensive configuration options

### Data Flow

```
CSV Dataset → load_examples() → create_prompts() → Model API → parse_answer() → Cache & Log → Visualization
```

## Environment Setup

### Prerequisites

```bash
# Create conda environment
conda create -n gpqa python=3.9
conda activate gpqa

# Install dependencies
pip install -r requirements.txt

# For visualization features
pip install -r requirements_visualization.txt
```

### API Configuration

Create a `.env` file with your API keys:

```bash
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
BING_SEARCH_V7_SUBSCRIPTION_KEY=your_bing_key_here  # For retrieval baselines
```

### Dataset Setup

The GPQA dataset is password-protected. Extract `dataset.zip` with password: `deserted-untie-orchid`

Available datasets:
- `dataset/gpqa_main.csv` - Core benchmark 
- `dataset/gpqa_extended.csv` - Extended version
- `dataset/gpqa_experts.csv` - Expert-validated subset
- `dataset/gpqa_diamond.csv` - Highest quality subset

## Common Development Commands

### Basic Evaluation

```bash
# Quick test with Claude Sonnet 4 (40 questions)
python baselines/run_baseline.py main \
  --model_name claude-sonnet-4-20250514 \
  --data_filename dataset/gpqa_main.csv \
  --prompt_type zero_shot \
  --max_examples 40 \
  --seed 0 \
  --verbose

# Test with different prompt strategies
python baselines/run_baseline.py main \
  --model_name claude-3-5-sonnet-20241022 \
  --data_filename dataset/gpqa_diamond.csv \
  --prompt_type chain_of_thought \
  --max_examples 20 \
  --seed 0
```

### Comprehensive Evaluation

```bash
# Run all closed-book baselines for GPT-4
for prompt_type in zero_shot 5_shot zero_shot_chain_of_thought chain_of_thought; do
  python baselines/run_baseline.py main \
    --model_name gpt-4 \
    --data_filename dataset/gpqa_main.csv \
    --prompt_type $prompt_type \
    --verbose
done

# Run open-book baselines (requires Bing API key)
for prompt_type in retrieval retrieval_content; do
  python baselines/run_baseline.py main \
    --model_name gpt-4 \
    --data_filename dataset/gpqa_main.csv \
    --prompt_type $prompt_type \
    --verbose
done
```

### Batch Experiments

```bash
# Use the comprehensive runner for systematic evaluation
./run_baseline_comprehensive.sh \
  --models claude-sonnet-4-20250514,claude-3-5-sonnet-20241022 \
  --prompt-types zero_shot,chain_of_thought \
  --max-examples 10,20 \
  --seeds 0,1,2 \
  --save-results \
  --show-plot

# Quick validation run
./run_baseline_comprehensive.sh \
  --models claude-sonnet-4-20250514 \
  --prompt-types zero_shot \
  --max-examples 5 \
  --seeds 0 \
  --verbose \
  --save-results
```

### Results Analysis and Visualization

```bash
# Generate performance plots from results CSV
python plotter.py tmp_logs/30_07_2025/16_49_34_40_test.csv --additional

# Create W&B visualization from log files
python visualize_accuracy.py \
  --log_file logs/claude-sonnet-4-20250514_40_total_questions_seed=0.log \
  --project_name "GPQA Analysis"

# Offline visualization (no W&B required)
python visualize_accuracy_offline.py \
  --log_file logs/claude-sonnet-4-20250514_40_total_questions_seed=0.log \
  --output results_visualization.html
```

### Answer-Only Baselines

```bash
# Train T5-based span identification model
python baselines/answer_only.py --epochs 25

# Train CBOW model  
python baselines/answer_cbow.py
```

## Key Development Patterns

### Model Integration

The system supports both OpenAI and Anthropic models through a unified interface:

```python
# In utils.py - Model selection and API calling
def call_model_with_retries(prompt, model_name, call_type='sample', temperature=0.0):
    api_type = get_api_type(model_name)  # 'openai' or 'anthropic'
    response = select_and_call_model(prompt, model_name, call_type, temperature)
    return response
```

Supported models:
- **OpenAI**: `gpt-3.5-turbo-16k-0613`, `gpt-4`, `gpt-4-1106-preview`
- **Anthropic**: `claude-3-5-sonnet-20241022`, `claude-3-5-haiku-20241022`, `claude-3-opus-20240229`, `claude-sonnet-4-20250514`, `claude-opus-4-20250514`

### Prompt Engineering

Prompt templates are located in `prompts/` with different strategies:

- **Zero-shot**: Direct question + choices + format instruction
- **Few-shot (5_shot)**: Examples from `chain_of_thought_examples.json` without explanations
- **Chain-of-thought**: Examples with step-by-step reasoning
- **Self-consistency**: Multiple samples with temperature=0.7, majority vote
- **Retrieval**: Bing search integration with content scraping

### Caching System

Aggressive caching prevents redundant API calls:

```python
# Cache key: (model_name, prompt_type, prompt_text)
cache_filename = f"cache_{model_name}.pkl"
```

Use `--overwrite_cache` to bypass cached responses during development.

### Results Management

Two output modes:

1. **Standard logs**: Detailed CSV with individual question results (`logs/`)
2. **Simplified results**: Aggregated metrics for plotting (`tmp_logs/` with `--save_results`)

### Answer Parsing

Robust regex-based answer extraction:

```python
patterns = [r'answer is \((.)\)', r'Answer: \((.)\)', r'answer: \((.)\)', r'answer \((.)\)', r'\((.)\)']
```

Models must respond with format like "The correct answer is (A)"

## Important Configuration Notes

### Seed Handling

- Seed controls answer choice shuffling (not model randomness)
- Use consistent seeds for reproducible evaluations
- Different seeds create different question orderings

### Max Examples

- Use small values (5-20) during development to control costs
- Full evaluation typically uses 100+ questions
- `max_examples` truncates the dataset after loading

### Temperature Settings

- Standard evaluation uses temperature=0.0 (deterministic)
- Self-consistency uses temperature=0.7 with multiple samples
- Chain-of-thought prompt generation uses temperature=0.0

### Verbose Mode

Essential for debugging:
- Shows full prompts and responses
- Displays correct vs chosen answers
- Useful for prompt engineering and error analysis

## File Structure Reference

```
gpqa/
├── baselines/                 # Core evaluation logic
│   ├── run_baseline.py       # Main evaluation orchestrator
│   ├── utils.py              # Shared utilities and model interfaces  
│   ├── open_book.py          # Retrieval-augmented evaluation
│   ├── closed_book.py        # Alternative evaluation interface
│   ├── answer_only.py        # T5 span identification baseline
│   └── answer_cbow.py        # CBOW baseline
├── prompts/                   # Prompt templates and examples
│   ├── chain_of_thought_examples.json
│   ├── bing-search-cot.txt
│   └── bing-search-cot-content.txt
├── dataset/                   # GPQA benchmark data
│   ├── gpqa_main.csv
│   ├── gpqa_diamond.csv
│   └── ...
├── logs/                      # Detailed evaluation results
├── baseline_results/          # Published baseline results
├── tmp_logs/                  # Simplified results for plotting
├── cache_*.pkl                # Model response caches
├── plotter.py                 # Response time visualization
├── visualize_accuracy.py      # W&B integration
├── visualize_accuracy_offline.py  # Local HTML visualization
├── run_baseline_comprehensive.sh  # Batch experiment runner
└── requirements.txt           # Python dependencies
```

## Best Practices for Development

1. **Start Small**: Use `--max_examples 5` and `--verbose` for initial testing
2. **Cache Management**: Delete relevant cache files when changing prompts
3. **Systematic Evaluation**: Use the comprehensive runner for production runs
4. **Seed Consistency**: Use the same seed across models for fair comparison
5. **Result Analysis**: Always generate plots to understand model behavior patterns
6. **API Cost Control**: Monitor usage with small batches before large-scale evaluation

This system provides a robust foundation for evaluating language models on graduate-level scientific reasoning tasks with comprehensive analysis and visualization capabilities.