# Flow-based Intrusion Classification (FIC)

This project implements a lightweight, flow-based intrusion detection system using a signature matching algorithm. It generates unique signatures for normal network flows from training data and uses them to detect anomalies in test data.

## Prerequisites

- Python 3.6 or higher
- Pip package manager

## Setup

Install the required Python libraries:
```bash
pip install -r requirements.txt
```

## Usage

Run the `main.py` script with the paths to your training and testing data. The data should be in `.pkl` format (pickled Pandas DataFrame).

```bash
python main.py --train_data <path_to_train_data.pkl> --test_data <path_to_test_data.pkl>
```

You can also specify the base for the logarithm used in signature generation with the `--base` argument (default is 2).

```bash
python main.py --train_data <path_to_train_data.pkl> --test_data <path_to_test_data.pkl> --base 10
```

## Output

The script will print the following information to the console:

-   Progress of data loading, model training, and prediction.
-   **Evaluation Results:** A confusion matrix and a detailed classification report (precision, recall, f1-score).
-   **Performance Info:** The final size of the generated signature model.
