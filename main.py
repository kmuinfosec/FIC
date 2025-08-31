import argparse
import sys
import os
from sklearn.metrics import confusion_matrix, classification_report

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import load_pickle_data
from flow2sig import SignatureModel

COLS_5 = [
    'Total Bwd packets', 
    'Total Fwd Packet',
    'Total Length of Bwd Packet',
    'Total Length of Fwd Packet',
    'Flow Duration'
]

# define except columns
DROP_COLS = [
    'Flow ID', 'Src IP', 'Src Port', 'Dst IP', 'Dst Port', 'Timestamp', 
    'ICMP Code', 'ICMP Type', 'Label', 'Total TCP Flow Time',
    'Attempted Category', 'id'
]

def run_analysis(train_df, test_df, feature_columns, base):
    print(f"--- {len(feature_columns)}feature, base={base} ---")

    train_data_log = train_df[feature_columns].to_numpy()
    test_data_log = test_df[feature_columns].to_numpy()
    
    y_true = (test_df['Label'].str.lower() != 'benign').astype(int)

    model = SignatureModel(base=base)
    model.fit(train_data_log)

    y_pred = model.predict(test_data_log)
    
    print("\n--- results ---")
    print(confusion_matrix(y_true, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, digits=4))
    
    print("\n---------")
    print(f"Model size: {model.get_model_size_mb():.3f} MB")
    print("-" * (40 + len(str(len(feature_columns))) + len(str(base))))


def main(args):
    try:
        train_df = load_pickle_data(args.train_data)
        test_df = load_pickle_data(args.test_data)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    cols_79 = [col for col in train_df.columns if col not in DROP_COLS]

    base_5_features = args.base
    base_79_features = args.base

    if 'train.pkl' in args.train_data:
        base_79_features = 80
        print("Info: Private/base: 80")
    elif 'train_cic.pkl' in args.train_data:
        base_79_features = 88
        print("Info: CICIDS2017/base: 88")

    run_analysis(train_df, test_df, COLS_5, base_5_features)
    
    print("\n" + "="*50 + "\n")

    run_analysis(train_df, test_df, cols_79, base_79_features)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Flow-based anomaly detection using signature matching.")
    
    parser.add_argument('--train_data', type=str, required=True, 
                        help='train data path (.pkl file)')
    parser.add_argument('--test_data', type=str, required=True, 
                        help='test data path (.pkl file)')
    parser.add_argument('--base', type=int, default=2, 
                        help='signature log base (base: 2)')
    
    args = parser.parse_args()
    main(args)