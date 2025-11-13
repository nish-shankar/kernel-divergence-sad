# Complete Workflow: Running Gemma-3 27B Experiment from Scratch

This guide walks you through setting up and running the Kernel Divergence Score (KDS) experiment for the Gemma-3 27B model on a RunPod H200 GPU.

**Note**: This workflow is identical to the Gemma-3 12B workflow, with only the model name changed.

---

## Prerequisites

1. **RunPod Account**: Sign up at https://www.runpod.io/
2. **HuggingFace Account**: Sign up at https://huggingface.co/
3. **HuggingFace Token**: Get your token from https://huggingface.co/settings/tokens
4. **Model Access**: Ensure you have access to `google/gemma-3-27b-it`:
   - Visit: https://huggingface.co/google/gemma-3-27b-it
   - Accept the terms if prompted
   - Verify your token has access

---

## Step 1: Create RunPod Instance

1. Go to https://www.runpod.io/console/pods
2. Click **"Deploy"** or **"Create Pod"**
3. Select:
   - **GPU**: NVIDIA H200 (or H100 if H200 unavailable)
   - **Template**: PyTorch 2.x or Ubuntu 22.04
   - **Container Disk**: At least 50GB (for model weights and dependencies)
   - **Volume**: Optional (for persistent storage)
4. Click **"Deploy"** and wait for the pod to start
5. Note the **SSH connection details** or use **Jupyter Notebook** interface

---

## Step 2: Connect to RunPod Instance

### Option A: SSH Connection
```bash
ssh root@<your-pod-ip> -p <ssh-port>
```

### Option B: Jupyter Notebook
- Click **"Connect"** → **"HTTP Service"** → **"Jupyter"**
- Open a terminal in Jupyter

---

## Step 3: Initial Setup

Once connected, run these commands:

```bash
# Update system packages
apt-get update && apt-get install -y git wget curl

# Install Miniconda (if not already installed)
if ! command -v conda &> /dev/null; then
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3
    rm Miniconda3-latest-Linux-x86_64.sh
fi

# Initialize conda
source /root/miniconda3/etc/profile.d/conda.sh
conda init bash
```

---

## Step 4: Clone Repository

```bash
# Navigate to workspace directory
cd /workspace

# Clone the repository
git clone https://github.com/nish-shankar/kernel-divergence-sad.git

# Navigate into the project
cd kernel-divergence-sad

# Verify you're on the latest main branch
git checkout main
git pull origin main
```

---

## Step 5: Setup Conda Environment

```bash
# Ensure you're in the project directory
cd /workspace/kernel-divergence-sad

# Accept conda terms of service (required for some channels)
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Create conda environment from environment.yml
# This will take 10-15 minutes
conda env create -f environment.yml

# Activate the environment
source /root/miniconda3/etc/profile.d/conda.sh
conda activate kds

# Verify installation
python --version  # Should show Python 3.9.18
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"
```

**Note**: If environment creation fails, check the error message. Common issues:
- Network timeouts: Retry the command
- Dependency conflicts: The environment.yml should handle these automatically
- Disk space: Ensure you have at least 20GB free

---

## Step 6: Configure HuggingFace Token

```bash
# Navigate to project root
cd /workspace/kernel-divergence-sad

# Create token file with your HuggingFace token
# Use the same token that was used for Gemma-3 12B
# The token file should already exist if you're reusing the same setup
# If not, create it:
echo "YOUR_HF_TOKEN_HERE" > token

# Verify token file was created
cat token
```

**Note**: If you're using the same RunPod instance or workspace, the token file from the Gemma-3 12B experiment should already exist and can be reused.

---

## Step 7: Verify Model Access

```bash
# Activate environment
source /root/miniconda3/etc/profile.d/conda.sh
conda activate kds

# Test loading Gemma-3 27B model config
python -c "
from transformers import AutoConfig
import sys
with open('token', 'r') as f:
    token = f.read().strip()
try:
    config = AutoConfig.from_pretrained('google/gemma-3-27b-it', token=token, trust_remote_code=True)
    print('SUCCESS: Model config loaded!')
    print(f'Model type: {config.model_type}')
except Exception as e:
    print(f'ERROR: {e}')
    print('Make sure you have accepted the model terms at: https://huggingface.co/google/gemma-3-27b-it')
    sys.exit(1)
"
```

If you get an access error:
1. Visit https://huggingface.co/google/gemma-3-27b-it
2. Click "Agree and access repository"
3. Retry the test above

---

## Step 8: Verify Dataset File

```bash
# Check if stages_oversight.csv exists
cd /workspace/kernel-divergence-sad

# Look for the CSV file in common locations
ls -lh stages_oversight.csv 2>/dev/null || \
ls -lh src/data/stages_oversight.csv 2>/dev/null || \
echo "Dataset file not found - it should be downloaded automatically on first run"
```

The dataset will be loaded automatically from `stages_oversight.csv` if present, or from `src/data/stages_oversight.csv`.

---

## Step 9: Run the Experiment

```bash
# Navigate to project root
cd /workspace/kernel-divergence-sad

# Activate conda environment
source /root/miniconda3/etc/profile.d/conda.sh
conda activate kds

# Verify GPU is available
nvidia-smi

# Run the experiment in the background
# This will sweep contamination rates from 0.00 to 1.00 in steps of 0.05 (21 total runs)
nohup bash scripts/run_on_runpod.sh gemma-3-27b-it stages_oversight 600 train > run_gemma-3-27b-it.log 2>&1 &

# Note the process ID (PID) for later reference
echo "Experiment started with PID: $!"
```

**Experiment Details** (same as Gemma-3 12B):
- **Model**: `gemma-3-27b-it` (changed from `gemma-3-12b-it`)
- **Dataset**: `stages_oversight` (600 samples: 37 seen + 563 unseen)
- **Batch Size**: `BATCH_SIZE=1`, `INFERENCE_BATCH_SIZE=4` (same as 12B)
- **Contamination Sweep**: 0.00 to 1.00 in steps of 0.05 (21 contamination rates)
- **Expected Duration**: ~6-8 hours on H200 GPU

---

## Step 10: Monitor Progress

### Check if Experiment is Running

```bash
# Check running processes
ps aux | grep -E "run_on_runpod|main.py" | grep gemma-3-27b-it | grep -v grep

# Check GPU usage
nvidia-smi

# View log file (real-time)
tail -f run_gemma-3-27b-it.log

# Or check latest entries
tail -n 50 run_gemma-3-27b-it.log
```

### Check Progress

```bash
# Count completed contamination rates (out of 21 total)
cat out/stages_oversight_gemma-3-27b-it/results.tsv 2>/dev/null | wc -l

# View latest results
tail -n 10 out/stages_oversight_gemma-3-27b-it/results.tsv 2>/dev/null

# List all result files
ls -lh out/stages_oversight_gemma-3-27b-it/ 2>/dev/null
```

### Quick Status Check (One Command)

```bash
cd /workspace/kernel-divergence-sad && \
source /root/miniconda3/etc/profile.d/conda.sh && \
conda activate kds && \
echo "=== Running Processes ===" && \
ps aux | grep -E "run_on_runpod|main.py" | grep -v grep && \
echo -e "\n=== GPU Usage ===" && \
nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv && \
echo -e "\n=== Latest Log ===" && \
tail -n 5 run_gemma-3-27b-it.log 2>/dev/null && \
echo -e "\n=== Completed Contamination Rates ===" && \
(cat out/stages_oversight_gemma-3-27b-it/results.tsv 2>/dev/null | wc -l || echo "0") && \
echo "out of 21 total"
```

---

## Step 11: Expected Output

### Log File Format

The log file (`run_gemma-3-27b-it.log`) will show:
```
Running experiment: model=gemma-3-27b-it, dataset=stages_oversight, target_num=600, split=train
Logs: run_gemma-3-27b-it.log
Sweeping contamination from 0.00 to 1.00 (step 0.05)
==> contamination=0.00
DEBUG: Loading dataset 'stages_oversight'
Loading stages_oversight data from: stages_oversight.csv
Loaded 600 samples
Seen samples: 37, Unseen samples: 563
INFO: Extracting Embeddings!
...
```

### Results File Format

The results file (`out/stages_oversight_gemma-3-27b-it/results.tsv`) will contain:
- One row per contamination rate
- Columns: contamination rate, KDS score, and other metrics
- 21 rows total (one for each contamination rate from 0.00 to 1.00)

---

## Step 12: Completion

When the experiment completes:

```bash
# Check final results
cat out/stages_oversight_gemma-3-27b-it/results.tsv

# Verify all 21 contamination rates completed
wc -l out/stages_oversight_gemma-3-27b-it/results.tsv

# Check log for any errors
tail -n 100 run_gemma-3-27b-it.log | grep -i error

# Download results (if using RunPod volume or SSH)
# Results are also automatically copied to /workspace/artifacts/ if available
ls -lh /workspace/artifacts/stages_oversight_gemma-3-27b-it_results.tsv 2>/dev/null
```

---

## Troubleshooting

### Issue: Out of Memory (OOM) Error

**Symptoms**: `torch.OutOfMemoryError: CUDA out of memory`

**Solutions**:
1. Check if other processes are using GPU:
   ```bash
   nvidia-smi
   # Kill other GPU processes if needed
   kill <PID>
   ```
2. Batch sizes are already conservative (1/4). If still OOM:
   - Reduce `INFERENCE_BATCH_SIZE` to 2 in `scripts/run_on_runpod.sh`
   - Restart the experiment

### Issue: Model Access Denied

**Symptoms**: `OSError: You are trying to access a gated repo`

**Solutions**:
1. Visit https://huggingface.co/google/gemma-3-27b-it
2. Click "Agree and access repository"
3. Verify token: `cat token`
4. Retry the experiment

### Issue: Experiment Stopped Unexpectedly

**Symptoms**: Process not running, log shows error

**Solutions**:
1. Check the end of the log:
   ```bash
   tail -n 100 run_gemma-3-27b-it.log
   ```
2. Fix the issue based on the error message
3. Restart the experiment (it will skip completed contamination rates if results exist)

### Issue: Conda Environment Creation Failed

**Symptoms**: `CondaEnvException: Pip failed`

**Solutions**:
1. Check disk space: `df -h`
2. Retry environment creation:
   ```bash
   conda env remove -n kds
   conda env create -f environment.yml
   ```
3. If specific package fails, try installing manually:
   ```bash
   conda activate kds
   pip install <package-name>
   ```

### Issue: Slow Download/Network Issues

**Symptoms**: Model download hangs or times out

**Solutions**:
1. Enable HF transfer (already in script):
   ```bash
   export HF_HUB_ENABLE_HF_TRANSFER=1
   ```
2. Use HuggingFace mirror (if available)
3. Pre-download model:
   ```bash
   python -c "
   from transformers import AutoModelForCausalLM
   with open('token', 'r') as f:
       token = f.read().strip()
   AutoModelForCausalLM.from_pretrained('google/gemma-3-27b-it', token=token, trust_remote_code=True)
   "
   ```

---

## Quick Reference Commands

```bash
# Navigate to project
cd /workspace/kernel-divergence-sad

# Activate environment
source /root/miniconda3/etc/profile.d/conda.sh && conda activate kds

# Start experiment
nohup bash scripts/run_on_runpod.sh gemma-3-27b-it stages_oversight 600 train > run_gemma-3-27b-it.log 2>&1 &

# Monitor progress
tail -f run_gemma-3-27b-it.log

# Check status
ps aux | grep main.py | grep gemma-3-27b-it

# View results
cat out/stages_oversight_gemma-3-27b-it/results.tsv

# Stop experiment (if needed)
pkill -f "gemma-3-27b-it"
```

---

## Summary

1. ✅ Create RunPod H200 instance
2. ✅ Connect via SSH or Jupyter
3. ✅ Install Miniconda
4. ✅ Clone repository
5. ✅ Create conda environment
6. ✅ Configure HuggingFace token
7. ✅ Verify model access
8. ✅ Run experiment
9. ✅ Monitor progress
10. ✅ Collect results

**Expected Timeline**:
- Setup: ~20-30 minutes
- Environment creation: ~10-15 minutes
- Experiment runtime: ~6-8 hours
- **Total**: ~7-9 hours

---

## Support

If you encounter issues not covered here:
1. Check the log file: `run_gemma-3-27b-it.log`
2. Check GitHub issues: https://github.com/nish-shankar/kernel-divergence-sad/issues
3. Verify all prerequisites are met
4. Ensure you have sufficient GPU memory (H200 recommended)

