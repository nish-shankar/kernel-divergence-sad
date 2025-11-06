# Kernel Divergence Score Experiment

Run KDS experiments for Qwen models on stages_oversight dataset.

## Quick Start

### 1. Initialize Conda

```bash
# Download Miniconda installer
cd /tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install Miniconda (silent mode, to /root/miniconda3)
bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3

# Initialize conda
eval "$(/root/miniconda3/bin/conda shell.bash hook)"

# Verify installation
conda --version

# Clean up installer
rm Miniconda3-latest-Linux-x86_64.sh
```

### 2. Install TMUX

```bash
apt-get update
apt-get install -y tmux
```

### 3. Clone Repository

```bash
cd /workspace
git clone https://github.com/nish-shankar/kernel-divergence-sad.git
cd kernel-divergence-sad

# Pull latest changes (to get the updated script)
git pull origin main
```

### 4. Create Conda Environment

```bash
# Create Conda Environment (installs all dependencies from environment.yml)
conda env create -f environment.yml -y

# Activate Environment
conda activate kds

# Install hf_transfer (only missing dependency)
pip install hf_transfer
```

### 5. Set Up Hugging Face Token

```bash
# Set Up Hugging Face Token (REPLACE YOUR_TOKEN!)
echo -n "hf_YOUR_TOKEN_HERE" > token
```

### 6. Make Scripts Executable

```bash
chmod +x scripts/*.sh
```

### 7. Verify GPU

```bash
nvidia-smi
```

### 8. Run Experiment in TMUX

**For Qwen 2.5 3B model (default):**
```bash
# Run Experiment in TMUX (just activate conda, script handles the rest)
tmux new -s qwen3b -d "bash -c '
  eval \"\$(/root/miniconda3/bin/conda shell.bash hook)\"
  cd /workspace/kernel-divergence-sad
  conda activate kds
  bash scripts/run_on_runpod.sh
'"

# Attach to tmux session
tmux attach -t qwen3b
```

**For Qwen 2.5 0.5B model:**
```bash
# Run Experiment in TMUX with 0.5B model
tmux new -s qwen0.5b -d "bash -c '
  eval \"\$(/root/miniconda3/bin/conda shell.bash hook)\"
  cd /workspace/kernel-divergence-sad
  conda activate kds
  bash scripts/run_on_runpod.sh qwen2.5-0.5b
'"

# Attach to tmux session
tmux attach -t qwen0.5b
```

**For other models:**
```bash
# Usage: bash scripts/run_on_runpod.sh [model] [dataset] [target_num] [split]
# Example for Qwen 2.5 7B:
tmux new -s qwen7b -d "bash -c '
  eval \"\$(/root/miniconda3/bin/conda shell.bash hook)\"
  cd /workspace/kernel-divergence-sad
  conda activate kds
  bash scripts/run_on_runpod.sh qwen2.5-7b
'"
tmux attach -t qwen7b
```

## Configuration

The experiment configuration is set in `scripts/run_on_runpod.sh`:
- `MODEL`: Model to use (default: `qwen2.5-3b`)
- `DATASET`: Dataset name (default: `stages_oversight`)
- `TARGET_NUM`: Number of samples (default: `600`)
- `SPLIT`: Data split (default: `train`)

## Results

Results are written to `out/{dataset}_{model}/results.tsv`

Each row contains:
- Timestamp
- Experiment identifier (includes contamination rate)
- KDS score
- Full experiment arguments

## Detaching from TMUX

To detach without stopping the experiment:
- Press `Ctrl+B`, then `D`

To reattach later:
```bash
tmux attach -t qwen3b
```
