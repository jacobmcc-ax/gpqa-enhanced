#!/usr/bin/env python3
"""
Test script to demonstrate the plotter functionality
"""

import pandas as pd
import os

def create_test_csv():
    """Create a test CSV file with sample response time data."""
    
    # Create sample data
    test_data = {
        'num_questions_asked': [10],
        'num_questions_correct': [7],
        'num_questions_incorrect': [3],
        'num_questions_not_answered': [0],
        'correct_question_ids': ['[0, 1, 3, 4, 6, 8, 9]'],
        'incorrect_question_ids': ['[2, 5, 7]'],
        'response_times': ['[25.3, 28.7, 45.2, 32.1, 29.8, 67.4, 38.9, 41.2, 33.5, 35.7]']
    }
    
    df = pd.DataFrame(test_data)
    
    # Create tmp_logs directory if it doesn't exist
    os.makedirs('tmp_logs', exist_ok=True)
    
    # Save test CSV
    test_csv_path = 'tmp_logs/test_response_times.csv'
    df.to_csv(test_csv_path, index=False)
    print(f"Test CSV created: {test_csv_path}")
    
    return test_csv_path

if __name__ == "__main__":
    # Create test data
    test_csv = create_test_csv()
    
    print("\nTo test the plotter, run:")
    print(f"python plotter.py {test_csv}")
    print(f"python plotter.py {test_csv} --additional")
    print(f"python plotter.py {test_csv} --no-show") 