import numpy as np
import hashlib
import math

class FIC:
    """
    A model that creates signatures based on flow data and uses them
    to determine normal/abnormal behavior via membership checking.
    """
    def __init__(self, base=2):
        """
        Initialize the model.

        Parameters
        ----------
        base : int
            Logarithm base used for discretization (default: 2).
        """
        self.base = base
        self.signature_set = set()

    def flow2sig(self, arr):
        """
        Internal function to generate a signature array from an input array.

        Parameters
        ----------
        arr : np.ndarray
            2D array of shape (n_samples, n_features)

        Returns
        -------
        np.ndarray
            1D array of dtype=uint64, length n_samples
        """
        arr = np.asarray(arr, dtype=np.float64)
        np.log1p(arr, out=arr)
        arr /= math.log(self.base)
        np.floor(arr, out=arr)
        arr = arr.astype(np.int8)
        
        out = np.empty(arr.shape[0], dtype=np.uint64)
        for i, row in enumerate(arr):
            h = hashlib.blake2b(row.tobytes(), digest_size=8).digest()
            out[i] = int.from_bytes(h, 'little', signed=False)
        return out

    def fit(self, data):
        """
        Create a set of normal behavior signatures using training data.

        Parameters
        ----------
        data : np.ndarray
            Training data (n_samples, n_features).
        """
        print("Starting training...")
        signatures = self.flow2sig(data)
        self.signature_set = set(signatures)
        print(f"Training complete. Generated {len(self.signature_set)} unique signatures.")

    def predict(self, data):
        """
        Predict whether the test data represents anomalous behavior.

        Parameters
        ----------
        data : np.ndarray
            Test data (n_samples, n_features).

        Returns
        -------
        np.ndarray
            1D int array (0: benign/in-set, 1: anomalous/out-of-set)
        """
        print("Starting prediction...")
        y_pred = []
        for row in data:
            row_2d = np.expand_dims(row, axis=0)
            sig = self.flow2sig(row_2d)[0]
            y_pred.append(0 if sig in self.signature_set else 1)
        print("Prediction complete.")
        return y_pred

    def set_signature_set(self, signature_set):
        """
        Replace the internal signature set used for membership checks.

        Parameters
        ----------
        signature_set : Iterable[int] or set[int]
            A collection of precomputed signatures (e.g., 64-bit hashes).
        """
        self.signature_set = signature_set