import pandas as pd
import random

# Load the dataset
df = pd.read_csv('dataset/gpqa_diamond.csv')

# Select a random question (seed for reproducibility)
random.seed(42)
question_idx = random.randint(0, len(df) - 1)
row = df.iloc[question_idx]

# Extract question and answer choices (without revealing correct answer)
question_text = row['Question']
choices = [
    row['Correct Answer'],
    row['Incorrect Answer 1'], 
    row['Incorrect Answer 2'],
    row['Incorrect Answer 3']
]

# Shuffle choices to hide which is correct
random.shuffle(choices)

print("=== SELECTED GPQA QUESTION ===")
print(f"Question: {question_text}")
print("\nAnswer Choices:")
for i, choice in enumerate(choices, 1):
    print(f"({chr(64+i)}) {choice}")

print(f"\n=== FOR LATER VERIFICATION ===")
print(f"Correct Answer: {row['Correct Answer']}")
print(f"Explanation: {row['Explanation']}")
print(f"Domain: {row['High-level domain']}")
print(f"Subdomain: {row['Subdomain']}")