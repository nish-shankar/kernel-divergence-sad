from datasets import Dataset
import pandas as pd


def load_data(args, tokenizer, model_name, split=None):
    # Expect a user-provided file at {args.data_dir}/sad.csv (or .json/.jsonl)
    # Required column: "input". Optional: "label" (defaults to 1 for all rows).
    path_csv = f"{args.data_dir}/sad.csv"
    try:
        df = pd.read_csv(path_csv)
    except Exception:
        # Fallbacks: json or jsonl
        try:
            df = pd.read_json(f"{args.data_dir}/sad.json", lines=False)
        except Exception:
            df = pd.read_json(f"{args.data_dir}/sad.jsonl", lines=True)

    if 'input' not in df.columns:
        raise ValueError('SAD file must contain an "input" column')
    if 'label' not in df.columns:
        df['label'] = 1

    return Dataset.from_pandas(df, preserve_index=False)


