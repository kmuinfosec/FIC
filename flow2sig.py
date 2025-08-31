import numpy as np
import hashlib
import math
import sys

class SignatureModel:
    """
    A model that creates signatures based on flow data and uses them
    to determine normal/abnormal behavior.
    """
    def __init__(self, base=2):
        """
        Initializes the model.
        :param base: The base of the logarithm for signature generation (default: 2)
        """
        self.base = base
        self.signature_set = set()

    def _flow2sig(self, arr):
        """
        Internal function to generate a signature array from an input array.
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
        Creates a set of normal behavior signatures using training data.
        :param data: Training data (Numpy array)
        """
        print("Starting training...")
        signatures = self._flow2sig(data)
        self.signature_set = set(signatures)
        print(f"Training complete. Generated {len(self.signature_set)} unique signatures.")

    def predict(self, data):
        """
        Predicts whether the test data represents anomalous behavior.
        :param data: Test data (Numpy array)
        :return: List of prediction results (0: normal, 1: abnormal)
        """
        print("Starting prediction...")
        y_pred = []
        for row in data:
            # Make each row a 2D array to process it individually.
            row_2d = np.expand_dims(row, axis=0)
            sig = self._flow2sig(row_2d)[0]
            y_pred.append(0 if sig in self.signature_set else 1)
        print("Prediction complete.")
        return y_pred

    def get_model_size_mb(self):
        """
        Returns the memory size of the current model (signature set) in MB.
        """
        return sys.getsizeof(self.signature_set) / (1024**2)