import pandas as pd
from datasets import Dataset
import os

def load_data(args, tokenizer, model_name, split=None):
    """
    Load SAD stages_oversight data from CSV file.
    
    Args:
        args: Command line arguments
        tokenizer: Tokenizer (not used for this dataset)
        model_name: Model name (not used for this dataset)
        split: Data split (not used for this dataset)
    
    Returns:
        HuggingFace Dataset object with 'input' and 'label' fields
    """
    
    # Look for the CSV file in multiple locations
    possible_paths = [
        os.path.join(args.data_dir, 'stages_oversight.csv'),
        'stages_oversight.csv',
        'src/data/stages_oversight.csv',
        os.path.join(os.path.dirname(__file__), 'stages_oversight.csv')
    ]
    
    csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_path = path
            break
    
    if not csv_path:
        raise FileNotFoundError(f"stages_oversight.csv not found in any of these locations: {possible_paths}")
    
    print(f"Loading stages_oversight data from: {csv_path}")
    
    # Load CSV file
    df = pd.read_csv(csv_path)
    
    print(f"Loaded {len(df)} samples")
    print(f"Seen samples: {len(df[df.label == 1])}, Unseen samples: {len(df[df.label == 0])}")
    
    # Create HuggingFace Dataset
    dataset = Dataset.from_dict({
        "input": df["input"].tolist(),
        "label": df["label"].tolist()
    })
    
    return dataset
