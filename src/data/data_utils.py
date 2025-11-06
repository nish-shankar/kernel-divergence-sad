
from datasets import Dataset


def load_data(args, tokenizer, model_name, split):
    print(f"DEBUG: Loading dataset '{args.data}'")
    if args.data == 'truthful_qa':
        from data.truthful_qa import load_data as load_truthfulqa
        return load_truthfulqa(args, tokenizer, model_name, split=split)
    elif args.data == 'wikimia':
        from data.wikimia import load_data as load_wikimia
        return load_wikimia(args, tokenizer, model_name, split=split)
    elif args.data == 'bookmia':
        from data.bookmia import load_data as load_bookmia
        return load_bookmia(args, tokenizer, model_name, split=split)
    elif args.data == 'arxivtection':
        from data.arxivtection import load_data as load_arxivtection
        return load_arxivtection(args, tokenizer, model_name, split=split)
    elif args.data == 'stages_oversight':
        from data.stages_oversight import load_data as load_stages_oversight
        return load_stages_oversight(args, tokenizer, model_name, split=split)
    elif args.data == 'sad':
        from data.sad import load_data as load_sad
        return load_sad(args, tokenizer, model_name, split=split)
    elif args.data in ['cc','enron','hackernews','philpapers','stackexchange','wikipedia']:
        from data.pile import load_data as load_pile
        return load_pile(args, tokenizer, model_name, split=split)
    else:
        raise ValueError("Unsupported dataset has been supplied")


def get_data_subsets(args, dataset):
    '''
        selects sample_size + landmark_size amount of data w.r.t. contamination rate
    '''
    dataset = dataset.shuffle(seed=args.seed)
    in_dataset = Dataset.from_dict(dataset[[idx for idx, x in enumerate(dataset['label']) if x==1]])
    out_dataset = Dataset.from_dict(dataset[[idx for idx, x in enumerate(dataset['label']) if x==0]])
    
    # Get actual available samples
    max_in_samples = len(in_dataset)
    max_out_samples = len(out_dataset)
    
    in_num = int(args.target_num * args.contamination)
    out_num = args.target_num - in_num

    # Clamp to available samples (matching old behavior exactly)
    # Old code silently used min(requested, available) via Python slicing
    # This just makes it explicit and adds warnings
    original_in_num = in_num
    original_out_num = out_num
    
    # Match old behavior: Python slicing returns min(requested, available)
    actual_in = min(in_num, max_in_samples)
    actual_out = min(out_num, max_out_samples)
    
    # Only warn if we're hitting limits
    if in_num > max_in_samples:
        print(f"WARNING: Requested {in_num} seen samples but only {max_in_samples} available. Using {actual_in} seen samples.")
    if out_num > max_out_samples:
        print(f"WARNING: Requested {out_num} unseen samples but only {max_out_samples} available. Using {actual_out} unseen samples.")
    
    # Use the actual values (matching old slicing behavior)
    in_num = actual_in
    out_num = actual_out

    in_data_subset = Dataset.from_dict(in_dataset[:in_num])
    out_data_subset = Dataset.from_dict(out_dataset[:out_num])
    in_labels = [1] * in_num
    out_labels = [0] * out_num

    return in_data_subset, out_data_subset, in_labels, out_labels

