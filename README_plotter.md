# GPQA Response Time Plotter

This script creates visualizations for response time analysis from GPQA evaluation results.

## Features

- **Main Time Analysis Plots**: Creates two plots similar to the reference image:
  - Distribution of Response Times (histogram with mean line)
  - Response Time by Correctness (scatter plot)
- **Additional Analysis Plots**: Four additional plots for deeper analysis:
  - Box plot of response times by correctness
  - Cumulative distribution of response times
  - Response time trend over question numbers
  - Accuracy by response time bins
- **Statistical Summary**: Comprehensive statistics including t-tests
- **Automatic File Organization**: Saves plots to `tmp_logs/plots/` by default

## Usage

### Basic Usage
```bash
python plotter.py path/to/your/results.csv
```

### Save plots without displaying
```bash
python plotter.py path/to/your/results.csv --no-show
```

### Create additional analysis plots
```bash
python plotter.py path/to/your/results.csv --additional
```

### Custom output location
```bash
python plotter.py path/to/your/results.csv --output-dir custom/plots/dir
```

### Custom output filename
```bash
python plotter.py path/to/your/results.csv --output my_analysis.png
```

## Command Line Options

- `csv_file`: Path to the CSV file with GPQA results (required)
- `--output, -o`: Output file for the main plot (default: auto-generated in tmp_logs/plots/)
- `--output-dir, -d`: Output directory for all plots (default: tmp_logs/plots/)
- `--no-show`: Do not display plots (only save)
- `--additional, -a`: Create additional analysis plots

## Input CSV Format

The script expects CSV files created by the modified `run_baseline.py` with the following columns:

- `num_questions_asked`: Total number of questions
- `num_questions_correct`: Number of correct answers
- `num_questions_incorrect`: Number of incorrect answers
- `num_questions_not_answered`: Number of unanswered questions
- `correct_question_ids`: List of correctly answered question IDs (as string)
- `incorrect_question_ids`: List of incorrectly answered question IDs (as string)
- `response_times`: List of response times in seconds (as string)

## Output

### Default Behavior
- Creates `tmp_logs/plots/` directory if it doesn't exist
- Saves main plots as `{csv_basename}_time_analysis.png`
- Saves additional plots as `{csv_basename}_additional_analysis.png` (if --additional flag used)
- Displays plots on screen (unless --no-show is used)

### Example Output Files
```
tmp_logs/plots/
├── 29_07_2025_16_24_27_3_test_time_analysis.png
├── 29_07_2025_16_24_27_3_test_additional_analysis.png
└── ...
```

## Example

1. Run baseline evaluation with response time tracking:
```bash
python baselines/run_baseline.py main --model_name claude-sonnet-4-20250514 --data_filename dataset/gpqa_main.csv --prompt_type chain_of_thought --max_examples 20 --seed 0 --save_results
```

2. Create plots from the generated CSV:
```bash
python plotter.py tmp_logs/29_07_2025/16_24_27_20_test.csv --additional
```

## Dependencies

- pandas
- matplotlib
- numpy
- scipy (for statistical tests)

## Test

Run the test script to create sample data and test the plotter:
```bash
python test_plotter.py
python plotter.py tmp_logs/test_response_times.csv --additional
``` 