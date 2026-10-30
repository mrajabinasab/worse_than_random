# Random Feature Selection Baseline with FSEVAL

This repository evaluates **random feature selection** as a baseline for feature selection methods, using the [FSEVAL](https://github.com/mrajabinasab/FSEVAL) benchmark (`sdufseval` on PyPI). It accompanies the paper [*Worse than Random: The Importance of a Baseline for Unsupervised Feature Selection*](https://arxiv.org/abs/2605.22973).

A random ranking is obtained by assigning every feature a score drawn uniformly from [0, 1). Repeating this 100 times per dataset gives the distribution of performance that a feature selection method achieves by chance. A method that does not clearly outperform this distribution provides no evidence of selecting informative features.

## FSEVAL

| Resource | Link |
| :--- | :--- |
| Python package (PyPI) | [pypi.org/project/sdufseval](https://pypi.org/project/sdufseval/) |
| Source code (GitHub) | [github.com/mrajabinasab/FSEVAL](https://github.com/mrajabinasab/FSEVAL) |
| Interactive dashboard | [fseval.imada.sdu.dk](https://fseval.imada.sdu.dk/) |
| Paper (arXiv) | [arXiv:2604.18227](https://doi.org/10.48550/arXiv.2604.18227) |

## Protocol

| Setting | Value |
| :--- | :--- |
| Random rankings per dataset | 100 (seeds `random_state` to `random_state + 99`) |
| Subset sizes | 0.5% to 10% of the features (step 0.5%) and 5% to 100% (step 5%) |
| Supervised metrics | ACC and AUC, stratified 5-fold cross-validation repeated with 5 seeds, for SVM, KNN, XGBoost, Random Forest, and Decision Tree |
| Unsupervised metrics | Clustering accuracy (CLSACC) and NMI of K-means with as many clusters as classes, repeated with 10 seeds |
| Model-agnostic metric | AAD |
| Stability | FSDEM stability of every performance curve |
| Base seed | 42 |

All 100 runs are saved individually, so the results contain the full distribution of the baseline and not only its mean.

## Requirements

- Python 3.11 or later
- [`sdufseval`](https://pypi.org/project/sdufseval/) 1.3.0 or later, which installs all other dependencies

## Installation

```bash
git clone <this repository>
cd <repository folder>
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Data

Place the datasets in a `datasets/` folder, in one of two formats:

- `{name}.mat` with the keys `X` (samples × features) and `Y` (labels), as distributed by [scikit-feature](https://jundongl.github.io/scikit-feature/datasets.html)
- `{name}_X.csv` and `{name}_y.csv`, each with a header row

The default benchmark uses 23 datasets: ALLAML, arcene, Carcinom, CLL_SUB_111, COIL20, colon, gisette, GLI_85, GLIOMA, Isolet, leukemia, lung, lung_discrete, madelon, ORL, orlraws10P, pixraw10P, Prostate_GE, SMK_CAN_187, TOX_171, warpAR10P, warpPIE10P, and Yale. Datasets that are missing are reported and skipped; the run continues with the others.

## Usage

Run the full benchmark:

```bash
python run_random.py
```

Options:

| Option | Default | Description |
| :--- | :--- | :--- |
| `--data-dir` | `datasets` | Folder containing the datasets. |
| `--output-dir` | `results` | Folder for the result files. |
| `--datasets` | the 23 datasets above | Space-separated dataset names. |
| `--runs` | 100 | Number of random rankings per dataset. |
| `--random-state` | 42 | Base seed. |
| `--n-jobs` | -1 | Number of CPU cores; -1 uses all cores. |
| `--force` | off | Recompute datasets that are already complete. |

For example, a quick test on two datasets:

```bash
python run_random.py --datasets colon leukemia --runs 5 --output-dir test_results
```

The full benchmark is computationally demanding: every random ranking is evaluated with five classifiers and K-means at 40 subset sizes. On a server, run it in the background and keep a log:

```bash
nohup python run_random.py > random.log 2>&1 &
```

Interrupted runs can be restarted with the same command. Datasets that are already complete are skipped, and datasets whose settings changed are recomputed.

## Output

The result files are written to `results/`. Each performance file has one row per run and dataset (100 rows per dataset) and one column per subset size.

| File | Content |
| :--- | :--- |
| `Random_{CLSACC,NMI}_{Range}_USI10_RS42.csv` | Clustering accuracy and NMI. |
| `Random_{ACC,AUC}_{Range}_SI5_CV5_RS42.csv` | ACC and AUC averaged over the five classifiers. |
| `Random_{Classifier}_{ACC,AUC}_{Range}_SI5_CV5_RS42.csv` | ACC and AUC of each classifier. |
| `Random_AAD_{Range}_RS42.csv` | AAD. |
| `Random_{Metric}_Stability_{Range}_{Settings}.csv` | Mean stability of the performance curves per dataset. |

`{Range}` is `10Percent` or `100Percent`. The suffix records the evaluation settings: `SI5_CV5` is 5 seeds of 5-fold cross-validation, `USI10` is 10 clustering seeds, and `RS42` is the base seed.

The files can be loaded directly into the [FSEVAL dashboard](https://fseval.imada.sdu.dk/) with its Import button, where the random baseline is shown as a mean curve with a band of one standard deviation.

## Citation

If you use this baseline in your research, please cite the paper:

```bibtex
@article{rajabinasab2026worse,
  author       = {Muhammad Rajabinasab and
                  Michael E. Houle and
                  Oussama Chelly and
                  Arthur Zimek},
  title        = {Worse than Random: The Importance of a Baseline for Unsupervised Feature Selection},
  journal      = {CoRR},
  volume       = {abs/2605.22973},
  year         = {2026},
  url          = {https://arxiv.org/abs/2605.22973},
  eprinttype   = {arXiv},
  eprint       = {2605.22973}
}
```

and FSEVAL:

```bibtex
@article{DBLP:journals/corr/abs-2604-18227,
  author       = {Muhammad Rajabinasab and
                  Arthur Zimek},
  title        = {{FSEVAL:} Feature Selection Evaluation Toolbox and Dashboard},
  journal      = {CoRR},
  volume       = {abs/2604.18227},
  year         = {2026},
  url          = {https://doi.org/10.48550/arXiv.2604.18227},
  doi          = {10.48550/ARXIV.2604.18227},
  eprinttype   = {arXiv},
  eprint       = {2604.18227}
}
```

## License

MIT License, see [LICENSE](LICENSE).
