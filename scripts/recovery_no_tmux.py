#!/usr/bin/env python3
"""
Recovery guide after connection closed without tmux
"""

print("="*80)
print("RECOVERY AFTER CONNECTION CLOSED (NO TMUX)")
print("="*80)

print("""
STEP 1: Reconnect to RunPod
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SSH back into your RunPod instance or use the web terminal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 2: Check if experiment is still running
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Check if Python process is still running:
  ps aux | grep "run_on_runpod.sh" | grep -v grep
  ps aux | grep "python.*main.py" | grep -v grep

If you see processes, experiment might still be running! ✅
If not, experiment stopped when connection closed ❌

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 3: Check what completed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Navigate to project:
  cd /workspace/kernel-divergence-sad

Check results file:
  cat out/stages_oversight_qwen2.5-0.5b/results.tsv

Count completed runs:
  wc -l out/stages_oversight_qwen2.5-0.5b/results.tsv

Check last completed contamination rate:
  tail -n 1 out/stages_oversight_qwen2.5-0.5b/results.tsv | grep -o 'contamination=[0-9.]*'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 4: Restart from where it stopped
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If experiment stopped, you have two options:

OPTION A: Restart from beginning (overwrites existing results)
  cd /workspace/kernel-divergence-sad
  eval "$(/root/miniconda3/bin/conda shell.bash hook)"
  conda activate kds
  bash scripts/run_on_runpod.sh qwen2.5-0.5b

OPTION B: Continue from specific contamination rate (manual)
  # Example: if last completed was 0.50, continue from 0.55:
  cd /workspace/kernel-divergence-sad
  eval "$(/root/miniconda3/bin/conda shell.bash hook)"
  conda activate kds
  
  # Run remaining contamination rates manually
  for r in 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1.00; do
    CONTAM=$r bash scripts/run_on_runpod.sh qwen2.5-0.5b
  done

OPTION C: Use nohup for background execution (survives disconnection)
  cd /workspace/kernel-divergence-sad
  eval "$(/root/miniconda3/bin/conda shell.bash hook)"
  conda activate kds
  
  nohup bash scripts/run_on_runpod.sh qwen2.5-0.5b > run_qwen2.5-0.5b.log 2>&1 &
  
  # Check if running
  ps aux | grep "run_on_runpod.sh" | grep -v grep
  
  # View logs
  tail -f run_qwen2.5-0.5b.log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 5: Recommended approach
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Check what completed: cat out/stages_oversight_qwen2.5-0.5b/results.tsv
2. If very few completed (< 5), restart from beginning
3. If many completed (> 10), continue manually from last rate
4. For future runs, use nohup or tmux to prevent disconnection issues

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUICK COMMANDS SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Check status
ps aux | grep python | grep main.py
cat out/stages_oversight_qwen2.5-0.5b/results.tsv

# Restart with nohup (recommended)
cd /workspace/kernel-divergence-sad
eval "$(/root/miniconda3/bin/conda shell.bash hook)"
conda activate kds
nohup bash scripts/run_on_runpod.sh qwen2.5-0.5b > run_qwen2.5-0.5b.log 2>&1 &

# Monitor
tail -f run_qwen2.5-0.5b.log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


