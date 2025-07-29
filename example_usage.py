#!/usr/bin/env python3
"""
Example usage of the GPQA accuracy visualization script.

This script demonstrates how to use the visualize_accuracy.py script
to create Weights & Biases visualizations from GPQA log files.
"""

import subprocess
import sys
from pathlib import Path


def main():
    # Example log file path (update this to your actual log file)
    log_file = "logs/claude-3-5-sonnet-20241022_9_total_questions_seed=2.log"
    
    # Check if log file exists
    if not Path(log_file).exists():
        print(f"Log file not found: {log_file}")
        print("Please update the log_file path in this script to point to your actual log file.")
        return
    
    # Command to run the visualization script
    cmd = [
        sys.executable, "visualize_accuracy.py",
        "--log_file", log_file,
        "--project_name", "GPQA Accuracy Analysis"
        # Note: No need to specify --wandb_entity, it will use your logged-in user
    ]
    
    print("Running visualization script...")
    print(f"Command: {' '.join(cmd)}")
    print("\nNote: Make sure you have:")
    print("1. Installed the required packages: pip install -r requirements_visualization.txt")
    print("2. Logged into Weights & Biases: wandb login")
    print("3. The script will automatically use your logged-in W&B account")
    print("\n" + "="*50)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
    except Exception as e:
        print(f"Error running script: {e}")


if __name__ == "__main__":
    main() 