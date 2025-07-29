#!/bin/bash

# Comprehensive Baseline Runner Script
# This script allows you to run multiple configurations of run_baseline.py

set -e  # Exit on any error

# Configuration arrays - modify these to customize your experiments
MODELS=(
    "claude-sonnet-4-20250514"
    "claude-3-5-sonnet-20241022"
    "claude-3-5-haiku-20241022"
    "gpt-4"
    "gpt-3.5-turbo-16k-0613"
)

PROMPT_TYPES=(
    "zero_shot"
    "chain_of_thought"
    "5_shot"
    "self_consistency"
    "zero_shot_chain_of_thought"
)

DATASETS=(
    "dataset/gpqa_main.csv"
    "dataset/gpqa_extended.csv"
    "dataset/gpqa_experts.csv"
    "dataset/gpqa_diamond.csv"
)

MAX_EXAMPLES_OPTIONS=(
    5
    10
    20
    40
    100
)

SEEDS=(
    0
    1
    2
    3
    4
)

# Default values
DEFAULT_MAX_EXAMPLES=40
DEFAULT_SEED=0
DEFAULT_VERBOSE=false
DEFAULT_OVERWRITE_CACHE=false
DEFAULT_SAVE_RESULTS=false
DEFAULT_SHOW_PLOT=false
DEFAULT_ADDITIONAL_PLOTS=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -m, --models MODEL1,MODEL2,...     Specify models to run (default: all)"
    echo "  -p, --prompt-types TYPE1,TYPE2,... Specify prompt types (default: all)"
    echo "  -d, --datasets DATASET1,DATASET2,... Specify datasets (default: all)"
    echo "  -e, --max-examples NUM1,NUM2,...   Specify max examples (default: $DEFAULT_MAX_EXAMPLES)"
    echo "  -s, --seeds SEED1,SEED2,...        Specify seeds (default: $DEFAULT_SEED)"
    echo "  -v, --verbose                      Enable verbose output"
    echo "  -o, --overwrite-cache              Overwrite cache"
    echo "  -r, --save-results                 Save simplified results to CSV"
    echo "  -p, --show-plot                    Generate plots after saving results"
    echo "  -a, --additional-plots             Include additional analysis plots"
    echo "  -c, --config FILE                  Load configuration from file"
    echo "  -h, --help                         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Run all configurations"
    echo "  $0 -m claude-sonnet-4-20250514       # Run only Claude Sonnet 4"
    echo "  $0 -p chain_of_thought,zero_shot     # Run only specific prompt types"
    echo "  $0 -e 5,10 -s 0,1                    # Run with specific examples and seeds"
    echo "  $0 -v -o                             # Run with verbose output and overwrite cache"
    echo "  $0 -r                                # Run with simplified results logging"
    echo "  $0 -r -p                            # Run with results logging and plot generation"
    echo "  $0 -r -p -a                         # Run with results, plots, and additional analysis"
}

# Function to parse comma-separated arguments
parse_list() {
    local input="$1"
    if [[ -z "$input" ]]; then
        return 1
    fi
    IFS=',' read -ra ARRAY <<< "$input"
    echo "${ARRAY[@]}"
}

# Function to validate model name
validate_model() {
    local model="$1"
    local valid_models=(
        "claude-2" "claude-3-5-sonnet-20241022" "claude-3-5-haiku-20241022" 
        "claude-3-opus-20240229" "claude-sonnet-4-20250514" "claude-opus-4-20250514"
        "text-ada-001" "text-babbage-001" "text-curie-001" "text-davinci-002" 
        "text-davinci-003" "gpt-3.5-turbo-16k-0613" "gpt-4" "gpt-4-1106-preview"
    )
    
    for valid_model in "${valid_models[@]}"; do
        if [[ "$model" == "$valid_model" ]]; then
            return 0
        fi
    done
    return 1
}

# Function to validate prompt type
validate_prompt_type() {
    local prompt_type="$1"
    local valid_types=(
        "zero_shot" "chain_of_thought" "5_shot" "self_consistency" 
        "zero_shot_chain_of_thought" "retrieval" "retrieval_content"
    )
    
    for valid_type in "${valid_types[@]}"; do
        if [[ "$prompt_type" == "$valid_type" ]]; then
            return 0
        fi
    done
    return 1
}

# Function to run a single experiment
run_experiment() {
    local model="$1"
    local prompt_type="$2"
    local dataset="$3"
    local max_examples="$4"
    local seed="$5"
    local verbose="$6"
    local overwrite_cache="$7"
    local save_results="$8"
    local show_plot="$9"
    local additional_plots="${10}"
    
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local experiment_name="${model}_${prompt_type}_${max_examples}ex_seed${seed}_${timestamp}"
    
    print_info "Starting experiment: $experiment_name"
    print_info "Model: $model"
    print_info "Prompt Type: $prompt_type"
    print_info "Dataset: $dataset"
    print_info "Max Examples: $max_examples"
    print_info "Seed: $seed"
    
    # Build command
    local cmd="python baselines/run_baseline.py main"
    cmd="$cmd --model_name $model"
    cmd="$cmd --data_filename $dataset"
    cmd="$cmd --prompt_type $prompt_type"
    cmd="$cmd --max_examples $max_examples"
    cmd="$cmd --seed $seed"
    
    if [[ "$verbose" == "true" ]]; then
        cmd="$cmd --verbose"
    fi
    
    if [[ "$overwrite_cache" == "true" ]]; then
        cmd="$cmd --overwrite_cache"
    fi
    
    if [[ "$save_results" == "true" ]]; then
        cmd="$cmd --save_results"
    fi
    
    if [[ "$show_plot" == "true" ]]; then
        cmd="$cmd --show_plot"
    fi
    
    if [[ "$additional_plots" == "true" ]]; then
        cmd="$cmd --additional_plots"
    fi
    
    # Run the command
    print_info "Executing: $cmd"
    
    # Create log directory if it doesn't exist (only for save_results mode)
    if [[ "$save_results" == "true" ]]; then
        mkdir -p tmp_logs
        local log_file="tmp_logs/${experiment_name}.log"
    else
        # No log file when save_results is false
        local log_file="/dev/null"
    fi
    local start_time=$(date +%s)
    
    if timeout 3600 bash -c "$cmd" > "$log_file" 2>&1; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        print_success "Experiment completed successfully in ${duration}s: $experiment_name"
        print_success "Log saved to: $log_file"
    else
        local exit_code=$?
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        if [[ $exit_code -eq 124 ]]; then
            print_error "Experiment timed out after ${duration}s: $experiment_name"
        else
            print_error "Experiment failed with exit code $exit_code after ${duration}s: $experiment_name"
        fi
        print_error "Check log file: $log_file"
    fi
    
    echo "----------------------------------------"
}

# Function to load configuration from file
load_config() {
    local config_file="$1"
    if [[ ! -f "$config_file" ]]; then
        print_error "Configuration file not found: $config_file"
        exit 1
    fi
    
    print_info "Loading configuration from: $config_file"
    source "$config_file"
}

# Parse command line arguments
VERBOSE="$DEFAULT_VERBOSE"
OVERWRITE_CACHE="$DEFAULT_OVERWRITE_CACHE"
SAVE_RESULTS="$DEFAULT_SAVE_RESULTS"
SHOW_PLOT="$DEFAULT_SHOW_PLOT"
ADDITIONAL_PLOTS="$DEFAULT_ADDITIONAL_PLOTS"
CUSTOM_MODELS=""
CUSTOM_PROMPT_TYPES=""
CUSTOM_DATASETS=""
CUSTOM_MAX_EXAMPLES=""
CUSTOM_SEEDS=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--models)
            CUSTOM_MODELS="$2"
            shift 2
            ;;
        -p|--prompt-types)
            CUSTOM_PROMPT_TYPES="$2"
            shift 2
            ;;
        -d|--datasets)
            CUSTOM_DATASETS="$2"
            shift 2
            ;;
        -e|--max-examples)
            CUSTOM_MAX_EXAMPLES="$2"
            shift 2
            ;;
        -s|--seeds)
            CUSTOM_SEEDS="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="true"
            shift
            ;;
        -o|--overwrite-cache)
            OVERWRITE_CACHE="true"
            shift
            ;;
        -r|--save-results)
            SAVE_RESULTS="true"
            shift
            ;;
        -p|--show-plot)
            SHOW_PLOT="true"
            shift
            ;;
        -a|--additional-plots)
            ADDITIONAL_PLOTS="true"
            shift
            ;;
        -c|--config)
            load_config "$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Set arrays based on custom values or defaults
if [[ -n "$CUSTOM_MODELS" ]]; then
    MODELS=($(parse_list "$CUSTOM_MODELS"))
fi

if [[ -n "$CUSTOM_PROMPT_TYPES" ]]; then
    PROMPT_TYPES=($(parse_list "$CUSTOM_PROMPT_TYPES"))
fi

if [[ -n "$CUSTOM_DATASETS" ]]; then
    DATASETS=($(parse_list "$CUSTOM_DATASETS"))
fi

if [[ -n "$CUSTOM_MAX_EXAMPLES" ]]; then
    MAX_EXAMPLES_OPTIONS=($(parse_list "$CUSTOM_MAX_EXAMPLES"))
fi

if [[ -n "$CUSTOM_SEEDS" ]]; then
    SEEDS=($(parse_list "$CUSTOM_SEEDS"))
fi

# Validate configurations
print_info "Validating configurations..."

for model in "${MODELS[@]}"; do
    if ! validate_model "$model"; then
        print_error "Invalid model: $model"
        exit 1
    fi
done

for prompt_type in "${PROMPT_TYPES[@]}"; do
    if ! validate_prompt_type "$prompt_type"; then
        print_error "Invalid prompt type: $prompt_type"
        exit 1
    fi
done

for dataset in "${DATASETS[@]}"; do
    if [[ ! -f "$dataset" ]]; then
        print_error "Dataset file not found: $dataset"
        exit 1
    fi
done

# Print configuration summary
print_info "Configuration Summary:"
print_info "Models: ${MODELS[*]}"
print_info "Prompt Types: ${PROMPT_TYPES[*]}"
print_info "Datasets: ${DATASETS[*]}"
print_info "Max Examples: ${MAX_EXAMPLES_OPTIONS[*]}"
        print_info "Seeds: ${SEEDS[*]}"
        print_info "Verbose: $VERBOSE"
        print_info "Overwrite Cache: $OVERWRITE_CACHE"
        print_info "Save Results: $SAVE_RESULTS"
        print_info "Show Plot: $SHOW_PLOT"
        print_info "Additional Plots: $ADDITIONAL_PLOTS"

# Calculate total number of experiments
total_experiments=$((${#MODELS[@]} * ${#PROMPT_TYPES[@]} * ${#DATASETS[@]} * ${#MAX_EXAMPLES_OPTIONS[@]} * ${#SEEDS[@]}))
print_info "Total experiments to run: $total_experiments"

# Ask for confirmation if running many experiments
if [[ $total_experiments -gt 50 ]]; then
    print_warning "You are about to run $total_experiments experiments. This may take a very long time and cost significant API credits."
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Aborted by user"
        exit 0
    fi
fi

# Create results summary file
summary_file="logs/experiment_summary_$(date +"%Y%m%d_%H%M%S").txt"
echo "Experiment Summary - $(date)" > "$summary_file"
echo "========================================" >> "$summary_file"
echo "Total experiments: $total_experiments" >> "$summary_file"
echo "Configuration:" >> "$summary_file"
echo "  Models: ${MODELS[*]}" >> "$summary_file"
echo "  Prompt Types: ${PROMPT_TYPES[*]}" >> "$summary_file"
echo "  Datasets: ${DATASETS[*]}" >> "$summary_file"
echo "  Max Examples: ${MAX_EXAMPLES_OPTIONS[*]}" >> "$summary_file"
        echo "  Seeds: ${SEEDS[*]}" >> "$summary_file"
        echo "  Verbose: $VERBOSE" >> "$summary_file"
        echo "  Overwrite Cache: $OVERWRITE_CACHE" >> "$summary_file"
        echo "  Save Results: $SAVE_RESULTS" >> "$summary_file"
        echo "  Show Plot: $SHOW_PLOT" >> "$summary_file"
        echo "  Additional Plots: $ADDITIONAL_PLOTS" >> "$summary_file"
echo "" >> "$summary_file"
echo "Results:" >> "$summary_file"
echo "========================================" >> "$summary_file"

# Run experiments
experiment_count=0
start_time=$(date +%s)

for model in "${MODELS[@]}"; do
    for prompt_type in "${PROMPT_TYPES[@]}"; do
        for dataset in "${DATASETS[@]}"; do
            for max_examples in "${MAX_EXAMPLES_OPTIONS[@]}"; do
                for seed in "${SEEDS[@]}"; do
                    experiment_count=$((experiment_count + 1))
                    print_info "Progress: $experiment_count/$total_experiments"
                    
                    run_experiment "$model" "$prompt_type" "$dataset" "$max_examples" "$seed" "$VERBOSE" "$OVERWRITE_CACHE" "$SAVE_RESULTS" "$SHOW_PLOT" "$ADDITIONAL_PLOTS"
                    
                    # Add a small delay to avoid overwhelming the API
                    sleep 2
                done
            done
        done
    done
done

# Final summary
end_time=$(date +%s)
total_duration=$((end_time - start_time))
print_success "All experiments completed!"
print_success "Total time: ${total_duration}s ($(($total_duration / 60)) minutes)"
print_success "Summary saved to: $summary_file"

# Generate a simple results summary
print_info "Generating results summary..."
echo "" >> "$summary_file"
echo "Execution Summary:" >> "$summary_file"
echo "  Total time: ${total_duration}s ($(($total_duration / 60)) minutes)" >> "$summary_file"
echo "  Experiments completed: $experiment_count" >> "$summary_file"
echo "  Completion time: $(date)" >> "$summary_file"

print_success "Done!" 