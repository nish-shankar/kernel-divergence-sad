#!/usr/bin/env bash
set -euo pipefail

# Configuration - can be overridden via command line arguments
# Usage: bash scripts/run_on_runpod.sh [model] [dataset] [target_num] [split]
# Default: qwen2.5-3b stages_oversight 600 train
MODEL="${1:-qwen2.5-3b}"
DATASET="${2:-stages_oversight}"
TARGET_NUM="${3:-600}"  # Set to match available samples: 37 seen + 563 unseen = 600 total
SPLIT="${4:-train}"

# Ensure we are at repo root
cd "$(dirname "$0")/.."

# Create out dir
mkdir -p out

# Enable fast HF transfers if available
export HF_HUB_ENABLE_HF_TRANSFER=1 || true
export TOKENIZERS_PARALLELISM=true
# PyTorch memory management to avoid fragmentation
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# Basic sanity checks
if [[ ! -f token ]]; then
  echo "ERROR: token file not found at ./token. Create it with your HF token on a single line." >&2
  exit 1
fi

OUT_DIR="out/${DATASET}_${MODEL}"
LOG_FILE="run_${MODEL//\//_}.log"

echo "Running experiment: model=${MODEL}, dataset=${DATASET}, target_num=${TARGET_NUM}, split=${SPLIT}"
echo "Logs: ${LOG_FILE}"

# Adjust batch sizes based on model size
if [[ "${MODEL}" == *"7b"* ]] || [[ "${MODEL}" == *"7B"* ]]; then
  BATCH_SIZE=2
  INFERENCE_BATCH_SIZE=8
elif [[ "${MODEL}" == *"3b"* ]] || [[ "${MODEL}" == *"3B"* ]]; then
  BATCH_SIZE=4
  INFERENCE_BATCH_SIZE=16
elif [[ "${MODEL}" == *"0.5b"* ]] || [[ "${MODEL}" == *"0.5B"* ]]; then
  BATCH_SIZE=8
  INFERENCE_BATCH_SIZE=8  # Reduced to 8 for limited VRAM (14GB free) - safer than 16
elif [[ "${MODEL}" == *"1.5b"* ]] || [[ "${MODEL}" == *"1.5B"* ]]; then
  BATCH_SIZE=4  # Reduced from 8 to 4 to avoid OOM
  INFERENCE_BATCH_SIZE=8
elif [[ "${MODEL}" == *"1b"* ]] || [[ "${MODEL}" == *"1B"* ]] || [[ "${MODEL}" == *"1.1b"* ]] || [[ "${MODEL}" == *"1.1B"* ]]; then
  BATCH_SIZE=4  # Similar to 1.5B model
  INFERENCE_BATCH_SIZE=8  # Reduced from 16 to 8 to avoid OOM during embedding extraction
elif [[ "${MODEL}" == *"0.27b"* ]] || [[ "${MODEL}" == *"0.27B"* ]] || [[ "${MODEL}" == *"270m"* ]] || [[ "${MODEL}" == *"270M"* ]]; then
  BATCH_SIZE=8  # Similar to 0.5B model
  INFERENCE_BATCH_SIZE=32  # Increased from 8 to 32 for faster embedding extraction (270M model is small)
elif [[ "${MODEL}" == *"gemma"* ]] || [[ "${MODEL}" == *"Gemma"* ]]; then
  # Default Gemma batch sizes (fallback for other Gemma sizes)
  BATCH_SIZE=4
  INFERENCE_BATCH_SIZE=8
else
  BATCH_SIZE=4
  INFERENCE_BATCH_SIZE=16
fi

# Run
# If CONTAM is provided in environment, run a single setting; otherwise sweep 0.00 -> 1.00 by 0.05
if [[ -n "${CONTAM:-}" ]]; then
  echo "Single run with contamination=${CONTAM}"
  python -u src/main.py \
    --model "${MODEL}" \
    --data "${DATASET}" \
    --split "${SPLIT}" \
    --target_num "${TARGET_NUM}" \
    --batch_size "${BATCH_SIZE}" \
    --inference_batch_size "${INFERENCE_BATCH_SIZE}" \
    --sgd \
    --contamination "${CONTAM}" \
    --out_dir "${OUT_DIR}" | tee -a "${LOG_FILE}"
else
  echo "Sweeping contamination from 0.00 to 1.00 (step 0.05)"
  for r in $(seq 0 0.05 1.0); do
    echo "==> contamination=${r}"
    python -u src/main.py \
      --model "${MODEL}" \
      --data "${DATASET}" \
      --split "${SPLIT}" \
      --target_num "${TARGET_NUM}" \
      --batch_size "${BATCH_SIZE}" \
      --inference_batch_size "${INFERENCE_BATCH_SIZE}" \
      --sgd \
      --contamination "${r}" \
      --out_dir "${OUT_DIR}" | tee -a "${LOG_FILE}"
  done
fi

# The pipeline writes to out/results.tsv flat; organize it under the per-run folder if present
mkdir -p "${OUT_DIR}"
if [[ -f out/results.tsv ]]; then
  mv -f out/results.tsv "${OUT_DIR}/results.tsv"
fi

# Scrub any HF token occurrences before sharing
if [[ -f "${OUT_DIR}/results.tsv" ]]; then
  sed -E "s/token='hf_[^']*'//g" -i "${OUT_DIR}/results.tsv" || true
  echo "Results: ${OUT_DIR}/results.tsv"
else
  echo "WARNING: results.tsv not found; check ${LOG_FILE} for details." >&2
fi

# Optional: copy to persistent workspace if available
if [[ -d /workspace ]]; then
  mkdir -p /workspace/artifacts
  if [[ -f "${OUT_DIR}/results.tsv" ]]; then
    cp "${OUT_DIR}/results.tsv" \
       "/workspace/artifacts/${DATASET}_${MODEL}_results.tsv"
    echo "Copied to: /workspace/artifacts/${DATASET}_${MODEL}_results.tsv"
  fi
fi

echo "Done."


