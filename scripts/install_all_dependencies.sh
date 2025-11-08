#!/bin/bash
# Complete pip install command for all dependencies
# This installs all packages needed for the KDS experiment

pip install \
    accelerate==0.34.2 \
    datasets==2.21.0 \
    transformers==4.44.2 \
    peft==0.4.0 \
    torch==2.1.0 \
    numpy==1.24.4 \
    pandas==2.0.3 \
    tqdm==4.66.5 \
    huggingface-hub==0.24.6 \
    safetensors==0.4.5 \
    tokenizers==0.19.1 \
    sentencepiece==0.1.99 \
    protobuf==4.25.0 \
    pyyaml==6.0.1 \
    requests==2.32.3 \
    pyarrow==17.0.0 \
    dill==0.3.7 \
    hf_transfer \
    bitsandbytes==0.40.2 \
    xformers==0.0.22.post7 \
    einops==0.8.0 \
    triton==2.1.0 \
    scipy==1.10.1 \
    scikit-learn==1.3.2

