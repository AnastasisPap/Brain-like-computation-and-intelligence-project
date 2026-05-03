"""
Utility functions for the NX-414 brain-model alignment project.
Covers HDF5 inspection and stimulus-to-feature index matching.
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
from typing import Literal
import numpy as np
from scipy import stats
from scipy.spatial.distance import pdist, squareform

def inspect_h5(path, max_depth=2, _prefix="", _depth=0):
    """
    Print the structure of an HDF5 file, showing dataset shapes and dtypes.
    Useful for quickly understanding what is stored in a .h5 file without
    loading any data into memory.
    """
    with h5py.File(path, "r") as f:
        _inspect_group(f, max_depth=max_depth, _prefix=_prefix, _depth=_depth)

def _inspect_group(group, max_depth, _prefix, _depth):
    """Recursive helper that walks through HDF5 groups and datasets."""
    for key in group.keys():
        item = group[key]
        full_key = f"{_prefix}/{key}" if _prefix else key
        if isinstance(item, h5py.Dataset):
            print(f"  [{full_key}]  shape={item.shape}  dtype={item.dtype}")
        elif isinstance(item, h5py.Group):
            print(f"  <group> {full_key}/")
            if _depth < max_depth - 1:
                _inspect_group(item, max_depth, full_key, _depth + 1)
            else:
                print(f"    ... (max depth reached)")

def build_id_index(feat_path):
    """
    Build a dictionary mapping each stimulus ID to its row index in a
    feature file. This lets us quickly look up which row corresponds to
    a given stimulus when matching neural responses to model features.
    """
    with h5py.File(feat_path, "r") as f:
        ids = f["ids"][:]
    return {id_: i for i, id_ in enumerate(ids)}

def get_feat_rows(feat_path, layer_key, neural_ids):
    """
    Load feature rows from a feature file for a given set of stimulus IDs,
    returning them in the same order as neural_ids. Internally sorts the
    row indices before reading to keep HDF5 access efficient, then restores
    the original order.
    """
    id_to_idx = build_id_index(feat_path)
    feat_idx = np.array([id_to_idx[x] for x in neural_ids])

    sort_order = np.argsort(feat_idx)
    restore_order = np.argsort(sort_order)
    sorted_idx = feat_idx[sort_order]

    with h5py.File(feat_path, "r") as f:
        feats = f[layer_key][sorted_idx]

    return feats[restore_order]

def plot_mean_eeg_heatmap(eeg_path, subject, roi, 
                           threshold_zscore=2.5, 
                           percentile_abs=99.11,
                           channel_threshold=0.10,
                           save_path=None):
    
    with h5py.File(eeg_path, "r") as f:
        data = f[f"train/neural_data/{subject}/{roi}"][:]
    
    n_stim, n_ch, n_tp = data.shape
    
    # Compute quality mask
    ep_var      = data.var(axis=2)
    s_mean      = ep_var.mean(axis=0)
    s_std       = ep_var.std(axis=0)
    ep_var_norm = (ep_var - s_mean) / (s_std + 1e-8)
    max_abs     = np.abs(data).max(axis=2)
    thresh_abs  = np.percentile(max_abs, percentile_abs)
    q_mask      = (ep_var_norm > threshold_zscore) | (max_abs > thresh_abs)
    
    # Identify clean channels
    flagged_per_channel = q_mask.mean(axis=0)
    clean_channels      = flagged_per_channel < channel_threshold
    print(f"Clean channels: {clean_channels.sum()} / {n_ch} ({100 * clean_channels.mean():.1f}%)")
    
    # Average over clean stimuli per channel
    clean_mean = np.zeros((n_ch, n_tp))
    for ch in range(n_ch):
        clean_stimuli  = ~q_mask[:, ch]
        clean_mean[ch] = data[clean_stimuli, ch, :].mean(axis=0)
    
    clean_mean_filtered = clean_mean[clean_channels]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(clean_mean_filtered, aspect="auto", cmap="RdBu_r",
                   interpolation="nearest",
                   extent=[0, 0.8, clean_mean_filtered.shape[0], 0])
    # ax.axvline(x=0, color="black", linewidth=1, linestyle="--", label="Stimulus onset")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Channel index (clean channels only)")
    ax.set_title(f"Mean EEG response — {subject} / {roi} (clean channels only)")
    plt.colorbar(im, ax=ax, label="Mean amplitude")
    ax.legend()
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()

def compute_ceiling_variancebased(
    responses: np.ndarray,
    nan_policy: str = "omit",
) -> np.ndarray:
    """
    Variance-based noise ceiling (Allen et al. 2022 style).
 
    Input
    -----
    responses : (n_channels, n_timepoints, n_stimuli, n_reps)
        or  (n_units, n_stimuli, n_reps)
 
    Steps
    -----
    1. z-score across stimuli (axis=-2) for each (unit, rep).
    2. Noise variance = var across reps (ddof=1), averaged over stimuli.
    3. Signal variance = max(1 − noise_var, 0).
    4. SNR = signal_var / noise_var.
    5. nc (%) = 100 · SNR / (SNR + 1 / n_reps).
 
    Returns
    -------
    nc : (n_channels, n_timepoints) or (n_units,)  in percent [0, 100]
    """
    R = np.asarray(responses, dtype=np.float64)
    # last two axes are always (..., n_stimuli, n_reps)
    n_reps = R.shape[-1]
 
    # z-score across stimuli for each (unit, rep) — axis=-2
    mu = R.mean(axis=-2, keepdims=True)
    sd = R.std(axis=-2, keepdims=True)
    if nan_policy == "omit":
        mu = np.nanmean(R, axis=-2, keepdims=True)
        sd = np.nanstd(R, axis=-2, keepdims=True)
    Rz = (R - mu) / (sd + 1e-12)
 
    # noise variance: var across reps, then mean across stimuli
    noise_var = np.nanvar(Rz, axis=-1, ddof=1).mean(axis=-1)   # drop stim & rep axes
    signal_var = np.maximum(1.0 - noise_var, 0.0)
 
    snr = signal_var / (noise_var + 1e-12)
    nc = 100.0 * snr / (snr + 1.0 / n_reps)
    return nc
 
 
def compute_ceiling_splithalf(
    responses: np.ndarray,
    folds: int = 10,
    seed: int = 0,
    spearman_brown: bool = True,
    equalize_halves: bool = True,
    clip_folds: bool = False,
) -> np.ndarray:
    """
    Split-half reliability (van Bree et al. 2025).
 
    Input
    -----
    responses : (n_channels, n_timepoints, n_stimuli, n_reps)
        or  (n_units, n_stimuli, n_reps)
 
    Steps
    -----
    1. Randomly split reps into two equal halves (drop one if n_reps is odd).
    2. Average each half over reps → two response matrices over stimuli.
    3. Pearson r across stimuli for each unit.
    4. Spearman-Brown correction: r_sb = 2r / (1 + r).
    5. Average across folds.
 
    Returns
    -------
    nc : (n_channels, n_timepoints) or (n_units,)  in [0, 1]
    """
    R = np.asarray(responses, dtype=np.float64)
    n_reps = R.shape[-1]
    half = n_reps // 2          # always equal halves (drop last rep if odd)
    rng  = np.random.default_rng(seed)
 
    fold_results = []
    for f in range(folds):
        idx = rng.permutation(n_reps)
        if equalize_halves:
            h1_idx = idx[:half]
            h2_idx = idx[half : 2 * half]
        else:
            h1_idx = idx[:half]
            h2_idx = idx[half:]
 
        h1 = R[..., h1_idx].mean(axis=-1)   # (..., n_stimuli)
        h2 = R[..., h2_idx].mean(axis=-1)
 
        # Pearson r across stimuli (axis=-1) for every unit
        h1c = h1 - h1.mean(axis=-1, keepdims=True)
        h2c = h2 - h2.mean(axis=-1, keepdims=True)
        num  = (h1c * h2c).sum(axis=-1)
        den  = np.sqrt((h1c**2).sum(axis=-1) * (h2c**2).sum(axis=-1)) + 1e-12
        r    = num / den
 
        if spearman_brown:
            r = 2.0 * r / (1.0 + np.abs(r) + 1e-12)  # |r| in denominator for stability
 
        if clip_folds:
            r = np.clip(r, 0.0, 1.0)
 
        fold_results.append(r)
 
    nc = np.array(fold_results).mean(axis=0)
    return np.clip(nc, 0.0, 1.0)

def compute_ceiling_variancebased_clean(
    responses: np.ndarray,
    nan_policy: str = "omit",
) -> np.ndarray:
    """
    Nan-safe version of compute_ceiling_variancebased.
    Use this when responses contain NaN entries from QC masking.
    The key fix is using np.nanmean instead of .mean() when averaging
    noise variance across stimuli, so channels with partial NaN entries
    still produce a valid estimate rather than propagating NaN.
    """
    R = np.asarray(responses, dtype=np.float64)
    n_reps = R.shape[-1]

    # z-score across stimuli for each (unit, rep) — always nan-safe
    mu = np.nanmean(R, axis=-2, keepdims=True)
    sd = np.nanstd(R, axis=-2, keepdims=True)
    Rz = (R - mu) / (sd + 1e-12)

    # noise variance: nanvar across reps, then nanmean across stimuli
    noise_var = np.nanvar(Rz, axis=-1, ddof=1)   # (..., n_stimuli)
    noise_var = np.nanmean(noise_var, axis=-1)    # (...,)  — KEY FIX
    signal_var = np.maximum(1.0 - noise_var, 0.0)

    snr = signal_var / (noise_var + 1e-12)
    # effective n_reps per unit — count non-NaN reps averaged over stimuli
    n_valid = (~np.isnan(R)).sum(axis=-1).mean(axis=-1)  # (...) mean over stimuli
    n_valid = np.maximum(n_valid, 1.0)                    # avoid division by zero
    
    snr = signal_var / (noise_var + 1e-12)
    nc = 100.0 * snr / (snr + 1.0 / n_valid)
    return nc


def compute_ceiling_splithalf_clean(
    responses: np.ndarray,
    folds: int = 10,
    seed: int = 0,
    spearman_brown: bool = True,
    equalize_halves: bool = True,
    clip_folds: bool = False,
) -> np.ndarray:
    """
    Nan-safe version of compute_ceiling_splithalf.
    Use this when responses contain NaN entries from QC masking.
    The key fixes are:
    1. np.nanmean instead of .mean() when averaging over repetitions
       within each half, so a single NaN rep does not corrupt the half-average.
    2. np.nanmean instead of .mean() for the centering step in Pearson r,
       so NaN stimuli do not propagate into the correlation.
    3. np.nanmean instead of .mean() when averaging fold results.
    """
    R = np.asarray(responses, dtype=np.float64)
    n_reps = R.shape[-1]
    half = n_reps // 2
    rng = np.random.default_rng(seed)

    fold_results = []
    for f in range(folds):
        idx = rng.permutation(n_reps)
        if equalize_halves:
            h1_idx = idx[:half]
            h2_idx = idx[half : 2 * half]
        else:
            h1_idx = idx[:half]
            h2_idx = idx[half:]

        # KEY FIX 1: nanmean over repetitions within each half
        h1 = np.nanmean(R[..., h1_idx], axis=-1)   # (..., n_stimuli)
        h2 = np.nanmean(R[..., h2_idx], axis=-1)

        # KEY FIX 2: nanmean for centering in Pearson r
        h1c = h1 - np.nanmean(h1, axis=-1, keepdims=True)
        h2c = h2 - np.nanmean(h2, axis=-1, keepdims=True)
        num = np.nansum(h1c * h2c, axis=-1)
        den = np.sqrt(np.nansum(h1c**2, axis=-1) * np.nansum(h2c**2, axis=-1)) + 1e-12
        r = num / den

        if spearman_brown:
            r = 2.0 * r / (1.0 + np.abs(r) + 1e-12)

        if clip_folds:
            r = np.clip(r, 0.0, 1.0)

        fold_results.append(r)

    # KEY FIX 3: nanmean across folds
    nc = np.nanmean(np.array(fold_results), axis=0)
    return np.clip(nc, 0.0, 1.0)

class RepresentationalSimilarityAnalysis:
    """
    Representational Similarity Analysis (RSA).

    Given two representation matrices X and Y with the same number of conditions
    (rows), RSA:
    1. Computes a Representational Dissimilarity Matrix (RDM) for each:
       RDM_X[i, j] = dissimilarity(x_i, x_j)
       RDM_Y[i, j] = dissimilarity(y_i, y_j)
    2. Flattens the upper triangles of both RDMs and computes a correlation
       between them (Pearson or Spearman).
    """

    def __init__(
        self,
        dissimilarity: Literal["correlation", "euclidean", "cosine"] = "correlation",
        similarity_metric: Literal["pearson", "spearman"] = "spearman",
    ):
        self.dissimilarity = dissimilarity
        self.similarity_metric = similarity_metric

    def __call__(self, X: np.ndarray, Y: np.ndarray) -> float:
        return self.forward(X, Y)

    def forward(self, X: np.ndarray, Y: np.ndarray) -> float:
        # flatten to (n_conditions, n_features)
        X = np.asarray(X, dtype=np.float64).reshape(X.shape[0], -1)
        Y = np.asarray(Y, dtype=np.float64).reshape(Y.shape[0], -1)

        rdm_x = self.compute_rdm(X)
        rdm_y = self.compute_rdm(Y)

        return self.compare_rdms(rdm_x, rdm_y)

    def compute_rdm(self, X: np.ndarray) -> np.ndarray:
        """
        Compute the Representational Dissimilarity Matrix (RDM)
        for a given representation matrix X.

        Parameters
        ----------
        X : np.ndarray
            Array of shape (n_conditions, n_features).

        Returns
        -------
        rdm : np.ndarray
            Array of shape (n_conditions, n_conditions) with pairwise dissimilarities.
        """
        # pdist computes upper triangle distances, squareform makes it symmetric
        return squareform(pdist(X, metric=self.dissimilarity))

    def compare_rdms(self, rdm1: np.ndarray, rdm2: np.ndarray) -> float:
        """
        Compare two RDMs by correlating their upper triangles.
        """
        # extract upper triangle indices (excluding diagonal)
        n = rdm1.shape[0]
        idx = np.triu_indices(n, k=1)
        vec1 = rdm1[idx]
        vec2 = rdm2[idx]

        if self.similarity_metric == "spearman":
            r, _ = stats.spearmanr(vec1, vec2)
        else:
            r, _ = stats.pearsonr(vec1, vec2)

        return float(r)

class CenteredKernelAlignment:
    """
    Unbiased linear CKA only.

    Parameters
    ----------
    eps : float
        Small constant for numerical stability.
    dtype : np.dtype
        Data type used for computations.
    """

    def __init__(
        self,
        eps: float = 1e-8,
        dtype: np.dtype = np.float64,
    ):
        self.eps = eps
        self.dtype = dtype

    def __call__(self, X: np.ndarray, Y: np.ndarray) -> float:
        return self.forward(X, Y)

    def forward(self, X: np.ndarray, Y: np.ndarray) -> float:
        X = np.asarray(X).astype(self.dtype)
        Y = np.asarray(Y).astype(self.dtype)

        if X.shape[0] != Y.shape[0]:
            raise ValueError(
                f"Batch sizes must match along axis 0: {X.shape[0]} vs {Y.shape[0]}"
            )

        # Flatten to (n_samples, n_features)
        X = X.reshape(X.shape[0], -1)
        Y = Y.reshape(Y.shape[0], -1)

        return self._unbiased_linear_cka(X, Y)

    def _unbiased_linear_hsic(self, X: np.ndarray, Y: np.ndarray) -> float:
        """
        Unbiased HSIC estimator for the linear kernel.

        Uses the U-statistic estimator from Song et al. (2012):
            HSIC_u(K, L) = 1/(n(n-3)) * [tr(KL) + 1'KL1/(n-1)(n-2)
                           - 2/(n-2) * 1'KL1]
        
        Simplified using the fact that for linear kernels K = XX', L = YY':
            HSIC_u(X, Y) = 1/(n(n-3)) * [||X'Y||_F^2 + (1'K1)(1'L1)/(n-1)(n-2)
                           - 2/(n-2) * sum_i (x_i'Y)(Y'x_i)]

        We use the cleaner formulation directly on the Gram matrices.

        X : [n, d_x]
        Y : [n, d_y]
        """
        n = X.shape[0]

        # Compute Gram matrices
        K = X @ X.T  # (n, n)
        L = Y @ Y.T  # (n, n)

        # Zero out diagonals for unbiased estimator
        np.fill_diagonal(K, 0)
        np.fill_diagonal(L, 0)

        # Unbiased HSIC estimator (Kornblith et al. 2019)
        KL = K @ L
        hsic = (
            np.trace(KL)
            + K.sum() * L.sum() / ((n - 1) * (n - 2))
            - 2 * KL.sum() / (n - 2)
        ) / (n * (n - 3))

        return float(hsic)

    def _unbiased_linear_cka(self, X: np.ndarray, Y: np.ndarray) -> float:
        """
        Unbiased linear CKA:
            CKA_unb(X, Y) =
                HSIC_unb(X, Y) / sqrt(HSIC_unb(X, X) * HSIC_unb(Y, Y))
        """
        hsic_xy = self._unbiased_linear_hsic(X, Y)
        hsic_xx = self._unbiased_linear_hsic(X, X)
        hsic_yy = self._unbiased_linear_hsic(Y, Y)

        denom = np.sqrt(hsic_xx * hsic_yy)
        return float(hsic_xy / (denom + self.eps))

def safe_normalize(feats):
    feats = np.asarray(feats, dtype=np.float64)
    norms = np.linalg.norm(feats, axis=1, keepdims=True)
    return feats / (norms + 1e-12)
