#!/usr/bin/env python3
"""
Recovery guide for reconnecting after connection closed
"""

print("="*80)
print("RECONNECTING AFTER CONNECTION CLOSED")
print("="*80)

print("""
STEP 1: Reconnect to your server/RunPod instance
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SSH back into your RunPod instance:
  ssh root@<your-runpod-ip>
  # OR use RunPod's web terminal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 2: Check if tmux session is still running
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

List all tmux sessions:
  tmux ls

Expected output if session exists:
  qwen0.5b: 1 windows (created ...)
  # OR
  qwen3b: 1 windows (created ...)
  # OR
  qwen7b: 1 windows (created ...)

If you see your session name, it's still running! ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 3: Reattach to tmux session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For Qwen 2.5 0.5B:
  tmux attach -t qwen0.5b

For Qwen 2.5 3B:
  tmux attach -t qwen3b

For Qwen 2.5 7B:
  tmux attach -t qwen7b

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 4: Check progress without attaching
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Check if experiment is still running:
  ps aux | grep "python.*main.py" | grep -v grep

View logs:
  tail -f run_qwen2.5-0.5b.log
  # OR
  tail -f run_qwen2.5-3b.log
  # OR  
  tail -f run_qwen2.5-7b.log

Check results:
  cat out/stages_oversight_qwen2.5-0.5b/results.tsv
  # Count completed runs:
  wc -l out/stages_oversight_qwen2.5-0.5b/results.tsv

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 5: If session is NOT found (experiment stopped)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If tmux ls shows nothing, the experiment may have stopped.

Check the log file for errors:
  tail -n 100 run_qwen2.5-0.5b.log

Check the last completed contamination rate:
  tail -n 1 out/stages_oversight_qwen2.5-0.5b/results.tsv

If you need to continue from where it stopped:
  1. Check which contamination rates completed
  2. Run remaining rates manually:
     CONTAM=0.50 bash scripts/run_on_runpod.sh qwen2.5-0.5b

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUICK COMMANDS SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Check sessions
tmux ls

# Reattach (replace qwen0.5b with your session name)
tmux attach -t qwen0.5b

# View logs
tail -f run_qwen2.5-0.5b.log

# Check results
cat out/stages_oversight_qwen2.5-0.5b/results.tsv

# Detach from tmux (when inside)
Ctrl+B, then D

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

