#!/usr/bin/env bash
# Wrapper script to run experiments in tmux for persistence
# Usage: bash scripts/run_in_tmux.sh [model] [dataset] [target_num] [split]

MODEL="${1:-qwen2.5-7b}"
DATASET="${2:-stages_oversight}"
TARGET_NUM="${3:-2000}"
SPLIT="${4:-train}"

SESSION_NAME="kds_${MODEL}_${DATASET}"

# Check if session already exists
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "Session '$SESSION_NAME' already exists. Attaching..."
  tmux attach -t "$SESSION_NAME"
else
  echo "Creating new tmux session '$SESSION_NAME'..."
  # Get project root directory
  PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
  LOG_FILE="${PROJECT_ROOT}/run_${MODEL//\//_}.log"
  
  # Create new session and run the experiment
  tmux new-session -d -s "$SESSION_NAME" -c "$PROJECT_ROOT" \
    "bash scripts/run_on_runpod.sh '$MODEL' '$DATASET' '$TARGET_NUM' '$SPLIT' 2>&1 | tee -a '$LOG_FILE'; \
     echo ''; \
     echo 'Experiment finished. Press any key to exit...'; \
     read"
  
  echo "Session started. Attaching..."
  sleep 1
  tmux attach -t "$SESSION_NAME"
fi

