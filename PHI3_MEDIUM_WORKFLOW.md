# Complete Workflow: Phi-3-medium-4k-instruct Experiment Setup

This guide walks you through setting up and running the Kernel Divergence Score (KDS) experiment for the Phi-3-medium-4k-instruct model on a RunPod H200 GPU.

---

## Step-by-Step Complete Setup

### Step 1: Connect to RunPod H200 GPU

1. Go to https://www.runpod.io/console/pods
2. Deploy an H200 GPU pod (or use existing pod)
3. Connect via SSH or Jupyter Notebook

---

### Step 2: Install System Dependencies

```bash
# Update package list
apt-get update

# Install basic tools
apt-get install -y git wget curl
```

---

### Step 3: Install Miniconda

```bash
# Download Miniconda installer
cd /tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install Miniconda (silent mode, to /root/miniconda3)
bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3

# Initialize conda
source /root/miniconda3/etc/profile.d/conda.sh

# Verify installation
conda --version

# Clean up installer
rm Miniconda3-latest-Linux-x86_64.sh
```

**Expected output**: `conda 23.x.x` or similar version number

---

### Step 4: Clone Repository

```bash
# Navigate to workspace
cd /workspace

# Clone the repository
git clone https://github.com/nish-shankar/kernel-divergence-sad.git

# Navigate into project
cd kernel-divergence-sad

# Pull latest changes (to get Phi-3-medium-4k-instruct support)
git pull origin main

# Verify you're in the right directory
pwd
# Should show: /workspace/kernel-divergence-sad
```

---

### Step 5: Accept Conda Terms of Service

```bash
# Accept terms for conda channels (required)
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

---

### Step 6: Create Conda Environment

```bash
# Ensure you're in the project directory
cd /workspace/kernel-divergence-sad

# Create conda environment from environment.yml
# This will take 10-15 minutes - be patient!
conda env create -f environment.yml

# Wait for completion - you'll see "done" when finished
```

**What this does**:
- Creates a conda environment named `kds`
- Installs Python 3.9.18
- Installs all required packages including:
  - PyTorch >= 2.2.0
  - Transformers >= 4.50.0
  - Bitsandbytes >= 0.43.0
  - And all other dependencies

**If you see errors**:
- Check disk space: `df -h` (need at least 20GB free)
- Check internet connection
- Retry the command

---

### Step 7: Activate Conda Environment

```bash
# Source conda initialization
source /root/miniconda3/etc/profile.d/conda.sh

# Activate the kds environment
conda activate kds

# Verify activation (should show (kds) prefix)
which python
# Should show: /root/miniconda3/envs/kds/bin/python

# Verify Python version
python --version
# Should show: Python 3.9.18
```

---

### Step 8: Verify Key Packages

```bash
# Ensure environment is activated
source /root/miniconda3/etc/profile.d/conda.sh
conda activate kds

# Check PyTorch
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
# Should show: PyTorch: 2.2.0 or higher

# Check Transformers
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"
# Should show: Transformers: 4.50.0 or higher

# Check CUDA availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
# Should show: CUDA available: True
```

---

### Step 9: Install hf_transfer (Optional but Recommended)

```bash
# Install hf_transfer for faster model downloads
pip install hf_transfer
```

---

### Step 10: Setup HuggingFace Token

```bash
# Navigate to project root
cd /workspace/kernel-divergence-sad

# Create token file with your HuggingFace token
# Replace YOUR_HF_TOKEN_HERE with your actual token
echo "YOUR_HF_TOKEN_HERE" > token

# Verify token file
cat token
```

**Important Notes**:
- The token file should contain ONLY the token string (no quotes, no extra characters)
- Get your token from: https://huggingface.co/settings/tokens
- Keep your token secure - never commit it to git

---

### Step 11: Verify Model Access

```bash
# Ensure environment is activated
source /root/miniconda3/etc/profile.d/conda.sh
conda activate kds

# Navigate to project root
cd /workspace/kernel-divergence-sad

# Test loading Phi-3-medium-4k-instruct model config
python -c "
from transformers import AutoConfig
import sys
with open('token', 'r') as f:
    token = f.read().strip()
try:
    config = AutoConfig.from_pretrained('microsoft/Phi-3-medium-4k-instruct', token=token, trust_remote_code=True)
    print('SUCCESS: Model config loaded!')
    print(f'Model type: {config.model_type}')
except Exception as e:
    print(f'ERROR: {e}')
    print('Make sure you have accepted the model terms at: https://huggingface.co/microsoft/Phi-3-medium-4k-instruct')
    sys.exit(1)
"
```

**If you get an access error**:
1. Visit https://huggingface.co/microsoft/Phi-3-medium-4k-instruct
2. Click "Agree and access repository"
3. Wait a few minutes for access to propagate
4. Retry the test above

---

### Step 12: Verify GPU Availability

```bash
# Check GPU
nvidia-smi

# Should show H200 GPU with available memory
# Example output:
# | NVIDIA H200 | ... | 0MiB / 143771MiB | ... |
```

---

### Step 13: Verify Dataset File

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

### Step 14: Run the Experiment

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
nohup bash scripts/run_on_runpod.sh phi-3-medium-4k-instruct stages_oversight 600 train > run_phi-3-medium-4k-instruct.log 2>&1 &

# Note the process ID
echo "Experiment started with PID: $!"
```

**Experiment Configuration**:
- **Model**: `phi-3-medium-4k-instruct` (14B parameters)
- **Dataset**: `stages_oversight` (600 samples: 37 seen + 563 unseen)
- **Batch Size**: `BATCH_SIZE=1`, `INFERENCE_BATCH_SIZE=4` (conservative for 14B model)
- **Contamination Sweep**: 0.00 to 1.00 in steps of 0.05 (21 contamination rates)
- **Expected Duration**: ~6-8 hours on H200 GPU

---

### Step 15: Monitor Progress

#### Check if Experiment is Running

```bash
# Check running processes
ps aux | grep -E "run_on_runpod|main.py" | grep phi-3-medium-4k-instruct | grep -v grep

# Check GPU usage
nvidia-smi

# View log file (real-time)
tail -f run_phi-3-medium-4k-instruct.log

# Press Ctrl+C to exit tail -f
```

#### Check Progress

```bash
# Count completed contamination rates (out of 21 total)
cat out/stages_oversight_phi-3-medium-4k-instruct/results.tsv 2>/dev/null | wc -l

# View latest results
tail -n 10 out/stages_oversight_phi-3-medium-4k-instruct/results.tsv 2>/dev/null

# List all result files
ls -lh out/stages_oversight_phi-3-medium-4k-instruct/ 2>/dev/null
```

#### Quick Status Check (One Command)

```bash
cd /workspace/kernel-divergence-sad && \
source /root/miniconda3/etc/profile.d/conda.sh && \
conda activate kds && \
echo "=== Running Processes ===" && \
ps aux | grep -E "run_on_runpod|main.py" | grep -v grep && \
echo -e "\n=== GPU Usage ===" && \
nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv && \
echo -e "\n=== Latest Log ===" && \
tail -n 5 run_phi-3-medium-4k-instruct.log 2>/dev/null && \
echo -e "\n=== Completed Contamination Rates ===" && \
(cat out/stages_oversight_phi-3-medium-4k-instruct/results.tsv 2>/dev/null | wc -l || echo "0") && \
echo "out of 21 total"
```

---

## Complete Setup Script (Copy-Paste All at Once)

If you want to run everything in one go:

```bash
#!/bin/bash
set -e

echo "=========================================="
echo "Phi-3-medium-4k-instruct Complete Setup"
echo "=========================================="

# Step 1: Install system dependencies
echo "Step 1: Installing system dependencies..."
apt-get update
apt-get install -y git wget curl

# Step 2: Install Miniconda
echo "Step 2: Installing Miniconda..."
if ! command -v conda &> /dev/null; then
    cd /tmp
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3
    rm Miniconda3-latest-Linux-x86_64.sh
fi

# Step 3: Initialize conda
echo "Step 3: Initializing conda..."
source /root/miniconda3/etc/profile.d/conda.sh

# Step 4: Clone repository
echo "Step 4: Cloning repository..."
cd /workspace
if [ ! -d "kernel-divergence-sad" ]; then
    git clone https://github.com/nish-shankar/kernel-divergence-sad.git
fi
cd kernel-divergence-sad
git pull origin main

# Step 5: Accept conda terms
echo "Step 5: Accepting conda terms..."
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main 2>/dev/null || true
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r 2>/dev/null || true

# Step 6: Create conda environment
echo "Step 6: Creating conda environment (this takes 10-15 minutes)..."
if ! conda env list | grep -q "^kds "; then
    conda env create -f environment.yml
else
    echo "Conda environment 'kds' already exists. Skipping creation."
fi

# Step 7: Activate environment
echo "Step 7: Activating environment..."
source /root/miniconda3/etc/profile.d/conda.sh
conda activate kds

# Step 8: Install hf_transfer
echo "Step 8: Installing hf_transfer..."
pip install hf_transfer

# Step 9: Verify installation
echo "Step 9: Verifying installation..."
python --version
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"

# Step 10: Check token file
echo "Step 10: Checking token file..."
cd /workspace/kernel-divergence-sad
if [ ! -f token ]; then
    echo "WARNING: token file not found!"
    echo "Please create it with: echo 'YOUR_HF_TOKEN' > token"
    exit 1
else
    echo "Token file found ✓"
fi

# Step 11: Verify GPU
echo "Step 11: Verifying GPU..."
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To run the experiment:"
echo "  cd /workspace/kernel-divergence-sad"
echo "  source /root/miniconda3/etc/profile.d/conda.sh"
echo "  conda activate kds"
echo "  nohup bash scripts/run_on_runpod.sh phi-3-medium-4k-instruct stages_oversight 600 train > run_phi-3-medium-4k-instruct.log 2>&1 &"
echo ""
```

---

## Expected Outputs

### During Setup

- Conda environment creation: Shows package installation progress
- Final message: "done" when environment is created
- Token verification: "SUCCESS: Model config loaded!"

### During Experiment

**Log file** (`run_phi-3-medium-4k-instruct.log`):
```
Running experiment: model=phi-3-medium-4k-instruct, dataset=stages_oversight, target_num=600, split=train
Logs: run_phi-3-medium-4k-instruct.log
Sweeping contamination from 0.00 to 1.00 (step 0.05)
==> contamination=0.00
DEBUG: Loading dataset 'stages_oversight'
Loading stages_oversight data from: stages_oversight.csv
Loaded 600 samples
Seen samples: 37, Unseen samples: 563
INFO: Extracting Embeddings!
...
```

**Results file** (`out/stages_oversight_phi-3-medium-4k-instruct/results.tsv`):
- One row per contamination rate
- 21 rows total (0.00, 0.05, 0.10, ..., 1.00)

---

## Troubleshooting

### Conda Environment Creation Fails

**Error**: `CondaEnvException: Pip failed`

**Solution**:
```bash
# Check disk space
df -h

# Remove old environment and retry
conda env remove -n kds
conda env create -f environment.yml
```

### Model Access Denied

**Error**: `OSError: You are trying to access a gated repo`

**Solution**:
1. Visit https://huggingface.co/microsoft/Phi-3-medium-4k-instruct
2. Click "Agree and access repository"
3. Wait 2-3 minutes
4. Retry

### Out of Memory

**Error**: `torch.OutOfMemoryError: CUDA out of memory`

**Solution**:
```bash
# Check GPU processes
nvidia-smi

# Kill other GPU processes if needed
kill <PID>

# Batch sizes are already minimal (1/4), so this shouldn't happen
```

### Experiment Stopped

**Check log**:
```bash
tail -n 100 run_phi-3-medium-4k-instruct.log
```

**Restart** (will skip completed contamination rates):
```bash
cd /workspace/kernel-divergence-sad
source /root/miniconda3/etc/profile.d/conda.sh
conda activate kds
nohup bash scripts/run_on_runpod.sh phi-3-medium-4k-instruct stages_oversight 600 train > run_phi-3-medium-4k-instruct.log 2>&1 &
```

### hf_transfer Error

**Error**: `ModuleNotFoundError: No module named 'hf_transfer'`

**Solution**:
```bash
pip install hf_transfer
```

Or disable fast transfer:
```bash
unset HF_HUB_ENABLE_HF_TRANSFER
```

---

## Summary

**Complete workflow**:
1. ✅ Connect to RunPod H200
2. ✅ Install system dependencies
3. ✅ Install Miniconda
4. ✅ Clone repository
5. ✅ Accept conda terms
6. ✅ Create conda environment (10-15 min)
7. ✅ Activate environment
8. ✅ Install hf_transfer
9. ✅ Verify packages
10. ✅ Setup token file
11. ✅ Verify model access
12. ✅ Verify GPU
13. ✅ Run experiment
14. ✅ Monitor progress

**Total setup time**: ~20-30 minutes  
**Experiment runtime**: ~6-8 hours  
**Total time**: ~7-9 hours

---

## Quick Reference

```bash
# Activate environment
source /root/miniconda3/etc/profile.d/conda.sh && conda activate kds

# Run experiment
cd /workspace/kernel-divergence-sad
nohup bash scripts/run_on_runpod.sh phi-3-medium-4k-instruct stages_oversight 600 train > run_phi-3-medium-4k-instruct.log 2>&1 &

# Monitor
tail -f run_phi-3-medium-4k-instruct.log

# Check progress
cat out/stages_oversight_phi-3-medium-4k-instruct/results.tsv 2>/dev/null | wc -l
```

---

## Model Details

- **Model Name**: `phi-3-medium-4k-instruct`
- **HuggingFace Path**: `microsoft/Phi-3-medium-4k-instruct`
- **Parameters**: 14B
- **Context Length**: 4,096 tokens
- **Batch Sizes**: `BATCH_SIZE=1`, `INFERENCE_BATCH_SIZE=4`
- **LoRA Modules**: `qkv_proj`
- **Wrapper**: `PhiWrapper`

---

## Support

If you encounter issues not covered here:
1. Check the log file: `run_phi-3-medium-4k-instruct.log`
2. Check GitHub issues: https://github.com/nish-shankar/kernel-divergence-sad/issues
3. Verify all prerequisites are met
4. Ensure you have sufficient GPU memory (H200 recommended)

