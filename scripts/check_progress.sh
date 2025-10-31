#!/usr/bin/env bash
# Quick script to check experiment progress

echo "=== Checking Running Processes ==="
ps aux | grep -E "python.*main.py|bash.*run_on_runpod" | grep -v grep || echo "No experiment processes found"

echo ""
echo "=== GPU Usage ==="
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader 2>/dev/null || echo "nvidia-smi not available"

echo ""
echo "=== Checking Log Files ==="
LOG_FILE="run_qwen2.5-7b.log"
if [[ -f "$LOG_FILE" ]]; then
  echo "Found log: $LOG_FILE"
  echo "Last 20 lines:"
  tail -20 "$LOG_FILE"
else
  echo "No log file found: $LOG_FILE"
fi

echo ""
echo "=== Checking Results ==="
OUT_DIR="out/stages_oversight_qwen2.5-7b"
if [[ -d "$OUT_DIR" ]]; then
  echo "Found output directory: $OUT_DIR"
  if [[ -f "$OUT_DIR/results.tsv" ]]; then
    echo "Results file exists. Last few lines:"
    tail -5 "$OUT_DIR/results.tsv"
  else
    echo "No results.tsv found yet"
  fi
else
  echo "No output directory found: $OUT_DIR"
fi

echo ""
echo "=== Checking Workspace Artifacts ==="
if [[ -d /workspace/artifacts ]]; then
  ls -lh /workspace/artifacts/*.tsv 2>/dev/null || echo "No artifacts found"
fi

