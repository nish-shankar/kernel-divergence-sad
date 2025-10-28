#!/usr/bin/env python3
"""
Extract SAD stages_oversight samples from YAML files and create CSV for KDS experiment.
This script processes the YAML files you have open and creates a labeled CSV dataset.
"""

import os
import yaml
import pandas as pd
import argparse

def extract_samples_from_yaml(file_path):
    """Extract samples from a single YAML file."""
    samples = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
            
        if 'samples' in content:
            for sample in content['samples']:
                # Extract text content
                text_content = sample.get('body', '')
                if not text_content:
                    continue
                
                # Extract choices if available
                choices = []
                if 'choices' in sample:
                    for choice in sample['choices']:
                        if isinstance(choice, dict) and 'text' in choice:
                            choices.append(choice['text'])
                        elif isinstance(choice, str):
                            choices.append(choice)
                elif 'choices_right' in sample and 'choices_wrong' in sample:
                    choices.extend(sample['choices_right'])
                    choices.extend(sample['choices_wrong'])
                
                # Format the full text
                full_text = text_content
                if choices:
                    full_text += "\nChoices:\n" + "\n".join([f"({chr(65+i)}) {c}" for i, c in enumerate(choices)])
                
                # Apply heuristic labeling for seen/unseen classification
                # Label 1 (seen): Common AI concepts, standard development stages, general knowledge
                # Label 0 (unseen): Specific evaluation scenarios, ethical dilemmas, novel oversight mechanisms
                label = 0  # Default to unseen
                
                # Heuristics to determine 'seen' (1) vs 'unseen' (0) for evaluation benchmarks
                seen_keywords = [
                    "ai development", "oversight", "safety", "ethics", "consent", 
                    "training", "model", "llm", "artificial intelligence", "machine learning",
                    "neural network", "deep learning", "algorithm", "data", "dataset"
                ]
                
                unseen_keywords = [
                    "quantum", "novel", "specific scenario", "dilemma", "hypothetical",
                    "evaluation", "benchmark", "test", "assessment", "measurement"
                ]
                
                # Check for seen keywords
                if any(keyword in full_text.lower() for keyword in seen_keywords):
                    label = 1  # Potentially seen concepts
                
                # Check for unseen keywords (override seen if found)
                if any(keyword in full_text.lower() for keyword in unseen_keywords):
                    label = 0  # More likely unseen/evaluation-specific
                
                samples.append({
                    "input": full_text,
                    "label": label
                })
                
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return samples

def main():
    parser = argparse.ArgumentParser(description='Extract SAD stages_oversight samples to CSV')
    parser.add_argument('--output', '-o', default='stages_oversight.csv', 
                       help='Output CSV file path')
    parser.add_argument('--yaml_dir', default='../sad/sad/stages/oversight/structs/batch/',
                       help='Directory containing YAML files')
    args = parser.parse_args()
    
    # Define the YAML files to process
    yaml_files = [
        os.path.join(args.yaml_dir, "oversight.yaml"),
        os.path.join(args.yaml_dir, "deploy_oversight.yaml"),
        os.path.join(args.yaml_dir, "test_oversight.yaml"),
    ]
    
    all_samples = []
    
    for file_path in yaml_files:
        if not os.path.exists(file_path):
            print(f"Warning: File not found: {file_path}")
            continue
            
        print(f"Processing: {file_path}")
        samples = extract_samples_from_yaml(file_path)
        all_samples.extend(samples)
        print(f"  Extracted {len(samples)} samples")
    
    if not all_samples:
        print("Error: No samples extracted. Check file paths and content.")
        return
    
    print(f"Total samples extracted: {len(all_samples)}")
    
    # Create DataFrame
    df = pd.DataFrame(all_samples)
    
    # Show label distribution
    seen_count = len(df[df.label == 1])
    unseen_count = len(df[df.label == 0])
    print(f"Seen samples: {seen_count}, Unseen samples: {unseen_count}")
    
    # Save to CSV
    df.to_csv(args.output, index=False)
    print(f"Saved {len(df)} samples to {args.output}")
    
    # Show sample of the data
    print("\nSample of extracted data:")
    print(df.head())
    
    print(f"\nCSV file created: {args.output}")
    print("You can now upload this CSV to your RunPod and use it with the KDS experiment!")

if __name__ == "__main__":
    main()
