#!/bin/bash

# SAD Stages_Oversight KDS Experiment Script
# This script runs the Kernel Divergence Score experiment on the SAD stages_oversight dataset

# Define the model and dataset
DATASET_NAME="stages_oversight"
MODEL_NAME="qwen2.5-0.5b"  # Corresponds to 'Qwen/Qwen2.5-0.5B-Instruct'
TARGET_NUM_SAMPLES=2000  # Total samples from CSV file
OUTPUT_DIR="out/${DATASET_NAME}_${MODEL_NAME}"

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

echo "Starting KDS experiment for ${DATASET_NAME} with ${MODEL_NAME} model."
echo "Target number of samples: ${TARGET_NUM_SAMPLES}"
echo "Output directory: ${OUTPUT_DIR}"

# Loop through contamination rates from 0.0 to 1.0 with a step of 0.05
for c in $(seq 0.00 0.05 1.00); do
  echo "Running contamination rate: $c"
  CUDA_VISIBLE_DEVICES=0 python src/main.py \
    --data $DATASET_NAME \
    --model $MODEL_NAME \
    --target_num $TARGET_NUM_SAMPLES \
    --out_dir $OUTPUT_DIR \
    --contamination $c \
    --sgd \
    --lr 0.0001 \
    --seed 0 \
    --batch_size 4 \
    --inference_batch_size 16 \
    --memory_for_model_activations_in_gb 2 \
    --exp_name "${MODEL_NAME}_${DATASET_NAME}_${TARGET_NUM_SAMPLES}_train_${c}_sgd_seed0_KDS"
done

echo "Experiment for ${DATASET_NAME} with ${MODEL_NAME} completed."
echo "Results are in ${OUTPUT_DIR}/results.tsv"
