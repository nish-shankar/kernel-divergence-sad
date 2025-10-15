# Kernel Divergence Score

An altered implementation of ICML 2025 paper, "[How Contaminated Is Your Benchmark? Measuring Dataset Leakage in Large Language Models with Kernel Divergence](https://arxiv.org/abs/2502.00678)" by Hyeong Kyu Choi*, Maxim Khanov*, Hongxin Wei, and Yixuan Li (with edits made by Nishith Shankar).

## Setup Environment
```
git clone https://github.com/nish-shankar/kernel-divergence-sad.git
cd kernel-divergence-sad
```

```
conda env create -f environment.yml
conda activate kds
```

Finally, create a "token" file right outside the ```src/``` directory (note that there shouldn't be any extension in the file name), containing your huggingface credential token.


## Experiments

Experiment commands are in ```scripts/```. Each shell file computes the kernel divergence scores for contamination rate 0.0~1.0 on seed 0.

```
sh scripts/wikimia.sh
```


```
sh scripts/bookmia.sh
```

```
sh scripts/arxivtection.sh
```

```
sh scripts/pile.sh
```


## SAD (Situational Awareness Dataset) Usage

1. Prepare your data file at `<data_dir>/sad.csv` with columns:
   - `input`: text prompt/question
   - `label`: 1 (for single-benchmark KDS; optional; defaults to 1)

2. Run with Llama 3.1 Instruct 8B (or any allowed model allowed in the codebase):
```
python src/main.py \
  --data sad \
  --model llama3.1 \
  --data_dir /ABSOLUTE/PATH/TO/SAD_DIR \
  --target_num 1000 \
  --contamination 1.0 \
  --sgd \
  --lr 0.0001 \
  --seed 0
```

3. Results are written to `out/results.tsv` with a row ending `_KDS` that contains the Kernel Divergence Score.


## Citation
```
@inproceedings{choi2024beyond,
      title={How Contaminated Is Your Benchmark? Measuring Dataset Leakage in Large Language Models with Kernel Divergence}, 
      author={Hyeong Kyu Choi and Maxim Khanov and Hongxin Wei and Yixuan Li},
      booktitle = {International Conference on Machine Learning},
      year = {2025}
}
```
