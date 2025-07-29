#!/usr/bin/env python3
"""
Script to visualize accuracy results from GPQA log files using Weights & Biases.

Usage:
    python visualize_accuracy.py --log_file path/to/log/file.log --project_name "GPQA Results"
"""

import argparse
import re
import wandb
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


def parse_log_file(log_file_path):
    """
    Parse a GPQA log file to extract question results.
    
    Args:
        log_file_path (str): Path to the log file
        
    Returns:
        dict: Dictionary containing experiment info and results
    """
    with open(log_file_path, 'r') as f:
        content = f.read()
    
    # Extract experiment configuration
    config = {}
    config_patterns = {
        'model': r'Model: (.+)',
        'prompt_type': r'Prompt Type: (.+)',
        'seed': r'Seed: (\d+)',
        'total_questions': r'Total Questions: (\d+)',
        'max_examples': r'Max Examples: (.+)'
    }
    
    for key, pattern in config_patterns.items():
        match = re.search(pattern, content)
        if match:
            config[key] = match.group(1)
    
    # Extract question results
    results = []
    question_pattern = r'Question (\d+): (CORRECT|INCORRECT)'
    matches = re.findall(question_pattern, content)
    
    for question_num, result in matches:
        results.append({
            'question_id': int(question_num),
            'correct': result == 'CORRECT'
        })
    
    return {
        'config': config,
        'results': results
    }


def create_accuracy_visualization(data, project_name="GPQA Results"):
    """
    Create and log accuracy visualization to Weights & Biases.
    
    Args:
        data (dict): Parsed log data
        project_name (str): W&B project name
    """
    # Initialize W&B with personal account to avoid org permission issues
    try:
        wandb.init(project=project_name, config=data['config'], entity=None)
    except Exception as e:
        print(f"W&B initialization failed: {e}")
        print("Trying with personal account...")
        # Try with personal account explicitly
        wandb.init(project=project_name, config=data['config'], entity="jacob-mccarran")
    
    # Create DataFrame
    df = pd.DataFrame(data['results'])
    
    # Create bar chart
    fig = go.Figure()
    
    # Add bars for correct answers (green)
    correct_data = df[df['correct'] == True]
    if not correct_data.empty:
        fig.add_trace(go.Bar(
            x=correct_data['question_id'],
            y=[1] * len(correct_data),
            name='Correct',
            marker_color='green',
            showlegend=True
        ))
    
    # Add bars for incorrect answers (red)
    incorrect_data = df[df['correct'] == False]
    if not incorrect_data.empty:
        fig.add_trace(go.Bar(
            x=incorrect_data['question_id'],
            y=[1] * len(incorrect_data),
            name='Incorrect',
            marker_color='red',
            showlegend=True
        ))
    
    # Update layout
    fig.update_layout(
        title=f"Question-by-Question Accuracy - {data['config'].get('model', 'Unknown Model')}",
        xaxis_title="Question Number",
        yaxis_title="Result",
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1],
            ticktext=['Incorrect', 'Correct'],
            range=[-0.5, 1.5]
        ),
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Log to W&B
    wandb.log({
        "accuracy_by_question": wandb.plotly(fig),
        "total_questions": len(data['results']),
        "correct_answers": len(correct_data),
        "incorrect_answers": len(incorrect_data),
        "accuracy_percentage": (len(correct_data) / len(data['results'])) * 100 if data['results'] else 0
    })
    
    # Create summary table
    summary_table = wandb.Table(columns=["Metric", "Value"])
    summary_table.add_data("Total Questions", len(data['results']))
    summary_table.add_data("Correct Answers", len(correct_data))
    summary_table.add_data("Incorrect Answers", len(incorrect_data))
    summary_table.add_data("Accuracy", f"{(len(correct_data) / len(data['results'])) * 100:.2f}%" if data['results'] else "0%")
    summary_table.add_data("Model", data['config'].get('model', 'Unknown'))
    summary_table.add_data("Prompt Type", data['config'].get('prompt_type', 'Unknown'))
    summary_table.add_data("Seed", data['config'].get('seed', 'Unknown'))
    
    wandb.log({"summary": summary_table})
    
    # Create detailed results table
    results_table = wandb.Table(columns=["Question ID", "Result", "Status"])
    for result in data['results']:
        status = "✅ Correct" if result['correct'] else "❌ Incorrect"
        results_table.add_data(result['question_id'], "Correct" if result['correct'] else "Incorrect", status)
    
    wandb.log({"detailed_results": results_table})
    
    print(f"Visualization logged to W&B project: {project_name}")
    print(f"Model: {data['config'].get('model', 'Unknown')}")
    print(f"Total Questions: {len(data['results'])}")
    print(f"Correct: {len(correct_data)}")
    print(f"Incorrect: {len(incorrect_data)}")
    print(f"Accuracy: {(len(correct_data) / len(data['results'])) * 100:.2f}%" if data['results'] else "0%")
    
    wandb.finish()


def main():
    parser = argparse.ArgumentParser(description='Visualize GPQA accuracy results in Weights & Biases')
    parser.add_argument('--log_file', required=True, help='Path to the log file')
    parser.add_argument('--project_name', default='GPQA Results', help='W&B project name')
    parser.add_argument('--wandb_entity', help='W&B entity/username (optional, defaults to logged-in user)')
    
    args = parser.parse_args()
    
    # Check if log file exists
    if not Path(args.log_file).exists():
        print(f"Error: Log file '{args.log_file}' not found.")
        return
    
    # Parse log file
    print(f"Parsing log file: {args.log_file}")
    data = parse_log_file(args.log_file)
    
    if not data['results']:
        print("Error: No question results found in the log file.")
        return
    
    # Create visualization (W&B will use the logged-in user by default)
    create_accuracy_visualization(data, args.project_name)


if __name__ == "__main__":
    main() 