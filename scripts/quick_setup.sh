#!/usr/bin/env bash
set -euo pipefail

# Quick setup script for RunPod H200 GPU
# Usage: bash scripts/quick_setup.sh

echo "=========================================="
echo "KDS Experiment Quick Setup"
echo "=========================================="

# Ensure we're at repo root
cd "$(dirname "$0")/.."

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Installing Miniconda..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
    bash /tmp/miniconda.sh -b -p /root/miniconda3
    rm /tmp/miniconda.sh
    echo "Miniconda installed!"
fi

# Initialize conda
source /root/miniconda3/etc/profile.d/conda.sh || true

# Check if environment exists
if conda env list | grep -q "^kds "; then
    echo "Conda environment 'kds' already exists. Skipping creation."
    echo "To recreate, run: conda env remove -n kds && conda env create -f environment.yml"
else
    echo "Creating conda environment..."
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main 2>/dev/null || true
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r 2>/dev/null || true
    conda env create -f environment.yml
    echo "Conda environment created!"
fi

# Activate environment
source /root/miniconda3/etc/profile.d/conda.sh
conda activate kds

# Check token file
if [[ ! -f token ]]; then
    echo ""
    echo "=========================================="
    echo "WARNING: token file not found!"
    echo "=========================================="
    echo "If you're reusing the same setup as Gemma-3 12B, the token file should already exist."
    echo "If not, create a 'token' file with your HuggingFace token:"
    echo "  echo 'YOUR_HF_TOKEN' > token"
    echo ""
    echo "Get your token from: https://huggingface.co/settings/tokens"
    echo ""
    exit 1
else
    echo "Token file found (reusing from previous setup)"
fi

# Verify GPU
echo ""
echo "Checking GPU..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
    echo "WARNING: nvidia-smi not found. GPU may not be available."
fi

# Verify Python and key packages
echo ""
echo "Verifying installation..."
python --version
python -c "import torch; print(f'PyTorch: {torch.__version__}')" || echo "ERROR: PyTorch not installed"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')" || echo "ERROR: Transformers not installed"

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To run the Gemma-3 27B experiment:"
echo "  bash scripts/run_on_runpod.sh gemma-3-27b-it stages_oversight 600 train"
echo ""
echo "Or run in background:"
echo "  nohup bash scripts/run_on_runpod.sh gemma-3-27b-it stages_oversight 600 train > run_gemma-3-27b-it.log 2>&1 &"
echo ""

