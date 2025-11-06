#!/usr/bin/env python3
"""
Troubleshooting tmux session creation
"""

print("="*80)
print("TROUBLESHOOTING TMUX SESSION")
print("="*80)

print("""
ISSUE: tmux session not created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Check if tmux is installed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run this command:
  which tmux

If it shows nothing, install tmux:
  apt-get update
  apt-get install -y tmux

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 2: Simpler tmux command (without nested quotes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Instead of the complex command, use this simpler approach:

# Create a wrapper script
cat > /tmp/run_exp.sh << 'EOF'
#!/bin/bash
eval "$(/root/miniconda3/bin/conda shell.bash hook)"
cd /workspace/kernel-divergence-sad
conda activate kds
bash scripts/run_on_runpod.sh qwen2.5-0.5b
EOF

chmod +x /tmp/run_exp.sh

# Then run in tmux
tmux new -s qwen0.5b -d 'bash /tmp/run_exp.sh'

# Or use tmux send-keys
tmux new -s qwen0.5b -d
tmux send-keys -t qwen0.5b 'eval "$(/root/miniconda3/bin/conda shell.bash hook)"' Enter
tmux send-keys -t qwen0.5b 'cd /workspace/kernel-divergence-sad' Enter
tmux send-keys -t qwen0.5b 'conda activate kds' Enter
tmux send-keys -t qwen0.5b 'bash scripts/run_on_runpod.sh qwen2.5-0.5b' Enter

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 3: OR run directly without tmux (for testing)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If tmux is problematic, you can run directly (but keep terminal open):

bash scripts/run_on_runpod.sh qwen2.5-0.5b

⚠️  Warning: If connection closes, experiment will stop!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDED: Check tmux installation first
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run these commands in order:

1. Check if tmux exists:
   which tmux

2. If empty, install tmux:
   apt-get update
   apt-get install -y tmux

3. Verify installation:
   tmux -V

4. Then try creating session again with simpler method above

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

