#!/bin/bash
# Complete Workflow: Fresh RunPod Setup for Qwen 2.5 0.5B Experiment
# ============================================================================
# Usage: Copy and paste each section into your RunPod terminal

set -e  # Exit on error

echo "=========================================="
echo "Complete Setup Workflow"
echo "=========================================="

# ============================================================================
# STEP 1: Install Conda
# ============================================================================

echo ""
echo "STEP 1: Installing Conda..."
cd /tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3
eval "$(/root/miniconda3/bin/conda shell.bash hook)"
conda --version
rm Miniconda3-latest-Linux-x86_64.sh
echo "✓ Conda installed"

# ============================================================================
# STEP 2: Install TMUX
# ============================================================================

echo ""
echo "STEP 2: Installing TMUX..."
apt-get update -qq
apt-get install -y tmux > /dev/null 2>&1
echo "✓ TMUX installed"

# ============================================================================
# STEP 3: Clone Repository
# ============================================================================

echo ""
echo "STEP 3: Cloning repository..."
cd /workspace
if [ -d "kernel-divergence-sad" ]; then
    echo "Repository exists, pulling latest changes..."
    cd kernel-divergence-sad
    git pull origin main
else
    git clone https://github.com/nish-shankar/kernel-divergence-sad.git
    cd kernel-divergence-sad
fi
echo "✓ Repository ready"

# ============================================================================
# STEP 4: Create Conda Environment
# ============================================================================

echo ""
echo "STEP 4: Creating conda environment..."
conda env create -f environment.yml -y
conda activate kds
echo "✓ Conda environment created"

# ============================================================================
# STEP 5: Install Additional Dependencies
# ============================================================================

echo ""
echo "STEP 5: Installing additional dependencies..."
pip install hf_transfer > /dev/null 2>&1
echo "✓ Dependencies installed"

# ============================================================================
# STEP 6: Setup Token (user must provide)
# ============================================================================

echo ""
echo "STEP 6: Setting up Hugging Face token..."
if [ ! -f token ]; then
    echo "WARNING: Token file not found. Please create it with:"
    echo "  echo -n 'hf_YOUR_TOKEN_HERE' > token"
else
    echo "✓ Token file exists"
fi

# ============================================================================
# STEP 7: Make Scripts Executable
# ============================================================================

echo ""
echo "STEP 7: Making scripts executable..."
chmod +x scripts/*.sh
echo "✓ Scripts executable"

# ============================================================================
# STEP 8: Verify GPU
# ============================================================================

echo ""
echo "STEP 8: Verifying GPU..."
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo "✓ GPU verified"

# ============================================================================
# STEP 9: Setup TMUX
# ============================================================================

echo ""
echo "STEP 9: Setting up TMUX..."
mkdir -p /tmp/tmux-0
chmod 700 /tmp/tmux-0
echo "✓ TMUX ready"

# ============================================================================
# DONE
# ============================================================================

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Create token file: echo -n 'hf_YOUR_TOKEN_HERE' > token"
echo "2. Run experiment: bash scripts/run_on_runpod.sh qwen2.5-0.5b"
echo "   OR in tmux: tmux new -s qwen0.5b -d 'bash /tmp/run_exp.sh'"
echo ""

