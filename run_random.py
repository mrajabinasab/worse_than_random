import argparse

from sdufseval import FSEVAL

DATASETS = [
    "ALLAML", "arcene", "Carcinom", "CLL_SUB_111", "COIL20", "colon",
    "gisette", "GLI_85", "GLIOMA", "Isolet", "leukemia", "lung",
    "lung_discrete", "madelon", "ORL", "orlraws10P", "pixraw10P",
    "Prostate_GE", "SMK_CAN_187", "TOX_171", "warpAR10P", "warpPIE10P", "Yale",
]


def parse_args():
    p = argparse.ArgumentParser(description="Evaluate the random feature selection baseline with FSEVAL.")
    p.add_argument("--data-dir", default="datasets", help="folder with {name}.mat or {name}_X.csv/{name}_y.csv files")
    p.add_argument("--output-dir", default="results", help="folder for the result CSV files")
    p.add_argument("--datasets", nargs="+", default=DATASETS, help="dataset names (default: the 23 benchmark datasets)")
    p.add_argument("--runs", type=int, default=100, help="number of random rankings per dataset")
    p.add_argument("--random-state", type=int, default=42, help="base seed")
    p.add_argument("--n-jobs", type=int, default=-1, help="CPU cores to use, -1 for all")
    p.add_argument("--force", action="store_true", help="recompute datasets that are already complete")
    return p.parse_args()


def main():
    args = parse_args()

    evaluator = FSEVAL(
        output_dir=args.output_dir,
        data_dir=args.data_dir,
        avg_steps=args.runs,
        supervised_iter=5,
        unsupervised_iter=10,
        cv=5,
        random_state=args.random_state,
        n_jobs=args.n_jobs,
        eval_type=["unsupervised", "supervised"],
        experiments=["10Percent", "100Percent"],
        stability=True,
        save_all=True,                 # one row per run, needed for the spread of the baseline
        save_classifier_results=True,  # per-classifier ACC/AUC, used by the FSEVAL dashboard
    )

    methods = [{
        "name": "Random",
        "type": "unsupervised",
        "stochastic": True,
        "func": evaluator.random_baseline,
    }]

    evaluator.run(args.datasets, methods, force=args.force)


if __name__ == "__main__":  # required, FSEVAL runs in parallel processes
    main()