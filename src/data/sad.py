from datasets import load_dataset, Dataset
import pandas as pd


def load_data(args, tokenizer, model_name, split=None):
    # Load SAD dataset from Hugging Face
    try:
        # Try to load from the official SAD dataset
        dataset = load_dataset('LRudL/sad', cache_dir=args.data_dir)
        
        # Convert to pandas for easier processing
        df = dataset['test'].to_pandas()  # Use test split by default
        
        # Extract the text content - SAD has different task categories
        # We'll combine all the question/prompt text into 'input' column
        texts = []
        for _, row in df.iterrows():
            # Combine question and context if available
            text = row.get('question', '')
            if 'context' in row and pd.notna(row['context']):
                text = f"{text} {row['context']}"
            texts.append(text)
        
        df['input'] = texts
        df['label'] = 1  # All SAD data is considered "in-domain"
        
        return Dataset.from_pandas(df, preserve_index=False)
        
    except Exception as e:
        print(f"Failed to load SAD from Hugging Face: {e}")
        print("Falling back to local file...")
        
        # Fallback to local file
        path_csv = f"{args.data_dir}/sad.csv"
        try:
            df = pd.read_csv(path_csv)
        except Exception:
            try:
                df = pd.read_json(f"{args.data_dir}/sad.json", lines=False)
            except Exception:
                df = pd.read_json(f"{args.data_dir}/sad.jsonl", lines=True)

        if 'input' not in df.columns:
            raise ValueError('SAD file must contain an "input" column')
        if 'label' not in df.columns:
            df['label'] = 1

        return Dataset.from_pandas(df, preserve_index=False)


