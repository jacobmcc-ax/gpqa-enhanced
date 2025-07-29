# GPQA Accuracy Visualization with Weights & Biases

This script creates interactive visualizations of GPQA accuracy results using Weights & Biases (W&B).

## Features

- **Bar Chart Visualization**: Shows correct/incorrect answers for each question
- **Summary Tables**: Displays overall statistics and detailed results
- **Interactive Plots**: Built with Plotly for interactive exploration
- **W&B Integration**: Automatic logging to your W&B dashboard

## Installation

1. Install the required packages:
```bash
pip install -r requirements_visualization.txt
```

2. Login to Weights & Biases:
```bash
wandb login
```

## Usage

### Basic Usage

```bash
python visualize_accuracy.py --log_file logs/your_log_file.log
```

### Advanced Usage

```bash
python visualize_accuracy.py \
    --log_file logs/claude-3-5-sonnet-20241022_9_total_questions_seed=2.log \
    --project_name "GPQA Analysis" \
    --wandb_entity your_username
```

### Parameters

- `--log_file`: Path to the GPQA log file (required)
- `--project_name`: W&B project name (default: "GPQA Results")
- `--wandb_entity`: Your W&B username/entity (optional)

## What the Script Creates

### 1. Bar Chart Visualization
- **X-axis**: Question number (0, 1, 2, ...)
- **Y-axis**: Result (Correct/Incorrect)
- **Colors**: Green for correct answers, Red for incorrect answers
- **Interactive**: Hover over bars to see details

### 2. Summary Table
- Total questions evaluated
- Number of correct/incorrect answers
- Overall accuracy percentage
- Model information
- Prompt type and seed

### 3. Detailed Results Table
- Question-by-question breakdown
- Visual indicators (✅/❌) for quick scanning
- Question ID and result status

## Example Output

When you run the script, you'll see output like:

```
Parsing log file: logs/claude-3-5-sonnet-20241022_9_total_questions_seed=2.log
Visualization logged to W&B project: GPQA Results
Model: claude-3-5-sonnet-20241022
Total Questions: 9
Correct: 7
Incorrect: 2
Accuracy: 77.78%
```

## Log File Format

The script expects log files with the following format:
```
2025-07-28 17:18:29,815 - INFO - Question 0: CORRECT
2025-07-28 17:18:29,815 - INFO - Question 1: CORRECT
2025-07-28 17:18:29,816 - INFO - Question 2: INCORRECT
...
```

## Troubleshooting

### Common Issues

1. **"No question results found"**: Make sure your log file contains lines with "Question X: CORRECT/INCORRECT"

2. **W&B authentication error**: Run `wandb login` and enter your API key

3. **Missing dependencies**: Install requirements with `pip install -r requirements_visualization.txt`

### Getting Your W&B API Key

1. Go to [wandb.ai](https://wandb.ai)
2. Sign in to your account
3. Go to Settings → API Keys
4. Copy your API key
5. Run `wandb login` and paste the key

## Example

Here's a complete example workflow:

```bash
# 1. Run your GPQA evaluation
python baselines/run_baseline.py main \
    --model_name claude-3-5-sonnet-20241022 \
    --data_filename dataset/gpqa_main.csv \
    --prompt_type chain_of_thought \
    --max_examples 9 \
    --seed 2

# 2. Visualize the results
python visualize_accuracy.py \
    --log_file logs/claude-3-5-sonnet-20241022_9_total_questions_seed=2.log \
    --project_name "GPQA Analysis" \
    --wandb_entity your_username
```

The visualization will be available in your W&B dashboard with interactive charts and detailed statistics. 