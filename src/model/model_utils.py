

model_dirs = {
    'mistral': 'mistralai/Mistral-7B-Instruct-v0.2',
    'llama3.1': 'meta-llama/Meta-Llama-3.1-8B-Instruct',
    'qwen2.5-0.5b': 'Qwen/Qwen2.5-0.5B-Instruct',
    'qwen2.5-1.5b': 'Qwen/Qwen2.5-1.5B-Instruct',
    'qwen2.5-3b': 'Qwen/Qwen2.5-3B-Instruct',
    'qwen2.5-7b': 'Qwen/Qwen2.5-7B-Instruct',
    'phi3-small': 'microsoft/Phi-3-small-128k-instruct',
    'gemma-3-0.27b-it': 'google/gemma-3-270m-it',
    'gemma-3-270m-it': 'google/gemma-3-270m-it',
    'gemma-3-1b-it': 'google/gemma-3-1b-it',
    'gemma-3-1.1b-it': 'google/gemma-3-1.1b-it',
    'gemma-3-4b-it': 'google/gemma-3-4b-it'
}


def load_model(args, model_name=None, peft_path=None):
    model_name = args.model if model_name is None else model_name
    
    if model_name == 'mistral' :
        from model.mistral import MistralWrapper
        return MistralWrapper(args, model_dirs[model_name], memory_for_model_activations_in_gb=args.memory_for_model_activations_in_gb, lora_adapter_path=peft_path)
    elif model_name in ['llama3.1', 'llama2-70b-chat', 'llama2-13b-chat', 'llama2-7b-chat', 'llama3.2-1b', 'llama3.2-3b', 'llama3.3-70b', ] :
        from model.llama import LlamaWrapper
        lversion = None
        if model_name in ['llama3.1', 'llama3.2-1b', 'llama3.2-3b', 'llama3.3-70b']:
            lversion = 3
        elif model_name in ['llama2-70b-chat', 'llama2-13b-chat', 'llama2-7b-chat']:
            lversion = 2
        return LlamaWrapper(args, model_dirs[model_name], memory_for_model_activations_in_gb=args.memory_for_model_activations_in_gb, lora_adapter_path=peft_path, llama_version=lversion)
    elif model_name in ["phi3-small", "phi3-medium"] :
        from model.phi import PhiWrapper
        return PhiWrapper(args, model_dirs[model_name], memory_for_model_activations_in_gb=args.memory_for_model_activations_in_gb, lora_adapter_path=peft_path)
    elif model_name in ["qwen2.5-0.5b", "qwen2.5-1.5b", "qwen2.5-3b", "qwen2.5-7b", "qwen2.5-14b", "qwen2.5-32b", "qwen2.5-72b"] :
        from model.qwen import QwenWrapper
        return QwenWrapper(args, model_dirs[model_name], memory_for_model_activations_in_gb=args.memory_for_model_activations_in_gb, lora_adapter_path=peft_path)
    elif model_name in ["gemma-3-0.27b-it", "gemma-3-270m-it", "gemma-3-1b-it", "gemma-3-1.1b-it", "gemma-3-4b-it"] :
        from model.gemma import GemmaWrapper
        return GemmaWrapper(args, model_dirs[model_name], memory_for_model_activations_in_gb=args.memory_for_model_activations_in_gb, lora_adapter_path=peft_path)
    else:
        raise ValueError("invalid model!")