import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import load_csv_data, save_sigset, load_sigset, save_preds
from flow2sig import FIC

def train(train_df, base, sigset_path):
    model = FIC(base=base)
    model.fit(train_df.to_numpy())
    save_sigset(sigset_path, model.signature_set)

def test(test_df, base, sigset_path, result_path):
    sigset = load_sigset(sigset_path)
    model = FIC(base=base)
    model.set_signature_set(sigset)
    y_pred = model.predict(test_df.to_numpy())
    save_preds(result_path, y_pred)

def main(args):
    try:
        train_df = load_csv_data(args.train_data) if args.train_data else None
        test_df  = load_csv_data(args.test_data)  if args.test_data  else None

        base = args.base
        if base <= 1:
            raise ValueError("`base` must be greater than 1.")
        sigset_path = args.sigset
        result_path = args.result

        if train_df is not None and test_df is not None:
            train(train_df, base, sigset_path)
            test(test_df, base, sigset_path, result_path)
            return

        if train_df is not None:
            train(train_df, base, sigset_path)
            return

        if test_df is not None:
            test(test_df, base, sigset_path, result_path)
            return

    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    sys.exit("error: provide --train_data and/or --test_data")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Flow-based anomaly detection using signature matching."
    )
    parser.add_argument("--train_data", type=str, help="Train data path (.csv)")
    parser.add_argument("--test_data",  type=str, help="Test data path (.csv)")
    parser.add_argument(
        "--sigset",
        type=str,
        default="sigset.npy",
        help="Signature set path (.npy). In train: save to this file; in test: load from this file. [default: sigset.npy]"
    )
    parser.add_argument(
        "--result",
        type=str,
        default="predictions.csv",
        help="Path to save y_pred as CSV. [default: predictions.csv]"
    )
    parser.add_argument("--base", type=int, default=2, help="Signature log base. [default: 2]")
    args = parser.parse_args()

    main(args)