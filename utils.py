"""
Utility functions for the NX-414 brain-model alignment project.
Covers HDF5 inspection and stimulus-to-feature index matching.
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt

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
                           channel_threshold=0.10):
    
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
    ax.axvline(x=0, color="black", linewidth=1, linestyle="--", label="Stimulus onset")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Channel index (clean channels only)")
    ax.set_title(f"Mean EEG response — {subject} / {roi} (clean channels only)")
    plt.colorbar(im, ax=ax, label="Mean amplitude")
    ax.legend()
    plt.tight_layout()
    plt.show()