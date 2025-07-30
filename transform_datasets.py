#!/usr/bin/env python3
"""
Script to transform GPQA CSV datasets into a simplified format.

Takes GPQA dataset files from /dataset and creates new files in /questions with:
- Column 1: Scientific question
- Column 2: Four answer choices (A), (B), (C), (D) 
- Column 3: Correct answer choice (A, B, C, or D)
- Column 4: Question domain
"""

import pandas as pd
import os
import sys
from pathlib import Path

def transform_dataset(input_file: str, output_file: str):
    """Transform a single GPQA dataset file to the simplified format."""
    
    # Read the CSV file
    try:
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} questions from {input_file}")
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        return False
    
    # Extract required columns
    required_columns = ['Question', 'Correct Answer', 'Incorrect Answer 1', 
                       'Incorrect Answer 2', 'Incorrect Answer 3', 'High-level domain']
    
    # Check if all required columns exist
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Skipping {input_file}: Not a question dataset (missing question columns)")
        return False
    
    # Create new dataframe with transformed data
    transformed_data = []
    
    for _, row in df.iterrows():
        question = str(row['Question']).strip()
        correct_answer = str(row['Correct Answer']).strip()
        incorrect_1 = str(row['Incorrect Answer 1']).strip()
        incorrect_2 = str(row['Incorrect Answer 2']).strip()
        incorrect_3 = str(row['Incorrect Answer 3']).strip()
        domain = str(row['High-level domain']).strip()
        
        # Skip rows with missing data
        if any(pd.isna(val) or val == 'nan' for val in [question, correct_answer, incorrect_1, incorrect_2, incorrect_3, domain]):
            continue
        
        # Create the four choices as formatted string (using | as separator to avoid CSV issues)
        choices = f"(A) {correct_answer} | (B) {incorrect_1} | (C) {incorrect_2} | (D) {incorrect_3}"
        
        # Correct answer is always A since we put correct answer first
        correct_choice = "A"
        
        transformed_data.append({
            'Question': question,
            'Answer_Choices': choices,
            'Correct_Answer': correct_choice,
            'Domain': domain
        })
    
    # Create output dataframe
    output_df = pd.DataFrame(transformed_data)
    
    # Save to CSV with proper quoting
    try:
        output_df.to_csv(output_file, index=False, quoting=1)  # QUOTE_ALL
        print(f"Saved {len(output_df)} transformed questions to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving {output_file}: {e}")
        return False

def main():
    """Main function to process all dataset files."""
    
    # Define paths
    script_dir = Path(__file__).parent
    dataset_dir = script_dir / "dataset"
    questions_dir = script_dir / "questions"
    
    # Create questions directory if it doesn't exist
    questions_dir.mkdir(exist_ok=True)
    print(f"Created/verified questions directory: {questions_dir}")
    
    # Find all CSV files in dataset directory
    if not dataset_dir.exists():
        print(f"Error: Dataset directory {dataset_dir} does not exist!")
        sys.exit(1)
    
    csv_files = list(dataset_dir.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {dataset_dir}")
        sys.exit(1)
    
    print(f"Found {len(csv_files)} CSV files to process:")
    for file in csv_files:
        print(f"  - {file.name}")
    
    # Process each CSV file
    success_count = 0
    for csv_file in csv_files:
        output_file = questions_dir / f"transformed_{csv_file.name}"
        print(f"\nProcessing {csv_file.name}...")
        
        if transform_dataset(str(csv_file), str(output_file)):
            success_count += 1
        else:
            print(f"Failed to process {csv_file.name}")
    
    print(f"\n=== Summary ===")
    print(f"Successfully processed {success_count}/{len(csv_files)} files")
    print(f"Output files saved in: {questions_dir}")
    
    # Show sample of first transformed file
    if success_count > 0:
        first_output = questions_dir / f"transformed_{csv_files[0].name}"
        if first_output.exists():
            print(f"\nSample from {first_output.name}:")
            sample_df = pd.read_csv(first_output)
            if len(sample_df) > 0:
                print("First question:")
                print(f"Question: {sample_df.iloc[0]['Question'][:100]}...")
                print(f"Choices:\n{sample_df.iloc[0]['Answer_Choices']}")
                print(f"Correct: {sample_df.iloc[0]['Correct_Answer']}")
                print(f"Domain: {sample_df.iloc[0]['Domain']}")

if __name__ == "__main__":
    main()