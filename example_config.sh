# Example configuration file for run_baseline_comprehensive.sh
# Copy this file and modify the arrays below to customize your experiments

# Models to test
MODELS=(
    "claude-sonnet-4-20250514"
    "claude-3-5-sonnet-20241022"
)

# Prompt types to test
PROMPT_TYPES=(
    "zero_shot"
    "chain_of_thought"
    "5_shot"
)

# Datasets to use
DATASETS=(
    "dataset/gpqa_main.csv"
    "dataset/gpqa_extended.csv"
)

# Number of examples to test
MAX_EXAMPLES_OPTIONS=(
    5
    10
    20
)

# Random seeds to use
SEEDS=(
    0
    1
    2
)

# This configuration will run:
# 2 models × 3 prompt types × 2 datasets × 3 max examples × 3 seeds = 108 experiments 