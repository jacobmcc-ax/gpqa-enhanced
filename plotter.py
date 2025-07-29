#!/usr/bin/env python3
"""
Plotter for GPQA response time analysis
Creates visualizations similar to the time analysis plots shown in the reference image.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast
import argparse
import os
from pathlib import Path

def parse_list_string(list_str):
    """Parse a string representation of a list back to a list."""
    try:
        return ast.literal_eval(list_str)
    except:
        return []

def load_csv_data(csv_file):
    """Load and parse CSV data from the GPQA results file."""
    df = pd.read_csv(csv_file)
    
    # Parse the list columns
    correct_ids = parse_list_string(df['correct_question_ids'].iloc[0])
    incorrect_ids = parse_list_string(df['incorrect_question_ids'].iloc[0])
    response_times = parse_list_string(df['response_times'].iloc[0])
    
    # Get model name and prompt type if available
    model_name = df['model_name'].iloc[0] if 'model_name' in df.columns else 'Unknown Model'
    prompt_type = df['prompt_type'].iloc[0] if 'prompt_type' in df.columns else 'Unknown Prompt'
    
    # Create a DataFrame with individual question data
    question_data = []
    for i, time in enumerate(response_times):
        if i in correct_ids:
            correctness = 'Correct'
            is_correct = True
        elif i in incorrect_ids:
            correctness = 'Incorrect'
            is_correct = False
        else:
            correctness = 'Refused'
            is_correct = None  # Neither correct nor incorrect
        
        question_data.append({
            'question_id': i,
            'response_time': time,
            'is_correct': is_correct,
            'correctness': correctness
        })
    
    result_df = pd.DataFrame(question_data)
    result_df.attrs['model_name'] = model_name
    result_df.attrs['prompt_type'] = prompt_type
    
    return result_df

def create_time_analysis_plots(df, output_file=None, show_plot=True):
    """Create time analysis plots similar to the reference image."""
    
    # Get model name and prompt type from DataFrame attributes
    model_name = df.attrs.get('model_name', 'Unknown Model')
    prompt_type = df.attrs.get('prompt_type', 'Unknown Prompt')
    
    # Create a descriptive title
    plot_title = f"Response Time Analysis - {model_name} ({prompt_type})"
    
    # Set up the figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle(plot_title, fontsize=16, fontweight='bold')
    
    # Left plot: Distribution of Response Times (Histogram)
    ax1.hist(df['response_time'], bins=15, color='purple', alpha=0.7, edgecolor='black')
    ax1.axvline(df['response_time'].mean(), color='red', linestyle='--', 
                label=f'Mean: {df["response_time"].mean():.1f}s')
    ax1.set_xlabel('Response Time (seconds)')
    ax1.set_ylabel('Number of Problems')
    ax1.set_title('Distribution of Response Times')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Right plot: Response Time by Correctness (Scatter Plot)
    correct_data = df[df['correctness'] == 'Correct']
    incorrect_data = df[df['correctness'] == 'Incorrect']
    refused_data = df[df['correctness'] == 'Refused']
    
    correct_count = len(correct_data)
    incorrect_count = len(incorrect_data)
    refused_count = len(refused_data)
    
    ax2.scatter(correct_data['question_id'], correct_data['response_time'], 
                color='green', label=f'Correct ({correct_count})', alpha=0.7, s=50)
    ax2.scatter(incorrect_data['question_id'], incorrect_data['response_time'], 
                color='red', label=f'Incorrect ({incorrect_count})', alpha=0.7, s=50)
    ax2.scatter(refused_data['question_id'], refused_data['response_time'], 
                color='blue', label=f'Refused ({refused_count})', alpha=0.7, s=50)
    ax2.set_xlabel('Problem Number')
    ax2.set_ylabel('Response Time (seconds)')
    ax2.set_title('Response Time by Correctness')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Adjust layout and save/show
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {output_file}")
    
    if show_plot:
        plt.show()
    
    return fig

def create_additional_plots(df, output_dir=None, output_file=None, show_plots=True):
    """Create additional useful plots for analysis."""
    
    # Get model name and prompt type from DataFrame attributes
    model_name = df.attrs.get('model_name', 'Unknown Model')
    prompt_type = df.attrs.get('prompt_type', 'Unknown Prompt')
    
    # Create a descriptive title
    plot_title = f"Additional Analysis - {model_name} ({prompt_type})"
    
    # Create a new figure for additional plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(plot_title, fontsize=16, fontweight='bold')
    
    # Plot 1: Box plot of response times by correctness
    correct_times = df[df['correctness'] == 'Correct']['response_time']
    incorrect_times = df[df['correctness'] == 'Incorrect']['response_time']
    refused_times = df[df['correctness'] == 'Refused']['response_time']
    
    # Only include categories that have data
    plot_data = []
    plot_labels = []
    if len(correct_times) > 0:
        plot_data.append(correct_times)
        plot_labels.append('Correct')
    if len(incorrect_times) > 0:
        plot_data.append(incorrect_times)
        plot_labels.append('Incorrect')
    if len(refused_times) > 0:
        plot_data.append(refused_times)
        plot_labels.append('Refused')
    
    ax1.boxplot(plot_data, tick_labels=plot_labels)
    ax1.set_ylabel('Response Time (seconds)')
    ax1.set_title('Response Time Distribution by Correctness')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Cumulative distribution of response times
    sorted_times = np.sort(df['response_time'])
    cumulative = np.arange(1, len(sorted_times) + 1) / len(sorted_times)
    ax2.plot(sorted_times, cumulative, 'b-', linewidth=2)
    ax2.set_xlabel('Response Time (seconds)')
    ax2.set_ylabel('Cumulative Probability')
    ax2.set_title('Cumulative Distribution of Response Times')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Response time vs question number (line plot)
    ax3.plot(df['question_id'], df['response_time'], 'o-', alpha=0.7)
    ax3.set_xlabel('Question Number')
    ax3.set_ylabel('Response Time (seconds)')
    ax3.set_title('Response Time Trend')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Accuracy vs response time bins
    time_bins = pd.cut(df['response_time'], bins=5)
    # Calculate accuracy excluding refused questions
    df_answered = df[df['correctness'] != 'Refused']
    accuracy_by_bin = df_answered.groupby(time_bins)['is_correct'].mean()
    ax4.bar(range(len(accuracy_by_bin)), accuracy_by_bin.values, alpha=0.7)
    ax4.set_xlabel('Response Time Bins')
    ax4.set_ylabel('Accuracy')
    ax4.set_title('Accuracy by Response Time Bins')
    ax4.set_xticks(range(len(accuracy_by_bin)))
    ax4.set_xticklabels([f'{bin_.left:.1f}-{bin_.right:.1f}s' for bin_ in accuracy_by_bin.index], rotation=45)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Additional plots saved to: {output_file}")
    elif output_dir:
        additional_plot_file = os.path.join(output_dir, 'additional_analysis.png')
        plt.savefig(additional_plot_file, dpi=300, bbox_inches='tight')
        print(f"Additional plots saved to: {additional_plot_file}")
    
    if show_plots:
        plt.show()
    
    return fig

def generate_summary_stats(df):
    """Generate and print summary statistics."""
    print("\n" + "="*50)
    print("RESPONSE TIME ANALYSIS SUMMARY")
    print("="*50)
    
    print(f"Total Questions: {len(df)}")
    print(f"Correct Answers: {len(df[df['correctness'] == 'Correct'])}")
    print(f"Incorrect Answers: {len(df[df['correctness'] == 'Incorrect'])}")
    print(f"Refused Questions: {len(df[df['correctness'] == 'Refused'])}")
    
    # Calculate accuracy excluding refused questions
    answered_df = df[df['correctness'] != 'Refused']
    if len(answered_df) > 0:
        accuracy = answered_df['is_correct'].mean()
        print(f"Overall Accuracy (excluding refusals): {accuracy:.3f} ({accuracy*100:.1f}%)")
    else:
        print("Overall Accuracy: N/A (no answered questions)")
    
    print(f"\nResponse Time Statistics:")
    print(f"  Mean: {df['response_time'].mean():.2f} seconds")
    print(f"  Median: {df['response_time'].median():.2f} seconds")
    print(f"  Std Dev: {df['response_time'].std():.2f} seconds")
    print(f"  Min: {df['response_time'].min():.2f} seconds")
    print(f"  Max: {df['response_time'].max():.2f} seconds")
    
    # Correct vs Incorrect vs Refused analysis
    correct_times = df[df['correctness'] == 'Correct']['response_time']
    incorrect_times = df[df['correctness'] == 'Incorrect']['response_time']
    refused_times = df[df['correctness'] == 'Refused']['response_time']
    
    print(f"\nCorrect Answers:")
    print(f"  Count: {len(correct_times)}")
    if len(correct_times) > 0:
        print(f"  Mean Time: {correct_times.mean():.2f} seconds")
        print(f"  Median Time: {correct_times.median():.2f} seconds")
    else:
        print(f"  Mean Time: N/A")
        print(f"  Median Time: N/A")
    
    print(f"\nIncorrect Answers:")
    print(f"  Count: {len(incorrect_times)}")
    if len(incorrect_times) > 0:
        print(f"  Mean Time: {incorrect_times.mean():.2f} seconds")
        print(f"  Median Time: {incorrect_times.median():.2f} seconds")
    else:
        print(f"  Mean Time: N/A")
        print(f"  Median Time: N/A")
    
    print(f"\nRefused Questions:")
    print(f"  Count: {len(refused_times)}")
    if len(refused_times) > 0:
        print(f"  Mean Time: {refused_times.mean():.2f} seconds")
        print(f"  Median Time: {refused_times.median():.2f} seconds")
    else:
        print(f"  Mean Time: N/A")
        print(f"  Median Time: N/A")
    
    if len(correct_times) > 0 and len(incorrect_times) > 0:
        from scipy import stats
        t_stat, p_value = stats.ttest_ind(correct_times, incorrect_times)
        print(f"\nT-test (Correct vs Incorrect response times):")
        print(f"  T-statistic: {t_stat:.3f}")
        print(f"  P-value: {p_value:.3f}")
        print(f"  Significant difference: {'Yes' if p_value < 0.05 else 'No'}")

def main():
    parser = argparse.ArgumentParser(description='Create time analysis plots from GPQA CSV results')
    parser.add_argument('csv_file', help='Path to the CSV file with GPQA results')
    parser.add_argument('--output', '-o', help='Output file for the main plot (e.g., time_analysis.png)')
    parser.add_argument('--output-dir', '-d', help='Output directory for all plots (default: tmp_logs/plots/)')
    parser.add_argument('--no-show', action='store_true', help='Do not display plots (only save)')
    parser.add_argument('--additional', '-a', action='store_true', help='Create additional analysis plots')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.csv_file):
        print(f"Error: File {args.csv_file} not found!")
        return
    
    # Load data
    print(f"Loading data from: {args.csv_file}")
    df = load_csv_data(args.csv_file)
    print(f"Loaded {len(df)} questions")
    
    # Set default output directory
    if args.output_dir is None:
        args.output_dir = "tmp_logs/plots"
    
    # Create output directory if it doesn't exist
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        print(f"Plots will be saved to: {args.output_dir}")
    
    # Generate summary statistics
    generate_summary_stats(df)
    
    # Create main time analysis plots
    show_plot = not args.no_show
    
    # Set default output file if not specified
    if args.output is None and args.output_dir:
        csv_basename = os.path.splitext(os.path.basename(args.csv_file))[0]
        model_name = df.attrs.get('model_name', 'unknown_model')
        prompt_type = df.attrs.get('prompt_type', 'unknown_prompt')
        
        # Create a clean filename with model and prompt type
        model_clean = model_name.replace('-', '_').replace('.', '_')
        prompt_clean = prompt_type.replace('_', '')
        
        args.output = os.path.join(args.output_dir, f"{model_clean}_{prompt_clean}_time_analysis.png")
    
    create_time_analysis_plots(df, args.output, show_plot)
    
    # Create additional plots if requested
    if args.additional:
        csv_basename = os.path.splitext(os.path.basename(args.csv_file))[0]
        model_name = df.attrs.get('model_name', 'unknown_model')
        prompt_type = df.attrs.get('prompt_type', 'unknown_prompt')
        
        # Create a clean filename with model and prompt type
        model_clean = model_name.replace('-', '_').replace('.', '_')
        prompt_clean = prompt_type.replace('_', '')
        
        additional_plot_file = os.path.join(args.output_dir, f"{model_clean}_{prompt_clean}_additional_analysis.png")
        create_additional_plots(df, args.output_dir, additional_plot_file, show_plot)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main() 