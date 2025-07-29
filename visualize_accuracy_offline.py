#!/usr/bin/env python3
"""
Offline version of GPQA accuracy visualization script.

This script creates local HTML visualizations without requiring W&B permissions.
"""

import argparse
import re
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime


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


def create_accuracy_visualization(data, output_dir="visualizations"):
    """
    Create local HTML visualizations of accuracy results.
    
    Args:
        data (dict): Parsed log data
        output_dir (str): Directory to save visualizations
    """
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Create DataFrame
    df = pd.DataFrame(data['results'])
    
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_name = data['config'].get('model', 'unknown_model').replace('-', '_').replace('.', '_')
    
    # 1. Create bar chart
    fig_bar = go.Figure()
    
    # Add bars for correct answers (green)
    correct_data = df[df['correct'] == True]
    if not correct_data.empty:
        fig_bar.add_trace(go.Bar(
            x=correct_data['question_id'],
            y=[1] * len(correct_data),
            name='Correct',
            marker_color='green',
            showlegend=True
        ))
    
    # Add bars for incorrect answers (red)
    incorrect_data = df[df['correct'] == False]
    if not incorrect_data.empty:
        fig_bar.add_trace(go.Bar(
            x=incorrect_data['question_id'],
            y=[1] * len(incorrect_data),
            name='Incorrect',
            marker_color='red',
            showlegend=True
        ))
    
    # Update layout
    fig_bar.update_layout(
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
    
    # Save bar chart
    bar_filename = f"{output_dir}/{model_name}_{timestamp}_accuracy_bar.html"
    fig_bar.write_html(bar_filename)
    
    # 2. Create summary statistics
    total_questions = len(data['results'])
    correct_count = len(correct_data)
    incorrect_count = len(incorrect_data)
    accuracy = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    
    # Create summary table
    summary_data = {
        'Metric': ['Total Questions', 'Correct Answers', 'Incorrect Answers', 'Accuracy', 'Model', 'Prompt Type', 'Seed'],
        'Value': [
            total_questions,
            correct_count,
            incorrect_count,
            f"{accuracy:.2f}%",
            data['config'].get('model', 'Unknown'),
            data['config'].get('prompt_type', 'Unknown'),
            data['config'].get('seed', 'Unknown')
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    fig_table = go.Figure(data=[go.Table(
        header=dict(values=list(summary_df.columns), fill_color='paleturquoise', align='left'),
        cells=dict(values=[summary_df[col] for col in summary_df.columns], fill_color='lavender', align='left'))
    ])
    
    fig_table.update_layout(title="Summary Statistics")
    table_filename = f"{output_dir}/{model_name}_{timestamp}_summary.html"
    fig_table.write_html(table_filename)
    
    # 3. Create detailed results table
    results_data = []
    for result in data['results']:
        status = "✅ Correct" if result['correct'] else "❌ Incorrect"
        results_data.append({
            'Question ID': result['question_id'],
            'Result': "Correct" if result['correct'] else "Incorrect",
            'Status': status
        })
    
    results_df = pd.DataFrame(results_data)
    fig_results = go.Figure(data=[go.Table(
        header=dict(values=list(results_df.columns), fill_color='paleturquoise', align='left'),
        cells=dict(values=[results_df[col] for col in results_df.columns], fill_color='lavender', align='left'))
    ])
    
    fig_results.update_layout(title="Detailed Results")
    results_filename = f"{output_dir}/{model_name}_{timestamp}_detailed_results.html"
    fig_results.write_html(results_filename)
    
    # 4. Create accuracy trend chart
    cumulative_correct = []
    cumulative_accuracy = []
    
    for i in range(1, total_questions + 1):
        correct_so_far = df.head(i)['correct'].sum()
        cumulative_correct.append(correct_so_far)
        cumulative_accuracy.append((correct_so_far / i) * 100)
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=list(range(1, total_questions + 1)),
        y=cumulative_accuracy,
        mode='lines+markers',
        name='Cumulative Accuracy',
        line=dict(color='blue', width=2),
        marker=dict(size=6)
    ))
    
    fig_trend.update_layout(
        title="Cumulative Accuracy Trend",
        xaxis_title="Question Number",
        yaxis_title="Accuracy (%)",
        yaxis=dict(range=[0, 100]),
        height=400
    )
    
    trend_filename = f"{output_dir}/{model_name}_{timestamp}_accuracy_trend.html"
    fig_trend.write_html(trend_filename)
    
    # Print summary
    print(f"Visualizations saved to: {output_dir}/")
    print(f"Model: {data['config'].get('model', 'Unknown')}")
    print(f"Total Questions: {total_questions}")
    print(f"Correct: {correct_count}")
    print(f"Incorrect: {incorrect_count}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"\nFiles created:")
    print(f"  - {bar_filename}")
    print(f"  - {table_filename}")
    print(f"  - {results_filename}")
    print(f"  - {trend_filename}")
    
    return {
        'bar_chart': bar_filename,
        'summary': table_filename,
        'detailed_results': results_filename,
        'trend': trend_filename
    }


def main():
    parser = argparse.ArgumentParser(description='Create offline GPQA accuracy visualizations')
    parser.add_argument('--log_file', required=True, help='Path to the log file')
    parser.add_argument('--output_dir', default='visualizations', help='Output directory for visualizations')
    
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
    
    # Create visualizations
    create_accuracy_visualization(data, args.output_dir)


if __name__ == "__main__":
    main() 