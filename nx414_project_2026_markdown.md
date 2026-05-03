<div style="background: linear-gradient(135deg, #e9f2fb 0%, #f7fbff 100%); padding: 18px 20px; border: 1px solid #d5e3f0; border-radius: 10px; text-align: center;">
  <div style="font-size: 32px; font-weight: 700; color: #1f3b57; letter-spacing: 0.2px;">NX-414 Brain-like Computation and Intelligence</div>
</div>


<div style="text-align: center; font-size: 21px; font-weight: 600; color: #36536b; margin-top: 6px;">Project Notebook — Spring 2026</div>


<div style="text-align: center; color: #4f6478; font-size: 16px; margin-bottom: 10px;">Brain–Model Alignment Across Neural Recording Modalities</div>
<div style="text-align: center; color: #6b7280; font-size: 13px;">Prepared by: Abdulkadir Gokce</div>

---


# Group Information

Fill in this section at the top of your notebook and report.

- **Group member 1:** Full name, SCIPER number, email address  
- **Group member 2:** Full name, SCIPER number, email address  
- **Group member 3 (if applicable):** Full name, SCIPER number, email address  

---

# What You Must Submit

Submit the following files:

1. **One Jupyter notebook** containing your full analysis.
2. **Any supporting Python scripts** needed to run the notebook.
3. **Figures that are part of your notebook answers** should be embedded and rendered in notebook Markdown.
4. **One PDF report** of **up to 2 pages**, **excluding references**, with **no appendix**.
5. **One zip archive** named exactly as:

```text
nx414_{SCIPER1}_{SCIPER2}_{SCIPER3}.zip
```

If your group has fewer than three members, reduce the number of `_SCIPER` fields accordingly.

## Submission Rules

- **Clear all notebook outputs before submission.**
- If outputs are not cleared, we will clear them ourselves and grade the cleaned notebook.
- Submit only the code required to reproduce your results.
- **Do not submit model weights.**
- **Do not submit CSV files or other large derived result dumps.**
- Keep the archive lightweight and reproducible.
- For the **final notebook**, any figure you want to present as part of your scientific argument should be **embedded in Markdown with accompanying interpretation**, rather than left as a raw cell output with no explanation.

Failure to follow these instructions may reduce your final grade.

## Use of LLMs

You may use LLM-based tools to help you write code, debug, or improve explanations. However, you remain fully responsible for the **correctness**, **quality**, and **clarity** of everything you submit, including both the notebook and the report.

In particular:

- check that any generated code actually runs and does what you claim it does,
- verify that any scientific statement or interpretation is correct,
- make sure the final writing sounds like a clear academic report written for this course,
- avoid vague, overly polished, or context-free text,
- avoid fancy wording or unnecessarily complex sentences that do not add clarity.

If you use an LLM, revise the output so that your submission reads naturally, is specific to your actual results, and does not look like generic generated text.

Failure to do so may result in **a point deduction**.

## Expected scope

Because this project spans roughly **three weeks** and counts for **30% of the final course grade**, the expected output is closer to a **compact course project** than to a one-week homework notebook. Your submission should therefore read like a small empirical study: it should be clearly structured, contain short written interpretations throughout, compare alternatives systematically, and end with a coherent synthesis of your main findings.

A strong notebook will not only run end-to-end, but will also explain **why** each analysis is being performed, what each metric is meant to capture, and what the results imply about the strengths and limitations of the models and datasets.

At the same time, **some parts of the project are intentionally left a bit loose**. This is by design: beyond implementing the required core analyses, you are expected to make reasonable scientific choices, justify them clearly, and show some ingenuity in how you explore the data and compare models.

## Suggested 3-week pacing

Use the notebook structure below to organize your work over the three weeks.

- **Week 1:** complete **Section 0** and **Section 1**. Understand the datasets, verify stimulus matching, inspect the processed responses, and start the visualization and reliability analyses.
- **Week 2:** complete the required analyses in **Section 2**. In this section, you must complete both the representational and predictive parts of the project. Begin **Section 3** by brainstorming possible extensions and sketching out a plan for your chosen extension.
- **Week 3:** complete **Section 3**, polish the notebook, select the strongest figures, and write the 2-page report.


---

# 0. Introduction and Setup

## 0.1 Project goal

In this project, you will study how neural responses from different recording modalities align with features extracted from two vision models. More specifically, you will work in the standard **brain–model alignment** setting: a model processes an image, a candidate internal layer is selected, and that representation is compared to measured neural responses using representational and predictive metrics.

The notebook is organized around four sections:

- **Section 0:** introduction, setup, and understanding the provided resources.
- **Section 1:** dataset inspection, visualization, and noise ceiling estimation.
- **Section 2:** brain–model alignment through both representational metrics and predictive linear models.
- **Section 3:** an open-ended extension beyond the baseline pipeline.

## 0.2 Why task-optimized models?

Task-optimized neural networks are among the most useful current **in-silico models of sensory cortex**. The central idea is simple: instead of hand-designing a model to mimic every biological detail, we optimize a model to perform a meaningful visual task and then ask whether its internal representations resemble those found in the brain. This approach has been highly influential because models trained to solve vision tasks often develop representations that predict activity along the visual hierarchy surprisingly well.

These models are useful scientifically because they provide **testable computational hypotheses**. If a model layer predicts neural responses well, that does not mean the brain literally implements the same mechanism, but it does suggest that the layer may encode information in a similar format or at a similar level of abstraction. Brain–model alignment is therefore a way to ask not just whether a model is accurate on a task, but whether it organizes visual information in a brain-relevant way.

## 0.3 Why compare multiple modalities?

A single recording modality gives only a partial view of neural computation. In this project, you will work with **electrophysiology, EEG, and fMRI**, which differ in temporal resolution, spatial resolution, and what exactly is measured. Looking across modalities helps you see which conclusions are robust and which depend on the measurement scale.

## 0.4 Learning goals

By the end of this project, you should be able to:

- inspect and summarize neural datasets from multiple modalities,
- visualize neural signals and data quality,
- implement and compare **two noise ceiling estimators**,
- implement **RSA** and **unbiased linear CKA**,
- fit **linear encoding models** from model features to neural responses,
- compare alignment across **models, layers, ROIs, and metrics**,
- interpret what each alignment metric captures,
- design and evaluate one meaningful extension beyond the baseline pipeline.

A strong submission should therefore demonstrate both **technical correctness** and **scientific reasoning**: beyond obtaining scores, you should be able to explain why a dataset is noisy, why one layer may outperform another, and why representational and predictive metrics sometimes disagree.

## 0.5 Provided data

All main data are stored in `/shared/NX-414/data/`.

### Background: processed data derivatives

The files provided for this project are **not raw neural recordings**. They are already processed, analysis-ready derivatives produced with modality-appropriate pipelines. This is important scientifically: many of your results will depend not only on the model features, but also on preprocessing choices such as repetition averaging, denoising, response-window selection, voxel/channel filtering, and how reliability is estimated.

We performed the preprocessing for you because these pipelines often require substantial modality-specific expertise, time, and compute.

At a high level, the datasets used here were prepared as follows:

- **TVSD (macaque electrophysiology)** — normalized multi-unit responses from ventral-stream areas. Responses were z-scored within session, firing rates were averaged in an analysis window centered on each site’s response peak, low-reliability channels were excluded, and repeated test responses were averaged for evaluation.
- **THINGS-EEG2 (human EEG)** — source EEG responses resampled to **100 Hz**. Noise ceilings were computed per subject, channel, and time point, and repetitions were averaged within train and test splits.
- **NSD (human fMRI)** — **b3 single-trial beta estimates** in `func1pt8mm` space, derived using voxel-wise HRF fitting, GLMdenoise, and ridge regression. Analyses are restricted to ROI-defined visually responsive voxels, low-reliability voxels are filtered out, and responses are averaged across available repetitions.

You are **not** expected to re-run the full preprocessing pipelines. You **are** expected to understand what kinds of neural quantities you are analyzing, what has already been averaged or denoised, and how these choices affect interpretation.

### Main neural datasets

- **`tvsd.h5`** — macaque electrophysiology from **2 monkeys**, with **22,248 train** and **100 test** stimuli, covering **V1, V4, and IT**.
- **`things_eeg2.h5`** — human EEG from **10 subjects**, with **16,540 train** and **200 test** stimuli, with region groupings such as **occipital**, **parietal**, **temporal**, **frontal**, **central**, **occipital_parietal**, and **whole_brain**.
- **`nsd_func1pt8mm_individualROIs.h5`** — human fMRI from **8 subjects**, with roughly **9,000 train** and **1,000 test** stimuli per subject, across multiple visual ROIs.

### Additional files

- `things_eeg2-test_reps.h5`  
  EEG test responses **with repetitions and without averaging**.  
  Use this file to implement and compare **two noise ceiling estimators**.

- `nsd-subj01-ncsnr-{lh,rh}.mgh`  
  Surface-based NSD reliability values for `subj-01` on **fsaverage**.  
  Use these to visualize cortical reliability and convert **ncsnr** into **noise ceiling**.

### Neural response shapes

- **TVSD:** `(n_stimuli, n_units)`
- **EEG2:** `(n_stimuli, n_channels, n_timepoints)`
- **NSD:** `(n_stimuli, n_voxels)`

For EEG, the time axis contains **80 time points** sampled at **100 Hz**, covering **0.0 s to 0.8 s**.

### Noise ceilings

Noise ceilings are stored per target:

- per neuron for **TVSD**,
- per channel × time point for **EEG2**,
- per voxel for **NSD**.

They are stored as **percent reliability**.  
To convert them to the range `[0, 1]`, divide by `100`.

In this project, the provided noise ceilings are mainly intended for **predictive metrics** such as **Pearson correlation** and **explained variance**. They reflect the reliability of the neural responses and therefore define an upper bound on how well any model can predict those responses.

When you compute predictive metrics, you should apply a noise ceiling correction to account for this upper bound. The standard idea is simple: divide the raw predictive score by the corresponding noise ceiling value for that target.

The provided noise ceilings are defined for **explained variance**. If you want to apply the same logic to **Pearson correlation**, first convert the explained-variance ceiling into a correlation ceiling by taking the element-wise square root, and then divide the raw correlation by that quantity. For a more detailed discussion of noise ceiling correction, see van Bree et al. (2025).

You may therefore report both **raw** and **noise-ceiling-corrected** predictive scores where appropriate.


For example, if the provided ceiling is an explained-variance reliability estimate, you can compute a noise-corrected Pearson correlation as:

```python
r_nc = r / np.sqrt(ev_ceiling)
```

where `r` is the raw Pearson correlation and `ev_ceiling` is the explained-variance ceiling expressed on the range `[0, 1]`.

By contrast, **RSA** and **CKA** should typically be reported as **raw values** in this project. Noise ceilings for representational similarity metrics require a different methodology and are **not** provided here.


Do **not** apply this correction directly to **RSA** or **CKA**.

### Stimulus identifiers

- **TVSD / EEG2:** byte strings such as `b'aardvark/aardvark_01b.jpg'`
- **NSD:** integer stimulus IDs

## 0.6 Model features

All extracted features are stored in `/shared/NX-414/extracted_features/`.

The feature files contain **internal activations extracted from multiple candidate layers** while the models process the same images shown in the neural experiments. You can think of each layer as a representation matrix of shape roughly **stimuli × features**. These layer-wise representations are what you will compare to the brain using RSA, CKA, and encoding models.

Feature extractions across models were made tractable by projecting activations to **30,000 dimensions** using a random projection. The provided feature files follow that same idea. In practice, this means you can treat the feature vectors as compact surrogates for the original activations while still performing meaningful alignment analyses.

### Model A: `adv_resnet152_imagenet_full_ffgsm_eps-1_alpha-125-ep10_seed-0`

- Architecture: **ResNet-152**
- Pretraining: ImageNet + adversarial fine-tuning
- Available feature files:
  - `things_stimuli.h5`
  - `nsd_stimuli.h5`

### Model B: `Qwen3-VL-2B-Instruct`

- Architecture: **vision-language transformer**
- Available feature files:
  - `things_stimuli.h5`
  - `nsd_stimuli.h5`

For both models, layers have been projected to **30,000 dimensions** using random projections.

### Feature extraction note

For this project, feature extraction has already been done for you. Your job is therefore not to run the vision models on raw images, but to understand **which layer** to use, how to match feature rows to neural stimuli, and what different layers reveal about representational hierarchy.

### Important note for NSD

For NSD, the feature files contain features for **all 73,000 images**, but each subject saw only a subset (~9,000).  
You must therefore select feature rows using the subject-specific NSD stimulus IDs.

## 0.7 Matching features to neural responses

You must match neural responses and features through the stimulus IDs.

### THINGS-based datasets: TVSD and EEG2

For these datasets, both neural IDs and feature IDs are byte strings. Matching should therefore be exact.

### NSD

For NSD, both sides use integer IDs. The feature file contains all 73,000 stimuli, while each subject has only a subset. Use the subject-specific NSD stimulus IDs to select the corresponding feature rows.

### Recommended procedure

```python
feat_ids = feature_file['ids'][:]
id_to_feat_idx = {id_: i for i, id_ in enumerate(feat_ids)}
feat_idx = np.array([id_to_feat_idx[x] for x in neural_ids])
```

To make HDF5 reads efficient:

1. build the index array,
2. sort indices before reading,
3. load only the required rows,
4. restore the original order.

## 0.8 General analysis rules

### Train/test discipline

Do **not** use the test split for model selection or hyperparameter tuning. Use a validation split or cross-validation within the training data.

### EEG targets

For EEG, you may either:

- flatten the targets to `(n_stimuli, n_channels * n_timepoints)`, or
- fit separate models per channel × time point.

Either choice is acceptable, but you must explain your decision clearly.

### Predictive metrics

Report the following predictive metrics where appropriate:

- `pearsonr`
- `pearsonr_nc`
- `explained_variance`
- `explained_variance_nc`

The provided EEG signals are not filtered like the other datasets. As a result, some low-reliability channels or time points can produce unstable predictive scores. When averaging predictive metrics over EEG targets, apply an on-the-fly filter such as **noise ceiling < 0.1**.

### Representational metrics

Also report:

- `RSA`
- `CKA`
- `encoding-RSA`
- `encoding-CKA`

Encoding RSA/CKA is a hybrid metric where you compute RSA or CKA between the predicted neural responses (from the linear encoding model) and the actual neural responses, instead of just comparing model activation directly. This can help you understand whether the linear encoding model captures the representational geometry of the neural data, beyond just predicting individual response values. You can refer to Conwell et al. (2024) for more details on this approach. 

Use only the test split for computing representational metrics.

Do **not** noise-correct RSA or CKA using the predictive-metric procedure.

## 0.9 Setup and data loading

Your notebook should begin with a short introduction, clear imports, utility functions, and a brief verification that the provided files are correctly organized and matched.

**Section 0 is required but not graded separately.** It is treated as setup for the rest of the project. Missing or incorrect setup may reduce scores in later sections if it affects correctness or reproducibility.

<div style="background:#eef5fb; border-left:4px solid #4c78a8; padding:8px 12px; border-radius:6px; font-weight:700; color:#26445e;">What you must do</div>

- Import the required packages.
- Define utility functions.
- Load metadata for all datasets.
- Inspect the structure of each `.h5` file.
- Load feature metadata for both models.
- Verify that feature IDs and neural stimulus IDs match.

<div style="background:#f3f6fa; border-left:4px solid #7a93ac; padding:8px 12px; border-radius:6px; font-weight:700; color:#32475b;">Required deliverables</div>

You must include all of the following:

1. **Dataset and feature overview:** one compact table or printed summary covering all neural datasets and both feature sets.
2. **Stimulus-matching verification:** explicit checks or assertions showing that stimulus matching works for THINGS-based datasets and for NSD.
3. **Short structural summary:** a short written note describing the main structural differences across datasets.

<div style="background:#eef8f4; border-left:4px solid #5b9a7a; padding:8px 12px; border-radius:6px; font-weight:700; color:#285943;">Questions you should answer</div>

- How many stimuli are available in each dataset?
- What is the shape of the neural response tensor in each dataset?
- Which datasets contain subjects, ROIs, repetitions, channels, or time points?
- What are the feature dimensionalities across layers?

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 0</strong><br>Summarize the structure of the three datasets and the two feature sets in 4–6 sentences. Clearly state which dataset is most complex structurally and why.</div>

# TODO


```python
# TODO: imports
# TODO: define paths
# TODO: inspect dataset structure
# TODO: verify stimulus matching
```


```python
%load_ext autoreload
%autoreload 2

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from tqdm.auto import tqdm
import h5py
import nibabel as nib
from nilearn import plotting as nlplt
from sklearn.linear_model import Ridge # TODO: be careful with sklearn
from sklearn import metrics
import torch
import warnings
warnings.filterwarnings('ignore')
# helper functions
from utils import *

# Reproducibility
SEED = 42
np.random.seed(SEED)

print("All imports OK")
```

---

# 1. Inspection, Visualization, and Noise Ceiling Estimates

This section is about understanding the data before doing model comparison. By the end of it, you should have a clear sense of how each modality is organized, which signals appear reliable, and how the provided reliability estimates relate to your own computations.

## 1.1 Inspect the datasets

<div style="background:#eef5fb; border-left:4px solid #4c78a8; padding:8px 12px; border-radius:6px; font-weight:700; color:#26445e;">What you must do</div>

- Inspect the content and axis meaning of TVSD, EEG2, and NSD.
- Identify where subject IDs, ROI labels, time axes, stimulus IDs, and noise ceilings are stored.
- State clearly what each axis means for each response array.

<div style="background:#f3f6fa; border-left:4px solid #7a93ac; padding:8px 12px; border-radius:6px; font-weight:700; color:#32475b;">Required deliverables</div>

You must include all of the following:

1. **TVSD structure table**
2. **EEG2 structure table**
3. **NSD structure table**

Each table must list the array name, array shape, and the meaning of each axis.


```python
# TODO: inspect TVSD
# TODO: inspect EEG2
# TODO: inspect NSD
# TODO: summarize axis meaning
```


```python
from pathlib import Path

DATA_DIR    = Path("/shared/NX-414/data")
FEAT_DIR    = Path("/shared/NX-414/extracted_features")

# --- Neural data files ---
TVSD_PATH      = DATA_DIR / "tvsd.h5"
EEG_PATH       = DATA_DIR / "things_eeg2.h5"
EEG_REPS_PATH  = DATA_DIR / "things_eeg2-test_reps.h5"
NSD_PATH       = DATA_DIR / "nsd_func1pt8mm_individualROIs.h5"
NSD_NCSNR_LH   = DATA_DIR / "nsd-subj01-ncsnr-lh.mgh"
NSD_NCSNR_RH   = DATA_DIR / "nsd-subj01-ncsnr-rh.mgh"

# --- Model feature directories ---
MODEL_A_NAME = "adv_resnet152_imagenet_full_ffgsm_eps-1_alpha-125-ep10_seed-0"
MODEL_B_NAME = "Qwen3-VL-2B-Instruct"

FEAT_A_THINGS = FEAT_DIR / MODEL_A_NAME / "things_stimuli.h5"
FEAT_A_NSD    = FEAT_DIR / MODEL_A_NAME / "nsd_stimuli.h5"
FEAT_B_THINGS = FEAT_DIR / MODEL_B_NAME / "things_stimuli.h5"
FEAT_B_NSD    = FEAT_DIR / MODEL_B_NAME / "nsd_stimuli.h5"

# Sanity check — all files should exist
all_paths = {
    "tvsd":          TVSD_PATH,
    "eeg":           EEG_PATH,
    "eeg_reps":      EEG_REPS_PATH,
    "nsd":           NSD_PATH,
    "nsd_ncsnr_lh":  NSD_NCSNR_LH,
    "nsd_ncsnr_rh":  NSD_NCSNR_RH,
    "feat_A_things": FEAT_A_THINGS,
    "feat_A_nsd":    FEAT_A_NSD,
    "feat_B_things": FEAT_B_THINGS,
    "feat_B_nsd":    FEAT_B_NSD,
}
for name, p in all_paths.items():
    status = "✓" if p.exists() else "✗ MISSING"
    print(f"  {status}  {name}: {p}")
```

#### TVSD dataset structure


```python
print("=" * 55)
print("TVSD (macaque electrophysiology)")
print("=" * 55)
inspect_h5(TVSD_PATH, max_depth = 4) # adjusted to 4 to confirm shapes from "Neural response shapes" section
```

**Explanation:**

- The TVSD dataset is organized by monkey (monkeyF and N) and brain region (IT, V1, V4).
- Neural responses are stored as 2D arrays of shape (n_stimuli, n_units)
- Rows correspond positionally to stimulus_ids such that we can match each recording a certain stimulus
- Noise ceilings are stored per unit / neuron as 1D arrays of shape (n_units,); this matches the second axis of the neural data
- dataset is pre-split into 22,248 training and 100 test stimuli.

**Some notes:**
- although the splits between the datasets are not equal, resplitting to get a more reliable final performance estimate on the test set is probably not advisable as splitting requires domain knowledge and deep knowledge of the dataset to not leak information from train to test (could be achieved by us) but also noise ceilings would have to be recomputed, etc. Probably the test set is carefully chosen by the authors. Further, other papers probably use the proposed split so we'd lose comparibility.
- When we do cross - validation, we must ensure that no stimulus indices appear in both the train and validation folds!

Check whether reponses are averaged repetitions or the same stimulus_ids appear multiple times per participant


```python
with h5py.File(TVSD_PATH, "r") as f:
    train_ids = f["train/stimulus_ids"][:]

n_total = len(train_ids)
n_unique = len(set(train_ids))
print(f"Total: {n_total}, Unique: {n_unique}")
```

#### THINGS-EEG (human EEG) dataset structure


```python
print("\n" + "=" * 55)
print("THINGS-EEG2 (human EEG)")
print("=" * 55)
inspect_h5(EEG_PATH, max_depth = 4) # again depth = 4 for more details
```

Check whether reponses are averaged repetitions or the same stimulus_ids appear multiple times per participant


```python
with h5py.File(EEG_PATH, "r") as f:
    train_ids = f["train/stimulus_ids"][:]

n_total = len(train_ids)
n_unique = len(set(train_ids))
print(f"Total: {n_total}, Unique: {n_unique}")
```

Data already averaged across the 4 repetitions

Stimulus IDs serve as a shared key between the neural recordings and the model feature files. Since we may only extract model features for a subset of all available images, we cannot rely on row indices alone and must match explicitly through the IDs. This is especially critical for NSD, where the feature file contains activations for all 73,000 images but each subject only saw roughly 9,000 of them.

**Explanation:**

- The THINGS-EEG2 dataset is organized by subject (sub-01 through sub-10) and brain region (occipital, parietal, temporal, frontal, central, occipital_parietal, whole_brain).
- Neural responses are stored as 3D arrays of shape (n_stimuli, n_channels, n_timepoints), where n_timepoints=80 covering 0–0.8s at 100Hz.
- Rows correspond positionally to stimulus_ids, which are shared across all subjects — all 10 subjects saw the exact same stimuli in the same order.
- Noise ceilings are stored per channel×timepoint as 2D arrays of shape (n_channels, 80), reflecting that reliability varies across both space and time.
- There are two noise ceiling groups: noise_ceilings/ computed from test repetitions (80 reps, reliable) and noise_ceilings_train/ computed from training repetitions (4 reps, noisier).
- The dataset is pre-split into 16,540 training and 200 test stimuli. Training responses are already averaged across the 4 repetitions (confirmed: all stimulus IDs are unique).

**Some notes:**

- have to discuss whether to use this noisy noise ceiling (haha) when using cross-validation. Claude was unsure whether it makes sense, thus, read papers maybe or ask TA

#### NSD (human fMRI) dataset


```python
print("\n" + "=" * 55)
print("NSD (human fMRI)")
print("=" * 55)
inspect_h5(NSD_PATH, max_depth=3)
```


```python
with h5py.File(NSD_PATH, "r") as f:
    mask_nc = f["roi_labels_nc/subj01/V1v"][:]
    nc      = f["noise_ceilings/subj01/V1v"][:]

print(f"roi_labels_nc True count: {mask_nc.sum()}")
print(f"noise_ceilings length:    {len(nc)}")
```

**Explanation:**
- The NSD dataset is organized by subject (subj01–subj08) and ROI. Unlike EEG2, each subject has
  their own stimulus IDs since different subjects saw different subsets of the 73,000 COCO images.
- Neural responses are stored as 2D arrays of shape `(n_stimuli, n_voxels)` per subject per ROI,
  where rows correspond positionally to that subject's stimulus IDs.
- Not all subjects completed the same number of sessions, so the number of stimuli varies across subjects.

**Understanding the spatial structure:**
- `roi_labels/` stores 3D boolean masks marking which voxels belong to each anatomical ROI.
- `roi_labels_nc/` stores the same kind of mask but only for voxels actually included in the 1D
  neural data and noise ceiling arrays. This is the critical mapping — without it you cannot know
  which voxels correspond to which entries in the 1D arrays.
- `noise_ceilings/` stores noise ceiling values as 1D arrays corresponding exactly to the `True`
  positions in `roi_labels_nc/`. We verified this: the length of `noise_ceilings/subj01/V1v`
  matches exactly the number of `True` values in `roi_labels_nc/subj01/V1v`.

**Some notes:**
- Stimulus IDs are integers (COCO image IDs) and differ per subject — we must use each subject's own stimulus IDs to select the correct rows from the feature file.
- Some ROIs may have zero voxels for certain subjects (e.g. subj02/FBA-1), and should be skipped when encountered.

### Verify stimulus matching: THINGS-based datasets (TVSD & EEG2)

(THINGS = image dataset used for visual stimuli in those two experiments/datasets)


```python
# ---- TVSD ----
with h5py.File(TVSD_PATH, "r") as f:
    tvsd_train_ids = f["train/stimulus_ids"][:]
    tvsd_test_ids  = f["test/stimulus_ids"][:]

tvsd_feat_idx = build_id_index(FEAT_A_THINGS)

missing_train = [x for x in tvsd_train_ids if x not in tvsd_feat_idx]
missing_test  = [x for x in tvsd_test_ids  if x not in tvsd_feat_idx]

assert len(missing_train) == 0, f"TVSD train: {len(missing_train)} IDs missing"
assert len(missing_test)  == 0, f"TVSD test:  {len(missing_test)}  IDs missing"
print(f"TVSD ✓  train={len(tvsd_train_ids):,}  test={len(tvsd_test_ids):,}  all matched")

# ---- EEG2 ----
with h5py.File(EEG_PATH, "r") as f:
    eeg_train_ids = f["train/stimulus_ids"][:]
    eeg_test_ids  = f["test/stimulus_ids"][:]

missing_train = [x for x in eeg_train_ids if x not in tvsd_feat_idx]
missing_test  = [x for x in eeg_test_ids  if x not in tvsd_feat_idx]

assert len(missing_train) == 0, f"EEG train: {len(missing_train)} IDs missing"
assert len(missing_test)  == 0, f"EEG test:  {len(missing_test)}  IDs missing"
print(f"EEG2 ✓  train={len(eeg_train_ids):,}  test={len(eeg_test_ids):,}  all matched")
```

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 1.1</strong><br>Explain the main differences between the three modalities in terms of what is being measured and how the data are organized.</div>

The three datasets differ fundamentally in what they measure and how they are organized.

**TVSD** records multi-unit spiking activity (MUA) from macaque visual cortex using chronically 
implanted Utah arrays — 1,024 microelectrodes spread across V1, V4, and IT in two animals [[2]](#papale2025). 
MUA aggregates spiking from multiple neurons near each electrode tip, sampled at 30 kHz. This 
gives exceptional temporal resolution: response windows of 25–125ms for V1, 50–150ms for V4, 
and 75–175ms for IT already reflect the known latency gradient along the visual hierarchy. 
Within the implanted regions, spatial resolution is on the order of hundreds of micrometers. 
The data are organized as 2D arrays (n_stimuli × n_units) per monkey per region, with no time 
axis since responses are already averaged within the analysis window.

**THINGS-EEG2** records scalp EEG from 10 human subjects using non-invasive electrode caps [[3]](#gifford2022). 
EEG provides full cortical coverage but poor spatial resolution due to volume conduction: the 
electrical signal spreads through skull and tissue before reaching the electrodes, blurring the 
spatial origin of the signal. Deep brain structures contribute minimally. Temporal resolution is 
good — the raw signal was sampled at 1 kHz and downsampled to 100 Hz for the provided data, 
though the 100 Hz is a preprocessing choice rather than a hardware limit. The data are organized 
as 3D arrays (n_stimuli × n_channels × n_timepoints), preserving the full temporal dynamics. 
Regions are defined anatomically by source location (occipital, parietal, temporal, frontal) 
rather than by functional visual area as in TVSD.

**NSD** records BOLD fMRI responses from 8 human subjects at 7T with 1.8mm voxel resolution [[4]](#allen2022). 
BOLD is a hemodynamic signal reflecting changes in the ratio of oxygenated to deoxygenated 
hemoglobin that follow neural activity with a substantial delay. The hemodynamic response peaks 
roughly 5–6 seconds after the neural event [[1]](#liao2002), and the brief initial dip in oxygenated 
hemoglobin that immediately follows neural firing is generally too small to reliably detect, 
meaning the measurable signal is dominated by the delayed overshoot of oxygenated blood flow. 
The 7T field strength was chosen specifically to maximize SNR over standard 3T scanners. Data 
are organized as 2D arrays (n_stimuli × n_voxels) per subject per ROI, where ROIs correspond 
to well-characterized functional visual areas (V1, V2, V3, hV4, FFA, PPA, etc.). Each subject 
has a different number of voxels per ROI due to individual brain anatomy, and stimulus IDs 
differ per subject since each saw a different subset of the 73,000 COCO images.

In summary, TVSD offers the highest temporal and spatial precision but is invasive, limited to 
macaques, and covers only a few targeted regions. EEG2 captures full-brain temporal dynamics 
non-invasively in humans but with poor spatial resolution. NSD provides the richest spatial 
picture of the human visual system at the cost of temporal resolution and an indirect 
hemodynamic signal. Together, the three modalities offer complementary views of the visual 
system that no single recording technique could provide alone.

**Data organization:**

TVSD is organized by monkey (monkeyF, monkeyN) and region (V1, V4, IT). Neural responses are 
stored as 2D arrays of shape `(n_stimuli, n_units)`, where the stimulus axis is aligned 
positionally to the stimulus ID array of shape `(n_stimuli,)`, meaning row $i$ of the neural 
data corresponds to stimulus $i$ of the ID array. Noise ceilings are stored as 1D arrays of 
shape `(n_units,)`, matching the second axis of the neural data exactly. The dataset is 
pre-split into 22,248 training and 100 test stimuli, shared across both monkeys.

THINGS-EEG2 is organized by subject (sub-01 through sub-10) and anatomical region (occipital, 
parietal, temporal, frontal, central, occipital_parietal, whole_brain). Neural responses are 
stored as 3D arrays of shape `(n_stimuli, n_channels, n_timepoints)`, where n_timepoints = 80 
covering 0–0.8s at 100 Hz. Noise ceilings are stored as 2D arrays of shape 
`(n_channels, n_timepoints)`, reflecting that reliability varies across both space and time. 
Two sets of noise ceilings are provided: `noise_ceilings/` computed from the 80 test 
repetitions and `noise_ceilings_train/` computed from the 4 training repetitions. Training 
responses are already averaged across repetitions (confirmed by all 16,540 training stimulus 
IDs being unique). The stimulus ID arrays of shape `(n_stimuli,)` are shared across all subjects 
since every subject saw the same images in the same order. The dataset is pre-split into 16,540 
training and 200 test stimuli.

NSD is organized by subject (subj01 through subj08) and ROI. Neural responses are stored as 2D 
arrays of shape `(n_stimuli, n_voxels)` per subject per ROI, positionally aligned to that 
subject's stimulus ID array. The number of stimuli and voxels varies across subjects due to 
differences in the number of completed sessions and individual brain anatomy. Two spatial 
structures are important here. `roi_labels/` stores 3D boolean masks of the full brain volume 
marking the anatomical extent of each ROI. `roi_labels_nc/` stores a refined version of this 
mask containing only the voxels that pass a reliability criterion. These are exactly the 
voxels included in the 1D neural data and noise ceiling arrays, confirmed by matching counts. 
Without `roi_labels_nc/` it is not possible to map the 1D arrays back to brain space. Noise 
ceilings are stored as 1D arrays of shape `(n_voxels,)` per subject per ROI, matching the 
second axis of the neural data. Stimulus IDs are integers (COCO image IDs) and differ per 
subject since each subject saw a different subset of the full 73,000-image pool.

## References

<a id="liao2002"></a>[1] C.-H. Liao, K. J. Worsley, J.-B. Poline, J. A. D. Aston, G. H. Duncan, and A. C. Evans, "Estimating the delay of the fMRI response," *NeuroImage*, vol. 16, no. 3, pp. 593–606, 2002.

<a id="papale2025"></a>[2] P. Papale, F. Wang, M. W. Self, and P. R. Roelfsema, "An extensive dataset of spiking activity to reveal the syntax of the ventral stream," *Neuron*, vol. 113, no. 4, pp. 539–553, 2025.

<a id="gifford2022"></a>[3] A. T. Gifford, K. Dwivedi, G. Roig, and R. M. Cichy, "A large and rich EEG dataset for modeling human visual object recognition," *NeuroImage*, vol. 264, p. 119754, 2022.

<a id="allen2022"></a>[4] E. J. Allen, G. St-Yves, Y. Wu, J. L. Breedlove, J. S. Prince, L. T. Dowdle, M. Nau, B. Caron, F. Pestilli, I. Charest, et al., "A massive 7T fMRI dataset to bridge cognitive neuroscience and artificial intelligence," *Nature Neuroscience*, vol. 25, no. 1, pp. 116–126, 2022.

---

## 1.2 Visualize EEG signals

<div style="background:#eef5fb; border-left:4px solid #4c78a8; padding:8px 12px; border-radius:6px; font-weight:700; color:#26445e;">What you must do</div>

- Plot example EEG responses for several stimuli and channels.
- Plot average responses over time for at least one subject and one ROI.
- Visualize the provided EEG noise ceilings over channels and time.

To detect potentially dead or degraded channels, we compute the variance of each 0.8s epoch 
across the 80 timepoints, giving one quality value per (stimulus, channel) pair. We then 
average these values within blocks of 200 consecutive stimuli to reduce noise and produce a 
readable summary. The resulting heatmap has stimulus blocks on the y-axis (a proxy for time 
in the experiment) and channels on the x-axis. A uniformly dark column indicates a dead 
channel throughout the recording, while a column that transitions from bright to dark suggests 
a channel that degraded at some point during the experiment.


```python
# ---- Block-averaged channel quality heatmap ----
BLOCK_SIZE = 200
SUBJECT    = "sub-01"
ROI        = "whole_brain"

with h5py.File(EEG_PATH, "r") as f:
    # shape: (16540, n_channels, 80)
    train_data = f[f"train/neural_data/{SUBJECT}/{ROI}"][:]

n_stimuli, n_channels, n_timepoints = train_data.shape
n_blocks = n_stimuli // BLOCK_SIZE

# For each stimulus, compute variance over the 80 timepoints -> (n_stimuli, n_channels)
epoch_var = train_data.var(axis=2)

# Average within blocks -> (n_blocks, n_channels)
epoch_var_blocked = epoch_var[:n_blocks * BLOCK_SIZE].reshape(n_blocks, BLOCK_SIZE, n_channels).mean(axis=1)
# Z-score each channel across blocks
channel_mean = epoch_var_blocked.mean(axis=0)
channel_std  = epoch_var_blocked.std(axis=0)
epoch_var_blocked_norm = (epoch_var_blocked - channel_mean) / (channel_std + 1e-8)

# Plot
fig, ax = plt.subplots(figsize=(14, 6))
im = ax.imshow(epoch_var_blocked_norm , aspect="auto", cmap="viridis",
               interpolation="nearest")
ax.set_xlabel("Channel index")
ax.set_ylabel(f"Stimulus block (each = {BLOCK_SIZE} stimuli)")
ax.set_title(f"Block-averaged epoch variance — {SUBJECT} / {ROI}")
plt.colorbar(im, ax=ax, label="Normalized variance (relative to channel mean)")
plt.tight_layout()
plt.show()
```


```python
import ipywidgets as widgets
from IPython.display import display

# ---- Block-averaged channel quality heatmap ----
BLOCK_SIZE = 200
SUBJECT    = "sub-01"
ROI        = "whole_brain"

with h5py.File(EEG_PATH, "r") as f:
    train_data = f[f"train/neural_data/{SUBJECT}/{ROI}"][:]

n_stimuli, n_channels, n_timepoints = train_data.shape
n_blocks = n_stimuli // BLOCK_SIZE

# For each stimulus, compute variance over the 80 timepoints -> (n_stimuli, n_channels)
epoch_var = train_data.var(axis=2)

# Average within blocks -> (n_blocks, n_channels)
epoch_var_blocked = epoch_var[:n_blocks * BLOCK_SIZE].reshape(n_blocks, BLOCK_SIZE, n_channels).mean(axis=1)

# Z-score each channel across blocks
channel_mean = epoch_var_blocked.mean(axis=0)
channel_std  = epoch_var_blocked.std(axis=0)
epoch_var_blocked_norm = (epoch_var_blocked - channel_mean) / (channel_std + 1e-8)

def plot_threshold(threshold):
    fig, ax = plt.subplots(figsize=(14, 6))
    mask = (epoch_var_blocked_norm < threshold).astype(float)
    im = ax.imshow(mask, aspect="auto", cmap="RdYlGn_r",
                   interpolation="nearest", vmin=0, vmax=1)
    ax.set_xlabel("Channel index")
    ax.set_ylabel(f"Stimulus block (each = {BLOCK_SIZE} stimuli)")
    ax.set_title(f"Dead channel detection (threshold={threshold:.2f}) — {SUBJECT} / {ROI}")
    plt.colorbar(im, ax=ax, label="0 = OK, 1 = dead/degraded")
    plt.tight_layout()
    plt.show()

slider = widgets.FloatSlider(
    value=-1.5, min=-3.0, max=0.0, step=0.1,
    description="Threshold:",
    continuous_update=False,
    style={"description_width": "initial"}
)

widgets.interact(plot_threshold, threshold=slider)
```


```python
import ipywidgets as widgets
from IPython.display import display

n_examples = 5

# Compute normalization statistics across ALL stimuli (do this once)
with h5py.File(EEG_PATH, "r") as f:
    all_data = f[f"train/neural_data/{SUBJECT}/{ROI}"][:]

# Variance per stimulus -> (n_stimuli, n_channels)
epoch_var_all = all_data.var(axis=2)

# Statistics across all stimuli per channel
stim_mean = epoch_var_all.mean(axis=0)  # (n_channels,)
stim_std  = epoch_var_all.std(axis=0)   # (n_channels,)

def plot_channel_block_detail(block_idx, channel_idx, stim_offset):
    start = block_idx * BLOCK_SIZE
    end   = start + BLOCK_SIZE
    
    # Load this block
    data_block = all_data[start:end]  # (BLOCK_SIZE, n_channels, 80)
    
    # Variance per stimulus -> (BLOCK_SIZE, n_channels)
    var_block = data_block.var(axis=2)
    
    # Z-score using global statistics
    var_block_norm = (var_block - stim_mean) / (stim_std + 1e-8)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    
    # Left: heatmap of all stimuli in this block x all channels
    im = axes[0].imshow(var_block_norm, aspect="auto", cmap="viridis",
                        interpolation="nearest")
    axes[0].axvline(x=channel_idx, color="red", linewidth=1.5, 
                    label=f"Channel {channel_idx}")
    # Horizontal bars showing which stimuli are plotted on the right
    axes[0].axhline(y=stim_offset,             color="orange", linewidth=1.5, linestyle="--")
    axes[0].axhline(y=stim_offset + n_examples - 1, color="orange", linewidth=1.5, 
                    linestyle="--", label=f"Stimuli shown on right")
    axes[0].set_xlabel("Channel index")
    axes[0].set_ylabel("Stimulus index within block")
    axes[0].set_title(f"Z-scored variance — block {block_idx} (stimuli {start}–{end})")
    axes[0].legend(fontsize=8)
    plt.colorbar(im, ax=axes[0], label="Z-scored variance")
    
    # Right: time courses of selected channel for n_examples stimuli
    time_axis  = np.linspace(0, 0.8, n_timepoints)
    for i in range(n_examples):
        stim_in_block = stim_offset + i
        axes[1].plot(time_axis, data_block[stim_in_block, channel_idx, :],
                     alpha=0.7, label=f"Stimulus {start + stim_in_block}")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Amplitude")
    axes[1].set_title(f"Time courses — channel {channel_idx}, block {block_idx}")
    axes[1].legend(fontsize=8)
    
    plt.tight_layout()
    plt.show()

n_examples = 5

block_slider = widgets.IntSlider(
    value=0, min=0, max=n_blocks - 1, step=1,
    description="Block index:",
    continuous_update=False,
    style={"description_width": "initial"}
)
channel_slider = widgets.IntSlider(
    value=0, min=0, max=n_channels - 1, step=1,
    description="Channel index:",
    continuous_update=False,
    style={"description_width": "initial"}
)
stim_slider = widgets.IntSlider(
    value=0, min=0, max=BLOCK_SIZE - n_examples, step=1,
    description="Stimulus offset:",
    continuous_update=False,
    style={"description_width": "initial"}
)

widgets.interact(plot_channel_block_detail, 
                 block_idx=block_slider, 
                 channel_idx=channel_slider,
                 stim_offset=stim_slider)
```

Log scale


```python
import ipywidgets as widgets
from IPython.display import display
import matplotlib.colors as mcolors

n_examples = 5

# Compute normalization statistics across ALL stimuli (do this once)
with h5py.File(EEG_PATH, "r") as f:
    all_data = f[f"train/neural_data/{SUBJECT}/{ROI}"][:]

# Variance per stimulus -> (n_stimuli, n_channels)
epoch_var_all = all_data.var(axis=2)

# Statistics across all stimuli per channel
stim_mean = epoch_var_all.mean(axis=0)  # (n_channels,)
stim_std  = epoch_var_all.std(axis=0)   # (n_channels,)

def plot_channel_block_detail(block_idx, channel_idx, stim_offset):
    start = block_idx * BLOCK_SIZE
    end   = start + BLOCK_SIZE
    
    # Load this block
    data_block = all_data[start:end]  # (BLOCK_SIZE, n_channels, 80)
    
    # Variance per stimulus -> (BLOCK_SIZE, n_channels)
    var_block = data_block.var(axis=2)
    
    # Z-score using global statistics
    var_block_norm = (var_block - stim_mean) / (stim_std + 1e-8)

    print(f"Z-scores for shown stimuli (channel {channel_idx}):")
    for i in range(n_examples):
        stim_in_block = stim_offset + i
        z = var_block_norm[stim_in_block, channel_idx]
        print(f"  Stimulus {start + stim_in_block}: z = {z:.2f}")
        
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    
    # Left: heatmap of all stimuli in this block x all channels
    im = axes[0].imshow(var_block_norm, aspect="auto", cmap="viridis",
                    interpolation="nearest",
                    norm=mcolors.SymLogNorm(linthresh=1))
    axes[0].axvline(x=channel_idx, color="red", linewidth=1.5, 
                    label=f"Channel {channel_idx}")
    # Horizontal bars showing which stimuli are plotted on the right
    axes[0].axhline(y=stim_offset,             color="orange", linewidth=1.5, linestyle="--")
    axes[0].axhline(y=stim_offset + n_examples - 1, color="orange", linewidth=1.5, 
                    linestyle="--", label=f"Stimuli shown on right")
    axes[0].set_xlabel("Channel index")
    axes[0].set_ylabel("Stimulus index within block")
    axes[0].set_title(f"Z-scored variance — block {block_idx} (stimuli {start}–{end})")
    axes[0].legend(fontsize=8)
    plt.colorbar(im, ax=axes[0], label="Z-scored variance")
    
    # Right: time courses of selected channel for n_examples stimuli
    time_axis  = np.linspace(0, 0.8, n_timepoints)
    for i in range(n_examples):
        stim_in_block = stim_offset + i
        axes[1].plot(time_axis, data_block[stim_in_block, channel_idx, :],
                     alpha=0.7, label=f"Stimulus {start + stim_in_block}")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Amplitude")
    axes[1].set_title(f"Time courses — channel {channel_idx}, block {block_idx}")
    axes[1].legend(fontsize=8)
    
    plt.tight_layout()
    plt.show()

n_examples = 5

block_slider = widgets.IntSlider(
    value=0, min=0, max=n_blocks - 1, step=1,
    description="Block index:",
    continuous_update=False,
    style={"description_width": "initial"}
)
channel_slider = widgets.IntSlider(
    value=0, min=0, max=n_channels - 1, step=1,
    description="Channel index:",
    continuous_update=False,
    style={"description_width": "initial"}
)
stim_slider = widgets.IntSlider(
    value=0, min=0, max=BLOCK_SIZE - n_examples, step=1,
    description="Stimulus offset:",
    continuous_update=False,
    style={"description_width": "initial"}
)

widgets.interact(plot_channel_block_detail, 
                 block_idx=block_slider, 
                 channel_idx=channel_slider,
                 stim_offset=stim_slider)
```


```python
# Z-score all stimuli using global statistics
epoch_var_norm_all = (epoch_var_all - stim_mean) / (stim_std + 1e-8)  # (n_stimuli, n_channels)

THRESHOLD = 2.5

fig, axes = plt.subplots(1, 2, figsize=(16, 4))

# Linear y-scale
axes[0].hist(epoch_var_norm_all.flatten(), bins=200, color="steelblue", edgecolor="none")
axes[0].axvline(x=THRESHOLD, color="red", linewidth=2, label=f"Threshold τ={THRESHOLD}")
axes[0].set_xlabel("Z-score")
axes[0].set_ylabel("Count")
axes[0].set_title(f"Z-score distribution — {SUBJECT} / {ROI}")
axes[0].legend()

# Log y-scale
axes[1].hist(epoch_var_norm_all.flatten(), bins=200, color="steelblue", edgecolor="none")
axes[1].axvline(x=THRESHOLD, color="red", linewidth=2, label=f"Threshold τ={THRESHOLD}")
axes[1].set_yscale("log")
axes[1].set_xlabel("Z-score")
axes[1].set_ylabel("Count (log scale)")
axes[1].set_title(f"Z-score distribution (log y) — {SUBJECT} / {ROI}")
axes[1].legend()

plt.tight_layout()
plt.show()

# Print fraction flagged
n_flagged = (epoch_var_norm_all > THRESHOLD).sum()
n_total   = epoch_var_norm_all.size
print(f"Flagged: {n_flagged} / {n_total} ({100 * n_flagged / n_total:.2f}%)")
```


```python
# Max absolute value per stimulus per channel
max_abs_all = np.abs(all_data).max(axis=2)  # (n_stimuli, n_channels)

THRESHOLD_ABS = 50

fig, axes = plt.subplots(1, 2, figsize=(16, 4))

# Linear y-scale
axes[0].hist(max_abs_all.flatten(), bins=200, color="steelblue", edgecolor="none")
axes[0].axvline(x=THRESHOLD_ABS, color="red", linewidth=2, label=f"Threshold={THRESHOLD_ABS}")
axes[0].set_xlabel("Max absolute amplitude")
axes[0].set_ylabel("Count")
axes[0].set_title(f"Max absolute amplitude distribution — {SUBJECT} / {ROI}")
axes[0].legend()

# Log y-scale
axes[1].hist(max_abs_all.flatten(), bins=200, color="steelblue", edgecolor="none")
axes[1].axvline(x=THRESHOLD_ABS, color="red", linewidth=2, label=f"Threshold={THRESHOLD_ABS}")
axes[1].set_yscale("log")
axes[1].set_xlabel("Max absolute amplitude")
axes[1].set_ylabel("Count (log scale)")
axes[1].set_title(f"Max absolute amplitude distribution (log y) — {SUBJECT} / {ROI}")
axes[1].legend()

plt.tight_layout()
plt.show()

# Print fraction flagged
n_flagged = (max_abs_all > THRESHOLD_ABS).sum()
n_total   = max_abs_all.size
print(f"Flagged: {n_flagged} / {n_total} ({100 * n_flagged / n_total:.2f}%)")
```


```python
# Apply z-score filter first
zscore_mask = epoch_var_norm_all > THRESHOLD  # (n_stimuli, n_channels), True = flagged

# Get max abs values for unflagged stimuli only
max_abs_filtered = max_abs_all.copy()
max_abs_filtered[zscore_mask] = np.nan  # mask out z-score flagged pairs

fig, axes = plt.subplots(1, 2, figsize=(16, 4))

# Linear y-scale
axes[0].hist(max_abs_filtered[~zscore_mask].flatten(), bins=100, 
             color="steelblue", edgecolor="none")
axes[0].axvline(x=THRESHOLD_ABS, color="red", linewidth=2, 
                label=f"Threshold={THRESHOLD_ABS}")
axes[0].set_xlabel("Max absolute amplitude")
axes[0].set_ylabel("Count")
axes[0].set_title(f"Max absolute amplitude (after z-score filter) — {SUBJECT} / {ROI}")
axes[0].legend()

# Log y-scale
axes[1].hist(max_abs_filtered[~zscore_mask].flatten(), bins=100, 
             color="steelblue", edgecolor="none")
axes[1].axvline(x=THRESHOLD_ABS, color="red", linewidth=2, 
                label=f"Threshold={THRESHOLD_ABS}")
axes[1].set_yscale("log")
axes[1].set_xlabel("Max absolute amplitude")
axes[1].set_ylabel("Count (log scale)")
axes[1].set_title(f"Max absolute amplitude (after z-score filter, log y) — {SUBJECT} / {ROI}")
axes[1].legend()

plt.tight_layout()
plt.show()

# Print fractions
n_remaining = (~zscore_mask).sum()
n_flagged_abs = (max_abs_filtered[~zscore_mask] > THRESHOLD_ABS).sum()
print(f"After z-score filter: {n_remaining:,} / {max_abs_all.size:,} pairs remaining")
print(f"Additionally flagged by amplitude: {n_flagged_abs} ({100 * n_flagged_abs / n_remaining:.2f}% of remaining)")
```


```python
# Combined quality mask
# True = flagged as bad (either high variance or extreme amplitude)
quality_mask = zscore_mask | (max_abs_all > THRESHOLD_ABS)  # (n_stimuli, n_channels)

n_flagged_total = quality_mask.sum()
n_total         = quality_mask.size
n_flagged_z     = zscore_mask.sum()
n_flagged_amp   = (max_abs_all > THRESHOLD_ABS).sum()
n_flagged_both  = (zscore_mask & (max_abs_all > THRESHOLD_ABS)).sum()

print(f"Total stimulus-channel pairs:        {n_total:,}")
print(f"Flagged by z-score (τ={THRESHOLD}):    {n_flagged_z:,} ({100 * n_flagged_z / n_total:.2f}%)")
print(f"Flagged by amplitude (>{THRESHOLD_ABS}): {n_flagged_amp:,} ({100 * n_flagged_amp / n_total:.2f}%)")
print(f"Flagged by both:                     {n_flagged_both:,} ({100 * n_flagged_both / n_total:.2f}%)")
print(f"Flagged by either (total):           {n_flagged_total:,} ({100 * n_flagged_total / n_total:.2f}%)")
print(f"Remaining clean pairs:               {n_total - n_flagged_total:,} ({100 * (1 - n_flagged_total / n_total):.2f}%)")
```

### EEG data quality assessment

Before analyzing the EEG responses, we first assessed the recording quality. We expected three 
types of problematic channels: dead channels with near-zero variance producing no meaningful 
signal, channels with unusually high variance caused by movement artifacts or equipment noise, 
and channels that drift over time showing a slowly changing baseline. A drifting channel also 
produces high variance since the drift itself contributes to signal variability. One limitation 
of variance-based detection is that mean shifts — where a channel is displaced to a very 
different amplitude but remains stable — are not directly detectable, which motivated our 
second amplitude-based filter described below.

With 16,540 training stimuli per subject, inspecting every stimulus-channel pair individually 
is not feasible. We therefore grouped stimuli into blocks of 200 consecutive stimuli, using 
block index as a proxy for time in the experiment. For each stimulus we computed the variance 
over the 80 timepoints of the 0.8s epoch, giving one quality value per stimulus-channel pair, 
which was then averaged within each block to produce a matrix of shape 
$(n_{\text{blocks}}, n_{\text{channels}})$.

To make differences visible across channels with very different natural amplitudes, we applied 
z-score normalization per channel using statistics computed across all stimuli. This was 
necessary because channels vary considerably in amplitude — some consistently show values in 
the $\pm 30$ range while others stay within $\pm 5$. Using raw variance would make the 
colorscale dominated by high-amplitude channels, hiding degradation in quieter ones. The 
z-score instead shows relative changes within each channel compared to its own baseline.

The blocked heatmap provided a useful first overview but turned out to be somewhat hard to 
interpret on its own, as averaging over 200 stimuli smooths out individual artifacts. We 
therefore built an interactive tool to inspect individual blocks at full stimulus resolution 
using a symmetric log scale to handle the wide dynamic range of z-score values. This revealed 
that certain channels showed recurring problems, particularly channels 13 and 53. These 
appeared as mostly flat columns in the heatmap with occasional extreme values.

Inspecting the actual time courses confirmed this: stimulus 7144 (sub-01, channel 13) showed 
a signal starting at $-200$, drifting to $-100$, then jumping to $+600$ within a single 0.8s 
epoch. Stimulus 7140 showed similar behavior, jumping between $-600$, $+100$ and $-550$.
For comparison, channel 43 over the same stimuli showed clean, stable responses typical of a 
good channel.

<div style="display: flex; gap: 10px; align-items: flex-start;">
  <figure style="text-align: center;">
    <img src="images/stimulus_7139_7143_ch_13_z_score.png" width="800"/>
    <figcaption>Channel 13 (anomalous) — stimuli 7139–7143</figcaption>
  </figure>
  <figure style="text-align: center;">
    <img src="images/stimulus_7139_7143_ch_43_z_score.png" width="800"/>
    <figcaption>Channel 43 (normal) — stimuli 7139–7143</figcaption>
  </figure>
</div>

### Automated quality control

To systematically identify faulty stimulus-channel pairs, we applied two complementary filters.

The first filter is based on the z-scored variance. For each stimulus and channel, we computed 
the variance over the 80 timepoints of the 0.8s epoch, then z-scored it using the mean and 
standard deviation computed across all 16,540 training stimuli for that channel:

$$z_{i,c} = \frac{\text{var}_{i,c} - \mu_c}{\sigma_c}$$

A high positive z-score indicates that the epoch was unusually variable compared to the 
channel's typical behavior. Based on visual inspection of individual time courses, z-scores 
above ~3 were clearly artifactual while z-scores below ~1.3 appeared normal. We set the 
threshold at $\tau = 2.5$, conservatively between these values, flagging 2.11% of all 
stimulus-channel pairs.

The second filter targets extreme amplitude values that the variance filter can miss. A channel 
that shifts to a very different baseline but remains stable will have low variance and pass the 
z-score filter undetected. We therefore also flag any stimulus-channel pair where the maximum 
absolute amplitude exceeds 50. This value was chosen by inspecting the amplitude distribution, 
which shows the vast majority of epochs well below this threshold. After applying the z-score 
filter first, the amplitude filter flags an additional 0.54% of remaining pairs, confirming 
that the two criteria are complementary rather than redundant.

The combined mask flags roughly 2.65% of all stimulus-channel pairs as faulty. We note that 
no persistently dead channels were found during visual inspection, suggesting that the 
preprocessing and source reconstruction pipeline had already removed the most severely 
degraded channels before we received the data. The secondary bump visible in the amplitude 
distribution around 750 to 1000 is worth noting — it may reflect a specific recurring artifact 
type rather than random noise, though we did not investigate it further.

The choice of both thresholds involves a tradeoff. Setting them too low risks discarding valid 
responses, while setting them too high risks keeping corrupted ones. For encoding model 
analyses, we prefer to err on the side of exclusion since a missing channel causes less harm 
than a corrupted one influencing the fit. The thresholds were chosen based on visual inspection 
rather than a formal criterion, as neither distribution showed a clear natural gap that would 
justify a principled cutoff.

<div style="display: flex; gap: 10px; align-items: flex-start;">
  <figure style="text-align: center;">
    <img src="images/z-score-distribution.png" width="800"/>
    <figcaption>Z-score distribution across all stimulus-channel pairs</figcaption>
  </figure>
  <figure style="text-align: center;">
    <img src="images/max_abs_distribution.png" width="800"/>
    <figcaption>Max absolute amplitude distribution</figcaption>
  </figure>
</div>

### Quality control across all subjects

The quality control analysis above was performed on sub-01. We now repeat it for all 10 
subjects using the same thresholds ($\tau = 2.5$ for z-score, 50 for max absolute amplitude) 
to check whether the thresholds generalize and whether data quality is consistent across 
subjects.

The z-score threshold is self-normalizing by construction — since it is computed relative to 
each channel's own mean and standard deviation, the same threshold should produce comparable 
flagging rates across subjects regardless of their absolute signal levels. The amplitude 
threshold of 50 is less principled in this regard, since subjects may differ in their overall 
response amplitude due to inter-subject variability in source reconstruction, cortical 
geometry, or signal-to-noise ratio. One alternative would be to use a subject-specific 
percentile threshold (e.g. flag the top 1% of amplitude values per subject), which adapts 
to each subject's own distribution while flagging a consistent fraction. However, this assumes 
the same fraction of data is artifactual in every subject, which is not necessarily true 
either. We therefore first apply the fixed threshold of 50 to all subjects and inspect the 
resulting flagged percentages. If the percentages are consistent across subjects, the fixed 
threshold is adequate. If a subject shows a dramatically different flagging rate, we will 
consider switching to a percentile-based threshold for that subject.


```python
subjects = [f"sub-{i:02d}" for i in range(1, 11)]
results = []

for subj in subjects:
    with h5py.File(EEG_PATH, "r") as f:
        data = f[f"train/neural_data/{subj}/{ROI}"][:]
    
    n_stim, n_ch, n_tp = data.shape
    
    # Variance-based z-score
    ep_var = data.var(axis=2)
    s_mean = ep_var.mean(axis=0)
    s_std  = ep_var.std(axis=0)
    ep_var_norm = (ep_var - s_mean) / (s_std + 1e-8)
    
    # Amplitude-based
    max_abs = np.abs(data).max(axis=2)
    
    # Combined mask
    mask = (ep_var_norm > THRESHOLD) | (max_abs > THRESHOLD_ABS)
    
    pct_z   = (ep_var_norm > THRESHOLD).mean() * 100
    pct_amp = (max_abs > THRESHOLD_ABS).mean() * 100
    pct_tot = mask.mean() * 100
    
    results.append({
        "Subject":           subj,
        "Z-score flagged %": round(pct_z, 2),
        "Amplitude flagged %": round(pct_amp, 2),
        "Total flagged %":   round(pct_tot, 2),
        "Clean pairs %":     round(100 - pct_tot, 2),
    })
    
    print(f"{subj}: z={pct_z:.2f}%  amp={pct_amp:.2f}%  total={pct_tot:.2f}%")

results_df = pd.DataFrame(results).set_index("Subject")
results_df
```


```python
percentile_50 = (max_abs_all < 50).mean() * 100
print(f"Threshold of 50 corresponds to the {percentile_50:.2f}th percentile for sub-01")
```


```python
subjects = [f"sub-{i:02d}" for i in range(1, 11)]
results = []

for subj in subjects:
    with h5py.File(EEG_PATH, "r") as f:
        data = f[f"train/neural_data/{subj}/{ROI}"][:]
    
    n_stim, n_ch, n_tp = data.shape
    
    # Variance-based z-score
    ep_var = data.var(axis=2)
    s_mean = ep_var.mean(axis=0)
    s_std  = ep_var.std(axis=0)
    ep_var_norm = (ep_var - s_mean) / (s_std + 1e-8)
    
    # Amplitude-based — subject-specific percentile threshold
    max_abs = np.abs(data).max(axis=2)
    THRESHOLD_ABS = np.percentile(max_abs, percentile_50)
    
    # Combined mask
    mask = (ep_var_norm > THRESHOLD) | (max_abs > THRESHOLD_ABS)
    
    pct_z   = (ep_var_norm > THRESHOLD).mean() * 100
    pct_amp = (max_abs > THRESHOLD_ABS).mean() * 100
    pct_tot = mask.mean() * 100
    
    results.append({
        "Subject":             subj,
        "Amp threshold":       round(THRESHOLD_ABS, 2),
        "Z-score flagged %":   round(pct_z, 2),
        "Amplitude flagged %": round(pct_amp, 2),
        "Total flagged %":     round(pct_tot, 2),
        "Clean pairs %":       round(100 - pct_tot, 2),
    })
    
    print(f"{subj}: amp_threshold={THRESHOLD_ABS:.1f}  z={pct_z:.2f}%  amp={pct_amp:.2f}%  total={pct_tot:.2f}%")

results_df = pd.DataFrame(results).set_index("Subject")
results_df
```

### Quality control on test repetitions

The noise ceilings provided in `noise_ceilings/` are computed from the 80 test repetitions. If individual test repetitions are anomalous — due to movement 
artifacts, electrode drift, or equipment issues — they will directly corrupt the noise ceiling 
estimate for the affected channel×timepoint combinations. It is therefore important to also 
assess data quality in the test repetitions.

Unlike the training data where repetitions were already averaged before storage, the test 
repetitions file (`things_eeg2-test_reps.h5`) preserves all 80 repetitions individually, 
with shape `(n_stimuli, n_channels, n_repetitions, n_timepoints)`. This actually gives us 
more control — a single bad repetition out of 80 can be cleanly excluded without affecting 
the remaining 79, whereas in the training data a bad repetition is baked into the average 
and cannot be recovered.

We apply the same two quality filters as before — z-score on epoch variance and max absolute 
amplitude — now at the level of individual repetitions. The z-score is computed per channel 
across all stimulus-repetition combinations, and the amplitude threshold uses the same 
percentile as derived for sub-01 in the training data. This flagged 0.91% of all 
stimulus-channel-repetition triples, lower than the 2.6% seen in training. However the two 
numbers are not directly comparable since training quality control was applied to averaged 
responses while here we operate on individual repetitions. The lower rate likely reflects 
both the smaller size of the test set and the fact that averaging dilutes but does not 
remove bad epochs in the training data.

The provided noise ceilings were computed before this quality control step and therefore 
may include a small fraction of anomalous repetitions. Given the low flagging rate (0.91%), 
the impact on the noise ceiling estimates is expected to be minimal. In Section 1.3 we will 
implement our own noise ceiling estimators using the cleaned test repetitions, which will 
allow a direct comparison to the provided ceilings.


```python
SUBJECT = "sub-01"
ROI     = "whole_brain"

with h5py.File(EEG_REPS_PATH, "r") as f:
    test_data = f[f"test/neural_data/{SUBJECT}/{ROI}"][:]
    # shape: (200, 63, 80, 80) -> (n_stimuli, n_channels, n_reps, n_timepoints)

n_stim, n_ch, n_reps, n_tp = test_data.shape

# Variance over timepoints for each (stimulus, channel, rep)
ep_var_test = test_data.var(axis=3)  # (200, 63, 80)

# Z-score per channel across all stimulus-rep combinations
ep_var_flat = ep_var_test.reshape(n_stim * n_reps, n_ch)  # (16000, 63)
s_mean_test = ep_var_flat.mean(axis=0)  # (63,)
s_std_test  = ep_var_flat.std(axis=0)   # (63,)
ep_var_norm_test = (ep_var_test - s_mean_test[None, :, None]) / (s_std_test[None, :, None] + 1e-8)

# Max absolute amplitude per (stimulus, channel, rep)
max_abs_test = np.abs(test_data).max(axis=3)  # (200, 63, 80)
thresh_abs_test = np.percentile(max_abs_test, percentile_50)

# Quality mask: True = flagged
quality_mask_test = (ep_var_norm_test > THRESHOLD) | (max_abs_test > thresh_abs_test)

n_flagged = quality_mask_test.sum()
n_total   = quality_mask_test.size
print(f"Flagged: {n_flagged} / {n_total} ({100 * n_flagged / n_total:.2f}%)")
```

Text TODO


```python
# ---- Heatmap of mean EEG response over channels x time (cleaned) ----

# Identify channels that are anomalous overall
# A channel is considered anomalous if more than 10% of its stimuli are flagged
flagged_per_channel = quality_mask.mean(axis=0)  # (n_channels,)
CHANNEL_THRESHOLD = 0.10
clean_channels = flagged_per_channel < CHANNEL_THRESHOLD
print(f"Clean channels: {clean_channels.sum()} / {n_channels} "
      f"({100 * clean_channels.mean():.1f}%)")

# Average over clean stimuli per channel, respecting the quality mask
clean_mean = np.zeros((n_channels, n_timepoints))
for ch in range(n_channels):
    clean_stimuli = ~quality_mask[:, ch]
    clean_mean[ch] = all_data[clean_stimuli, ch, :].mean(axis=0)

# Only keep clean channels for the heatmap
clean_mean_filtered = clean_mean[clean_channels]
time_axis = np.linspace(0, 0.8, n_timepoints)

fig, ax = plt.subplots(figsize=(12, 6))
im = ax.imshow(clean_mean_filtered, aspect="auto", cmap="RdBu_r",
               interpolation="nearest",
               extent=[0, 0.8, clean_mean_filtered.shape[0], 0])
ax.axvline(x=0, color="black", linewidth=1, linestyle="--", label="Stimulus onset")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Channel index (clean channels only)")
ax.set_title(f"Mean EEG response — {SUBJECT} / {ROI} (clean channels only)")
plt.colorbar(im, ax=ax, label="Mean amplitude")
ax.legend()
plt.tight_layout()
plt.show()
```


```python
import importlib
import utils
importlib.reload(utils)
from utils import *

subjects = ["sub-01", "sub-02", "sub-03", "sub-04"]

for roi in ["whole_brain","occipital", "occipital_parietal", "temporal", "frontal"]:
    for subj in subjects:
        plot_mean_eeg_heatmap(EEG_PATH, subj, roi)
```


```python
import importlib
import utils
importlib.reload(utils)
from utils import *

subjects = ["sub-01", "sub-02", "sub-03", "sub-04", "sub-05", "sub-06", "sub-07", "sub-08", "sub-09", "sub-10"]

for roi in ["occipital"]:
    for subj in subjects:
        plot_mean_eeg_heatmap(EEG_PATH, subj, roi)
```


```python
subjects = ["sub-01", "sub-02", "sub-03"]
for roi in ["whole_brain", "occipital"]:
    for subj in subjects:
        save_path = f"images/eeg_heatmap_{roi}_{subj.replace('-', '')}.png"
        plot_mean_eeg_heatmap(EEG_PATH, subj, roi, save_path=save_path)
```

### EEG signal visualization

To get a first impression of the EEG data quality and structure, we plotted the mean response 
across all clean training stimuli for each channel over the 0.8s post-stimulus window. Each 
epoch is time-locked to a stimulus onset, though due to the RSVP paradigm with a 200ms SOA, 
the later timepoints of each epoch are contaminated by responses to subsequent images. The 
repeating pattern of evoked responses every ~200ms visible in the heatmaps directly reflects 
this — each peak corresponds to the onset of a new image in the rapid sequence.

We show results for the `whole_brain` ROI (all 63 channels) and the `occipital` ROI (3 
channels) for subjects 01, 02, and 03. The `occipital` region is particularly relevant for 
visual processing as it overlies primary visual cortex (V1) and surrounding early visual 
areas [[cite]](#cite).

<div style="display: flex; gap: 10px;">
  <figure style="text-align: center;">
    <img src="images/eeg_heatmap_whole_brain_sub01.png" style="width: 100%;"/>
    <figcaption>sub-01 / whole_brain</figcaption>
  </figure>
  <figure style="text-align: center;">
    <img src="images/eeg_heatmap_whole_brain_sub02.png" style="width: 100%;"/>
    <figcaption>sub-02 / whole_brain</figcaption>
  </figure>
  <figure style="text-align: center;">
    <img src="images/eeg_heatmap_whole_brain_sub03.png" style="width: 100%;"/>
    <figcaption>sub-03 / whole_brain</figcaption>
  </figure>
</div>

<div style="display: flex; gap: 10px; margin-top: 15px;">
  <figure style="text-align: center;">
    <img src="images/eeg_heatmap_occipital_sub01.png" style="width: 100%;"/>
    <figcaption>sub-01 / occipital</figcaption>
  </figure>
  <figure style="text-align: center;">
    <img src="images/eeg_heatmap_occipital_sub02.png" style="width: 100%;"/>
    <figcaption>sub-02 / occipital</figcaption>
  </figure>
  <figure style="text-align: center;">
    <img src="images/eeg_heatmap_occipital_sub03.png" style="width: 100%;"/>
    <figcaption>sub-03 / occipital</figcaption>
  </figure>
</div>

**What we observe:**

Looking at the `whole_brain` heatmaps, the absolute amplitudes and overall color patterns 
differ across subjects — sub-01 shows a mix of positive and negative responses while sub-02 
is dominated by negative values. This inter-subject variability in absolute amplitude is 
expected given individual differences in skull thickness, electrode impedance, and cortical 
geometry. Despite these differences, two features are consistent across subjects: channel 30 
shows a persistent positive mean across the entire 0.8s window in all three subjects, 
suggesting this reflects a systematic property of that electrode's position or the online 
referencing to Fz rather than a subject-specific artifact. Additionally, the repeating 
pattern of elevated activity every ~200ms is visible in all subjects, directly reflecting 
the RSVP stimulus onsets.

In the `occipital` ROI, the temporal structure becomes much clearer. Sub-02 shows highly 
consistent responses across all three occipital channels, with clear peaks at approximately 
0.1s, 0.3s, 0.5s, and 0.7s after stimulus onset. Sub-01 shows a similar pattern but with 
more variability across channels — channel 2 consistently shows lower amplitude than channels 
1 and 3. Sub-03 shows an interesting temporal shift: the response peaks appear approximately 
50ms earlier (at ~0.05s, 0.25s, 0.45s, and 0.65s) compared to the other subjects. This 
pattern was also observed in subjects 05, 06, and 10, suggesting it may reflect a 
subgroup difference in neural response latency or a difference in how the data was processed 
for those subjects. The cause of this shift is currently unclear.

Despite the inter-subject variability, the consistent temporal structure across subjects — 
particularly the clear evoked responses in occipital channels — confirms that the data 
contains meaningful stimulus-driven signal rather than pure noise.


```python
# Load and average noise ceilings across all subjects for whole_brain
roi      = "whole_brain"
subjects = [f"sub-{i:02d}" for i in range(1, 11)]

nc_all = []
with h5py.File(EEG_PATH, "r") as f:
    for subj in subjects:
        nc = f[f"noise_ceilings/{subj}/{roi}"][:]  # (n_channels, 80)
        nc_all.append(nc)

nc_mean = np.mean(nc_all, axis=0) / 100  # (n_channels, 80), convert to [0,1]

fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# Heatmap over channels x time
im = axes[0].imshow(nc_mean, aspect="auto", cmap="viridis",
                    interpolation="nearest",
                    extent=[0, 0.8, nc_mean.shape[0], 0],
                    vmin=0, vmax=1)
axes[0].set_xlabel("Time (s)")
axes[0].set_ylabel("Channel index")
axes[0].set_title(f"Mean noise ceiling — {roi} (averaged across subjects)")
plt.colorbar(im, ax=axes[0], label="Noise ceiling [0, 1]")

# Mean over channels per timepoint
time_axis = np.linspace(0, 0.8, 80)
axes[1].plot(time_axis, nc_mean.mean(axis=0), color="steelblue", linewidth=2)
axes[1].fill_between(time_axis, 
                      nc_mean.mean(axis=0) - nc_mean.std(axis=0),
                      nc_mean.mean(axis=0) + nc_mean.std(axis=0),
                      alpha=0.3, color="steelblue", label="±1 std across channels")
axes[1].set_xlabel("Time (s)")
axes[1].set_ylabel("Noise ceiling [0, 1]")
axes[1].set_title(f"Mean noise ceiling over time — {roi}")
axes[1].legend()

plt.tight_layout()
plt.savefig("images/noise_ceiling_heatmap_whole_brain.png", dpi=150, bbox_inches="tight")
plt.show()
```

### Provided EEG noise ceilings

The noise ceilings provided in `noise_ceilings/` were computed on the 80 test repetitions and reflect how consistently each channel responds to the same 
image across repetitions. A high noise ceiling at a given channel×timepoint means the 
response there is strongly driven by the stimulus — the brain produces a reliable, 
reproducible signal for that image. A low noise ceiling means the response is not well 
explained by the stimulus, either because the channel is noisy or because it is engaged 
in processes unrelated to the visual task (attention, internal state, default mode activity) 
that vary across repetitions.

We averaged the noise ceilings across all 10 subjects and visualized them as a heatmap over 
channels × time, alongside the mean noise ceiling over time averaged across channels.

<div style="display: flex; gap: 10px;">
  <figure style="text-align: center;">
    <img src="images/noise_ceiling_heatmap_whole_brain.png" style="width: 100%;"/>
    <figcaption>Mean noise ceiling across subjects — whole_brain</figcaption>
  </figure>
</div>

Several patterns are immediately visible. First, the channels with the highest noise ceilings 
(around indices 15-20 and 45-50) are exactly the same channels that showed the strongest 
evoked responses in the mean EEG heatmap. This is a clean validation of the noise ceiling 
concept — the channels most reliably driven by the visual stimulus are the ones with the 
highest theoretical upper bound on model prediction accuracy. Channels with low noise ceilings 
are not simply noisy; they are engaged in processes that our vision models cannot and should 
not be expected to predict.

Second, the noise ceiling is highest in the first 400ms after stimulus onset and drops 
steeply afterwards. This aligns with the neural habituation effect described in the original 
paper [[3]](#gifford2022) — responses to successive images in a rapid sequence diminish over 
time, making later timepoints less reliable. The noise ceiling plateau between roughly 0.1s 
and 0.4s suggests that the brain's response to the first image in the sequence remains 
reliable across multiple stages of visual processing, capturing both early sensory responses 
and later higher-level processing. After 0.4s — corresponding approximately to when the 
third image in the sequence appears — habituation becomes strong enough that responses 
lose their stimulus-specificity and the noise ceiling drops sharply.

Third, the large standard deviation across channels visible in the line plot confirms that 
channels differ substantially in how stimulus-driven they are. This further motivates our 
earlier decision to filter out low-reliability channel×timepoint pairs when computing 
predictive metrics in Section 2 (noise ceiling < 0.1 as specified in the project guidelines).

<div style="background:#f3f6fa; border-left:4px solid #7a93ac; padding:8px 12px; border-radius:6px; font-weight:700; color:#32475b;">Required deliverables</div>

You must include all of the following:

1. **One plot of example EEG time courses** for several stimuli and channels.
2. **One heatmap over channels × time** for at least one subject and one ROI.
3. **One summary plot of the provided EEG noise ceilings**.
4. **One short written interpretation** in Answer box 1.2.

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 1.2</strong><br>Which time windows and channel groups appear most informative? Are the responses dominated by noise, or do you observe clear evoked structure?</div>

**Answer box 1.2**

The most informative time window is roughly 0.1s to 0.4s after stimulus onset, where both 
the evoked responses and noise ceilings are highest. Within this window, the first 200ms 
captures the primary visual response to each image before contamination from the next image 
in the RSVP sequence becomes dominant. Channel groups around indices 15-20 and 45-50 are 
consistently the most informative across subjects, showing the strongest evoked responses 
and highest noise ceilings — these are likely the visually responsive electrodes overlying 
occipital and parietal cortex. Frontal and central channels show much weaker stimulus-driven 
responses and lower noise ceilings, suggesting they are engaged in processes unrelated to 
the visual task.

The responses are not dominated by noise — there is clear evoked structure that is 
consistent across subjects and repeats every ~200ms in line with the RSVP stimulus onsets. 
However, the RSVP paradigm introduces substantial forward contamination: from 200ms onwards, 
each epoch contains overlapping responses to subsequent images, making later timepoints 
harder to interpret as stimulus-specific. The occipital region shows particularly clean 
evoked structure with responses peaking around 100ms post-stimulus, consistent with known 
latencies of early visual cortex responses.


```python
# TODO: load one EEG subject / ROI
# TODO: plot example traces
# TODO: plot channel x time heatmap
# TODO: visualize provided EEG noise ceilings
```

---

## 1.3 Estimate EEG noise ceilings using two methods

In practice, there are multiple ways to estimate noise ceilings, depending on the available data and the specific research question. When you have repeated measurements of the same stimulus, you can estimate reliability from the consistency of those repetitions. When repeated measurements are not available, reliability can instead be estimated across subjects, which often yields a more conservative ceiling.

In this part, you will implement two different estimators using the `things_eeg2-test_reps.h5` file, which contains the unaveraged test responses with repetitions.

You must implement **two different estimators** using `things_eeg2-test_reps.h5`. You can refer to the cited paper in each method's docstring for details.



```python
import numpy as np
import h5py
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
from tqdm.auto import tqdm
```

### Required estimators

1. **Variance-based estimator**  
2. **Split-half reliability estimator**

<div style="background:#eef5fb; border-left:4px solid #4c78a8; padding:8px 12px; border-radius:6px; font-weight:700; color:#26445e;">What you must do</div>

- Implement both estimators.
- Compute both estimators for EEG2.
- Compare them to the provided EEG noise ceilings stored in `things_eeg2.h5`.

<div style="background:#f3f6fa; border-left:4px solid #7a93ac; padding:8px 12px; border-radius:6px; font-weight:700; color:#32475b;">Required deliverables</div>

You must include all of the following:

1. **Working implementation of the variance-based estimator**
2. **Working implementation of the split-half estimator**
3. **One plot of mean noise ceiling over time**
4. **One plot of mean noise ceiling over channels**
5. **At least one channel × time heatmap for each estimator**
6. **At least one histogram comparing the value distributions**
7. **One direct visual comparison to the stored EEG noise ceilings**

### Starter functions


```python
import importlib
import utils
importlib.reload(utils)
from utils import *
```


```python
SUBJECT = "sub-01"
ROI     = "whole_brain"

with h5py.File(EEG_REPS_PATH, "r") as f:
    reps_raw = f["test"]["neural_data"][SUBJECT][ROI][:]
    print("Raw reps shape:", reps_raw.shape)  # (200, ch, 80, 80)

# Axes: (stim, ch, tp, reps) → transpose to (ch, tp, stim, reps)
reps = reps_raw.transpose(1, 2, 0, 3).astype(np.float32)
print("Transposed shape (ch, tp, stim, reps):", reps.shape)

n_ch, n_tp, n_stim, n_reps = reps.shape
times = np.linspace(0.0, 0.8, n_tp)
```


```python
print("Computing variance-based ceiling …")
nc_vb = compute_ceiling_variancebased(reps)          # (ch, tp) in percent
print("  shape:", nc_vb.shape, " range: %.1f – %.1f" % (np.nanmin(nc_vb), np.nanmax(nc_vb)))
 
print("Computing split-half ceiling …")
nc_sh = compute_ceiling_splithalf(reps, folds=10, seed=0)  # (ch, tp) in [0,1]
nc_sh_pct = nc_sh * 100.0                                   # convert to percent
print("  shape:", nc_sh_pct.shape, " range: %.1f – %.1f" % (np.nanmin(nc_sh_pct), np.nanmax(nc_sh_pct)))
 
# Load provided ceiling from things_eeg2.h5 for comparison
with h5py.File(EEG_PATH, "r") as f:
    nc_stored = f["noise_ceilings"][SUBJECT][ROI][:]
    print("Stored ceiling shape:", nc_stored.shape,
          " range: %.1f – %.1f" % (nc_stored.min(), nc_stored.max()))
```


```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=False)
 
for ax, nc, label, color in zip(
    axes,
    [nc_vb,      nc_sh_pct,  nc_stored],
    ["Variance-based", "Split-half", "Provided"],
    ["steelblue", "darkorange", "forestgreen"],
):
    mean_over_ch = np.nanmean(nc, axis=0)   # (tp,)
    sem          = np.nanstd(nc, axis=0) / np.sqrt(nc.shape[0])
    ax.fill_between(times, mean_over_ch - sem, mean_over_ch + sem, alpha=0.25, color=color)
    ax.plot(times, mean_over_ch, color=color, lw=2, label=label)
    ax.set_title(f"{label}\n(mean ± SEM over channels)", fontsize=11)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Noise ceiling (%)")
    ax.axhline(0, color="k", lw=0.5, ls="--")
    ax.legend(fontsize=9)
 
fig.suptitle(f"Noise ceiling over time — {SUBJECT} / {ROI}", fontsize=13, y=1.01)
fig.tight_layout()
plt.savefig("images/fig_nc_over_time.png", dpi=150, bbox_inches="tight")
plt.show()
```


```python
fig, ax = plt.subplots(figsize=(9, 4))

for nc, label, color in zip(
    [nc_vb, nc_sh_pct, nc_stored],
    ["Variance-based", "Split-half", "Provided"],
    ["steelblue", "darkorange", "forestgreen"],
):
    mean_over_ch = np.nanmean(nc, axis=0)  # (tp,)
    ax.plot(times, mean_over_ch, color=color, lw=2, label=label)

ax.set_xlabel("Time (s)")
ax.set_ylabel("Noise ceiling (%)")
ax.set_title(f"Noise ceiling over time — {SUBJECT} / {ROI}\n(mean over channels)")
ax.axhline(0, color="k", lw=0.5, ls="--")
ax.legend()
fig.tight_layout()
plt.savefig("images/fig_nc_over_time_same_plot.png", dpi=150, bbox_inches="tight")
plt.show()
```


```python
fig, ax = plt.subplots(figsize=(7, 4))
for nc, label, color in zip(
    [nc_vb, nc_sh_pct, nc_stored],
    ["Variance-based", "Split-half", "Provided"],
    ["steelblue", "darkorange", "forestgreen"],
):
    mean_over_tp = np.nanmean(nc, axis=1)   # (ch,)
    ax.plot(range(n_ch), mean_over_tp, color=color, lw=1.8, label=label, alpha=0.85)
 
ax.set_xlabel("Channel index")
ax.set_ylabel("Noise ceiling (%)")
ax.set_title(f"Noise ceiling over channels (mean over time) — {SUBJECT} / {ROI}")
ax.legend()
fig.tight_layout()
plt.savefig("images/fig_nc_over_channels.png", dpi=150, bbox_inches="tight")
plt.show()
```


```python
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
labels = ["Variance-based (%)", "Split-half (%)", "Provided (%)"]
ncs    = [nc_vb, nc_sh_pct, nc_stored]
 
for ax, nc, label in zip(axes, ncs, labels):
    vmax = np.nanpercentile(nc, 95)
    im = ax.imshow(nc, aspect="auto", origin="lower",
                   extent=[times[0], times[-1], 0, n_ch],
                   vmin=0, vmax=vmax, cmap="viridis")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Channel index")
    ax.set_title(label)
    fig.colorbar(im, ax=ax, shrink=0.85)
 
fig.suptitle(f"Channel × time noise ceiling heatmaps — {SUBJECT} / {ROI}", fontsize=13)
fig.tight_layout()
plt.savefig("images/fig_nc_heatmaps.png", dpi=150, bbox_inches="tight")
plt.show()
```


```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for ax, nc_est, label, color in zip(
    axes,
    [nc_vb, nc_sh_pct],
    ["Variance-based − Provided", "Split-half − Provided"],
    ["RdBu_r", "RdBu_r"],
):
    diff = nc_est - nc_stored
    vmax = np.nanpercentile(np.abs(diff), 95)
    im = ax.imshow(diff, aspect="auto", origin="lower",
                   extent=[times[0], times[-1], 0, n_ch],
                   vmin=-vmax, vmax=vmax, cmap="RdBu_r")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Channel index")
    ax.set_title(f"{label}\n(mean diff = {np.nanmean(diff):.2f}%)")
    fig.colorbar(im, ax=ax, shrink=0.85)

fig.suptitle(f"Estimator difference from provided ceiling — {SUBJECT} / {ROI}", fontsize=13)
fig.tight_layout()
plt.savefig("images/fig_nc_diff_heatmaps.png", dpi=150, bbox_inches="tight")
plt.show()
```


```python
fig, ax = plt.subplots(figsize=(8, 4))
bins = np.linspace(0, 100, 60)
for nc, label, color in zip(
    [nc_vb.ravel(), nc_sh_pct.ravel(), nc_stored.ravel()],
    ["Variance-based", "Split-half", "Provided"],
    ["steelblue", "darkorange", "forestgreen"],
):
    ax.hist(nc[np.isfinite(nc)], bins=bins, histtype="step", lw=2, color=color,
        label=f"{label}  (mean={np.nanmean(nc):.1f}%)")
 
ax.set_xlabel("Noise ceiling (%)")
ax.set_ylabel("Density")
ax.set_title(f"Distribution of noise ceiling values — {SUBJECT} / {ROI}")
ax.legend()
fig.tight_layout()
plt.savefig("images/fig_nc_histogram.png", dpi=150, bbox_inches="tight")
plt.show()
```


```python
bins = np.linspace(0, 100, 60)

counts_sh,  _ = np.histogram(nc_sh_pct.ravel()[np.isfinite(nc_sh_pct.ravel())], bins=bins, density=True)
counts_ref, _ = np.histogram(nc_stored.ravel()[np.isfinite(nc_stored.ravel())], bins=bins, density=True)

bin_centers = 0.5 * (bins[:-1] + bins[1:])
diff_counts = counts_sh - counts_ref

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(bin_centers, diff_counts, width=bins[1]-bins[0], color="purple", alpha=0.7)
ax.axhline(0, color="k", lw=1)
ax.set_xlabel("Noise ceiling (%)")
ax.set_ylabel("Density difference (Split-half − Provided)")
ax.set_title(f"Where split-half differs from provided — {SUBJECT} / {ROI}")
fig.tight_layout()
plt.savefig("images/fig_nc_diff_counts.png", dpi=150, bbox_inches="tight")
plt.show()
```


```python
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
 
for ax, nc_est, label, color in zip(
    axes,
    [nc_vb, nc_sh_pct],
    ["Variance-based vs Provided", "Split-half vs Provided"],
    ["steelblue", "darkorange"],
):
    flat_stored = nc_stored.ravel()
    flat_est    = nc_est.ravel()
    mask        = np.isfinite(flat_stored) & np.isfinite(flat_est)
    r, p        = stats.pearsonr(flat_stored[mask], flat_est[mask])
    ax.scatter(flat_stored[mask], flat_est[mask], s=2, alpha=0.3, color=color)
    lim = [0, 100]
    ax.plot(lim, lim, "k--", lw=1)
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel("Provided ceiling (%)")
    ax.set_ylabel(f"{label.split(' vs')[0]} (%)")
    ax.set_title(f"{label}\nr = {r:.3f}, p = {p:.2e}")
 
fig.suptitle(f"Estimator vs provided ceiling — {SUBJECT} / {ROI}", fontsize=13)
fig.tight_layout()
plt.savefig("images/fig_nc_scatter_comparison.png", dpi=150, bbox_inches="tight")
plt.show()
```


```python
import importlib
import utils
importlib.reload(utils)
from utils import compute_ceiling_variancebased_clean, compute_ceiling_splithalf_clean

# Apply QC mask to reps — set flagged (stim, ch, rep) triples to NaN
# reps shape: (ch, tp, stim, reps) — need to broadcast mask accordingly
# quality_mask_test shape: (stim, ch, reps) → transpose to (ch, stim, reps)
mask_sch = quality_mask_test.transpose(1, 0, 2)          # (ch, stim, reps)
mask_bcast = mask_sch[:, np.newaxis, :, :]               # (ch, 1, stim, reps)
mask_bcast = np.broadcast_to(mask_bcast, reps.shape)     # (ch, tp, stim, reps)

reps_clean = reps.copy()
reps_clean[mask_bcast] = np.nan
print(f"Flagged {quality_mask_test.mean()*100:.2f}% of (stim, ch, rep) triples set to NaN")
print(f"Channel 13: {quality_mask_test[:, 13, :].mean()*100:.2f}% flagged")
print(f"Channel 53: {quality_mask_test[:, 53, :].mean()*100:.2f}% flagged")

# Recompute estimators on cleaned data using nan-safe versions
print("\nComputing variance-based ceiling on cleaned data...")
nc_vb_clean = compute_ceiling_variancebased_clean(reps_clean)
print("Computing split-half ceiling on cleaned data...")
nc_sh_clean = compute_ceiling_splithalf_clean(reps_clean, folds=10, seed=0) * 100

print(f"\nVB  raw: {np.nanmean(nc_vb):.2f}%  |  clean: {np.nanmean(nc_vb_clean):.2f}%")
print(f"SH  raw: {np.nanmean(nc_sh_pct):.2f}%  |  clean: {np.nanmean(nc_sh_clean):.2f}%")
print(f"\nChannel 13 — VB raw: {nc_vb[13].mean():.2f}%  |  clean: {np.nanmean(nc_vb_clean[13]):.2f}%")
print(f"Channel 53 — VB raw: {nc_vb[53].mean():.2f}%  |  clean: {np.nanmean(nc_vb_clean[53]):.2f}%")
print(f"Channel 13 — SH raw: {nc_sh_pct[13].mean():.2f}%  |  clean: {np.nanmean(nc_sh_clean[13]):.2f}%")
print(f"Channel 53 — SH raw: {nc_sh_pct[53].mean():.2f}%  |  clean: {np.nanmean(nc_sh_clean[53]):.2f}%")
```


```python
fig, axes = plt.subplots(2, 1, figsize=(10, 8))

# Plot 1: noise ceiling over channels
ax = axes[0]
for nc, label, color, ls in zip(
    [nc_vb, nc_sh_pct, nc_stored, nc_vb_clean, nc_sh_clean],
    ["VB raw", "SH raw", "Provided", "VB clean", "SH clean"],
    ["steelblue", "darkorange", "forestgreen", "steelblue", "darkorange"],
    ["-", "-", "-", "--", "--"],
):
    mean_over_tp = np.nanmean(nc, axis=1)
    ax.plot(range(n_ch), mean_over_tp, color=color, lw=1.8,
            label=label, alpha=0.85, ls=ls)

ax.set_xlabel("Channel index")
ax.set_ylabel("Noise ceiling (%)")
ax.set_title(f"Noise ceiling over channels — raw vs cleaned — {SUBJECT} / {ROI}")
ax.legend(ncol=2)

# Plot 2: difference between raw and clean for each estimator
ax = axes[1]
for nc_raw, nc_cl, label, color in zip(
    [nc_vb, nc_sh_pct],
    [nc_vb_clean, nc_sh_clean],
    ["VB clean − raw", "SH clean − raw"],
    ["steelblue", "darkorange"],
):
    diff = np.nanmean(nc_cl - nc_raw, axis=1)  # mean over time
    ax.plot(range(n_ch), diff, color=color, lw=1.8, label=label)

ax.axhline(0, color="k", lw=1, ls="--")
ax.set_xlabel("Channel index")
ax.set_ylabel("Difference (%)")
ax.set_title(f"Effect of QC cleaning on noise ceiling — {SUBJECT} / {ROI}")
ax.legend()

fig.tight_layout()
plt.savefig("images/fig_nc_cleaning_effect_channels.png", dpi=150, bbox_inches="tight")
plt.show()
```


```python
# quality_mask_test shape: (stim, ch, reps)
flagged_per_channel = quality_mask_test.mean(axis=(0, 2)) * 100  # mean over stim and reps
for ch in [13, 33, 53]:
    print(f"Channel {ch}: {flagged_per_channel[ch]:.2f}% of (stim, rep) pairs flagged")

print(f"\nAll channels mean: {flagged_per_channel.mean():.2f}%")
print(f"Max flagged channel: {flagged_per_channel.argmax()} ({flagged_per_channel.max():.2f}%)")
```


```python
fig, axes = plt.subplots(2, 3, figsize=(18, 8))

ncs    = [nc_vb, nc_sh_pct, nc_stored, nc_vb_clean, nc_sh_clean, nc_sh_clean - nc_sh_pct]
labels = ["VB raw", "SH raw", "Provided", "VB clean", "SH clean", "SH clean − SH raw"]
cmaps  = ["viridis", "viridis", "viridis", "viridis", "viridis", "RdBu_r"]

for ax, nc, label, cmap in zip(axes.ravel(), ncs, labels, cmaps):
    vmax = np.nanpercentile(np.abs(nc), 95)
    vmin = -vmax if cmap == "RdBu_r" else 0
    im = ax.imshow(nc, aspect="auto", origin="lower",
                   extent=[times[0], times[-1], 0, n_ch],
                   vmin=vmin, vmax=vmax, cmap=cmap)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Channel index")
    ax.set_title(label)
    fig.colorbar(im, ax=ax, shrink=0.85)

fig.suptitle(f"Raw vs cleaned noise ceilings — {SUBJECT} / {ROI}", fontsize=13)
fig.tight_layout()
plt.savefig("images/fig_nc_cleaning_heatmaps.png", dpi=150, bbox_inches="tight")
plt.show()
```


```python
import ipywidgets as widgets
from IPython.display import display
import matplotlib.colors as mcolors

# Load test repetitions for inspection
# reps_raw shape: (200, n_ch, 80, 80) — (stim, ch, reps, tp)
with h5py.File(EEG_REPS_PATH, "r") as f:
    test_reps_raw = f["test"]["neural_data"][SUBJECT][ROI][:]

n_stim_test, n_ch_test, n_reps_test, n_tp_test = test_reps_raw.shape
time_axis_test = np.linspace(0, 0.8, n_tp_test)

# Compute variance per (stim, ch, rep) for z-scoring
ep_var_test_raw = test_reps_raw.var(axis=3)  # (200, ch, 80)
ep_var_flat = ep_var_test_raw.reshape(n_stim_test * n_reps_test, n_ch_test)
stim_mean_test = ep_var_flat.mean(axis=0)
stim_std_test  = ep_var_flat.std(axis=0)

n_examples = 5

def plot_test_channel_detail(stim_idx, channel_idx, rep_offset):
    # Z-score variance for all (stim, rep) for this channel
    var_norm = (ep_var_test_raw[:, channel_idx, :] - stim_mean_test[channel_idx]) / \
               (stim_std_test[channel_idx] + 1e-8)  # (200, 80)

    print(f"Z-scores for shown repetitions (stim {stim_idx}, channel {channel_idx}):")
    for i in range(n_examples):
        rep = rep_offset + i
        z = var_norm[stim_idx, rep]
        flagged = quality_mask_test[stim_idx, channel_idx, rep]
        print(f"  Rep {rep}: z = {z:.2f}  {'← FLAGGED' if flagged else ''}")

    fig, axes = plt.subplots(1, 2, figsize=(16, 5))

    # Left: heatmap of z-scored variance across all reps x all stimuli for this channel
    im = axes[0].imshow(var_norm.T, aspect="auto", cmap="viridis",
                        interpolation="nearest",
                        norm=mcolors.SymLogNorm(linthresh=1))
    axes[0].axhline(y=rep_offset, color="orange", linewidth=1.5, linestyle="--")
    axes[0].axhline(y=rep_offset + n_examples - 1, color="orange", linewidth=1.5,
                    linestyle="--", label=f"Reps shown on right")
    axes[0].axvline(x=stim_idx, color="red", linewidth=1.5,
                    label=f"Stimulus {stim_idx}")
    axes[0].set_xlabel("Stimulus index")
    axes[0].set_ylabel("Repetition index")
    axes[0].set_title(f"Z-scored variance — channel {channel_idx}")
    axes[0].legend(fontsize=8)
    plt.colorbar(im, ax=axes[0], label="Z-scored variance")

    # Right: time courses of selected repetitions for this stim and channel
    for i in range(n_examples):
        rep = rep_offset + i
        flagged = quality_mask_test[stim_idx, channel_idx, rep]
        label = f"Rep {rep} {'[FLAGGED]' if flagged else ''}"
        axes[1].plot(time_axis_test, test_reps_raw[stim_idx, channel_idx, rep, :],
                     alpha=0.7, label=label,
                     linestyle="--" if flagged else "-")

    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Amplitude")
    axes[1].set_title(f"Time courses — channel {channel_idx}, stimulus {stim_idx}")
    axes[1].legend(fontsize=8)

    plt.tight_layout()
    plt.show()

stim_slider = widgets.IntSlider(
    value=92, min=0, max=n_stim_test - 1, step=1,
    description="Stimulus index:",
    continuous_update=False,
    style={"description_width": "initial"}
)
channel_slider = widgets.IntSlider(
    value=13, min=0, max=n_ch_test - 1, step=1,
    description="Channel index:",
    continuous_update=False,
    style={"description_width": "initial"}
)
rep_slider = widgets.IntSlider(
    value=9, min=0, max=n_reps_test - n_examples, step=1,
    description="Rep offset:",
    continuous_update=False,
    style={"description_width": "initial"}
)

widgets.interact(plot_test_channel_detail,
                 stim_idx=stim_slider,
                 channel_idx=channel_slider,
                 rep_offset=rep_slider)
```

<h3>Channel quality investigation in the test repetitions</h3>

Out of curiosity, we investigated whether the QC mask derived from the training data in 
Section 1.2 also captures problematic behavior in the test repetitions. We applied the same 
two filters — z-score on epoch variance and maximum absolute amplitude — to the test 
repetitions file, which contains all 80 repetitions for the 200 test stimuli. The overall 
flagging rate was 0.91%, but this varied dramatically across channels: channel 13 had 50.4% 
of its stimulus-repetition pairs flagged and channel 53 had 7.17% flagged, while most other 
channels had near-zero flagging rates.

We then recomputed both noise ceiling estimators using nan-safe versions that ignore flagged 
entries rather than dropping entire channels. The effect of cleaning on the noise ceiling 
estimates is shown below.

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nc_cleaning_effect_channels.png" style="width: 40%;"/>
    <figcaption>Top: mean noise ceiling over channels for raw and cleaned estimators. 
    Bottom: pointwise difference (clean minus raw) averaged over time. The variance-based 
    estimator drops substantially at channels 13 and 53 after cleaning, while the split-half 
    estimator is largely unaffected.</figcaption>
  </figure>
</div>

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nc_cleaning_heatmaps.png" style="width: 100%;"/>
    <figcaption>Channel × time heatmaps for raw and cleaned estimators. The effect of 
    cleaning is concentrated at channels 13 and 53 and is essentially invisible elsewhere.
    </figcaption>
  </figure>
</div>

For the vast majority of channels the cleaning has no visible effect on either estimator, 
which is reassuring given the low overall flagging rate. The only notable changes occur at 
channels 13 and 53. The variance-based estimator drops by around 24 percentage points at 
channel 13 and around 12 percentage points at channel 53 after cleaning. The split-half 
estimator is largely unaffected — it had already assigned near-zero reliability to those 
channels before cleaning, suggesting it was already sensitive to their poor quality without 
requiring the explicit QC step. We do not over-interpret this difference between the two 
estimators, as the precise reason depends on how each method aggregates information across 
repetitions and would require further investigation.

To understand what is happening at channel 13 specifically, we used the interactive widget 
to inspect individual test repetition time courses. The amplitude threshold used for the 
test repetitions was computed as the 99.11th percentile of the maximum absolute amplitude 
across all stimulus-channel-repetition triples, which yielded a threshold of 1073 — far 
above the intended range of around 50 that was appropriate for the training data. This 
inflation occurred because channel 13's extreme artifact values pulled the percentile 
threshold up dramatically, effectively disabling the amplitude filter for the test set. 
With a corrected threshold computed excluding channels 13 and 53, the threshold would be 
53.03, flagging 99.13% of channel 13's repetitions and 53.17% of channel 53's repetitions.

We show three representative examples from channel 13 below.

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/ch13_artifact_stim73.png" style="width: 100%;"/>
    <figcaption>Channel 13, stimulus 73 — all five shown repetitions are flagged by the 
    z-score filter and show highly reproducible sharp spikes reaching amplitudes of ±2500, 
    an order of magnitude larger than any other channel. The consistency of the artifact 
    across repetitions is notable — it looks more like a stimulus-locked hardware artifact 
    than random noise.</figcaption>
  </figure>
</div>

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/ch13_normal_stim92.png" style="width: 100%;"/>
    <figcaption>Channel 13, stimulus 92 — these repetitions were not flagged under the 
    original threshold of 1073 and show much lower amplitudes (roughly ±80). Whether 
    these represent clean signal or a milder form of the same artifact is unclear — a 
    threshold of 50 would flag them, but determining the appropriate threshold requires 
    more knowledge of what constitutes signal versus artifact for this channel and electrode 
    location. The variance-based estimator does not identify these as artifacts since their 
    variance is within the normal range.</figcaption>
  </figure>
</div>

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/ch13_mixed_stim128.png" style="width: 100%;"/>
    <figcaption>Channel 13, stimulus 128 — a mixed case where some repetitions are flagged 
    (reps 10, 12, 13) and one unflagged repetition (rep 11, green) shows a spike reaching 
    around -500, which would have been caught by an amplitude threshold of 50 but slipped 
    through the inflated threshold of 1073. This illustrates a limitation of the 
    percentile-based threshold approach: when one channel has pathologically extreme values, 
    it inflates the threshold and reduces the sensitivity of the amplitude filter for that 
    same channel.</figcaption>
  </figure>
</div>

Additionally, the z-scored variance heatmap for channel 13 — visible in all three figures 
above as the left panel — shows an interesting pattern: early repetitions (top rows) tend 
to have lower z-scored variance than later repetitions, suggesting the artifact may have 
worsened progressively over the course of the recording session. This is consistent with 
electrode drift or a gradually deteriorating contact, though we cannot confirm this without 
access to the raw recording metadata.

In summary, visual inspection confirms that channel 13 is severely corrupted in the test 
repetitions and should be excluded from any downstream analysis. Channel 53 is more 
ambiguous — with 7.17% flagged under the original threshold and 53.17% under the corrected 
threshold, its status depends strongly on the threshold choice. Resolving this would require 
knowledge of the electrode layout and ideally a systematic inspection of its time courses 
across stimuli, which is beyond the scope of this section. We flag both channels as 
potentially unreliable and use the uncleaned noise ceiling estimates for the remainder of 
the analysis to stay consistent with the provided ceilings.


```python
# print(f"thresh_abs_test = {thresh_abs_test:.2f}")

```


```python
# bad_channels = [13, 53]
# good_channels = [c for c in range(n_ch_test) if c not in bad_channels]
# thresh_abs_test = np.percentile(
#     np.abs(test_reps_raw[:, good_channels, :, :]), percentile_50
# )
# print(f"Threshold excluding bad channels: {thresh_abs_test:.2f}")

# # Recompute quality mask with corrected threshold
# quality_mask_test = (ep_var_norm_test > THRESHOLD) | (max_abs_test > thresh_abs_test)
# n_flagged = quality_mask_test.sum()
# n_total = quality_mask_test.size
# print(f"Flagged: {n_flagged} / {n_total} ({100 * n_flagged / n_total:.2f}%)")
# print(f"Channel 13: {quality_mask_test[:, 13, :].mean()*100:.2f}% flagged")
# print(f"Channel 53: {quality_mask_test[:, 53, :].mean()*100:.2f}% flagged")
```

Out of curiosity, we investigated whether applying the QC mask from Section 1.2 to the test 
repetitions changes the noise ceiling estimates. We set flagged stimulus-channel-repetition 
triples to NaN (0.91% overall, but 50.4% for channel 13 and 7.17% for channel 53) and 
recomputed both estimators using nan-safe versions that ignore missing entries.

For the vast majority of channels the cleaning has no visible effect on either estimator, 
which is reassuring given the low overall flagging rate. The only notable changes occur at 
channels 13 and 53. For the variance-based estimator, the ceiling drops by around 24 
percentage points at channel 13 and around 12 percentage points at channel 53 after cleaning. 
The split-half estimator is largely unaffected — which is not surprising given that it had 
already assigned near-zero reliability to those channels even before cleaning. In that sense 
the split-half estimator had already reflected the poor quality of those channels without 
needing the explicit QC step, while the variance-based estimator required the bad epochs to 
be removed before producing a similarly low estimate. We do not over-interpret this further. 
Given that the overall impact of cleaning is minimal and confined to the two channels already 
identified as problematic, we use the uncleaned estimates for the remainder of the analysis 
to stay consistent with the provided ceilings.


```python
import numpy as np


def compute_ceiling_variancebased(responses: np.ndarray, nan_policy: str = 'omit') -> np.ndarray:
    """
    Noise ceiling per unit using the method described in the NSD paper
    (Allen et al., 2021 / 2022 style variance-based estimator).

    Steps:
      1) z-score across stimuli (axis=1) for each (unit, rep) -> total var ≈ 1
      2) estimate noise variance across repetitions (axis=2), then average across stimuli
      3) signal variance = 1 - noise_var
      4) reliability (percent) for finite repeats:
             nc = 100 * (snr / (snr + 1 / n_reps))

    Parameters
    ----------
    responses : np.ndarray
        Shape (n_units, n_stimuli, n_reps) or
        (n_channels, n_timepoints, n_stimuli, n_reps).
    nan_policy : {'propagate', 'raise', 'omit'}, default='omit'
        Passed to the z-scoring logic when handling NaNs.

    Returns
    -------
    np.ndarray
        Per-unit noise ceilings in percent with shape (n_units,) or
        (n_channels, n_timepoints), depending on your implementation.
    """

    ### TODO
    pass


def compute_ceiling_splithalf(
    responses: np.ndarray,
    folds: int = 10,
    seed: int = 0,
    spearman_brown: bool = True,
    equalize_halves: bool = True,
    clip_folds: bool = False
) -> np.ndarray:
    """
    Split-half reliability per unit (voxel / channel / channel*timepoint).
    You can refer to van Bree et al. (2025) for mathematical details.
    
    Steps:
      1) For each fold, randomly split repetitions into two halves.
      2) Average responses within each half and compute Pearson correlation across stimuli.
      3) Optionally apply Spearman-Brown correction to each fold's correlation.
      4) Average across folds to get a final reliability estimate.

    Parameters
    ----------
    responses : np.ndarray
        Shape (n_units, n_stimuli, n_reps) or
        (n_channels, n_timepoints, n_stimuli, n_reps).
        The last axis corresponds to repetitions / trials.
    folds : int, default=10
        Number of random split-halves to sample.
    seed : int, default=0
        Base RNG seed; each fold may use seed + fold_idx.
    spearman_brown : bool, default=True
        Apply Spearman-Brown correction:
            r_sb = 2r / (1 + r)
    equalize_halves : bool, default=True
        If True, use equal-sized halves and drop one trial if n_reps is odd.
        If False, the second half may be larger by one trial.
    clip_folds : bool, default=False
        If True, clip reliability values after correction.

    Returns
    -------
    np.ndarray
        Array of shape (n_units) or (n_channels, n_timepoints).
    """
    ### TODO
    pass
```


```python
# TODO: load repeated EEG test responses
# TODO: compute variance-based estimator
# TODO: compute split-half estimator
# TODO: visualize and compare both estimators
```

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 1.3</strong><br>Compare the two estimators. Do they produce similar patterns across channels and time? Where do they differ most?</div>

We estimate noise ceilings using two methods — the variance-based estimator following Allen et al. 
(2022) and the split-half reliability estimator following van Bree et al. (2025) — and compare 
both to the provided ceilings stored in <code>things_eeg2.h5</code>. We use sub-01 and the 
<code>whole_brain</code> ROI throughout. Computing both estimators and comparing them to the 
stored values serves two purposes: it validates that our implementations are correct, and it tells 
us which method was used to generate the provided ceilings, which matters for interpreting how 
conservative or liberal those ceilings are.

The variance-based estimator works by decomposing total response variance into signal and noise 
components. For each channel × time unit, responses are first z-scored across stimuli for each 
repetition separately — this removes slow amplitude drifts across repetitions and ensures total 
variance is approximately 1. Noise variance is then estimated as the variance across repetitions 
averaged over stimuli, and signal variance is whatever remains. The noise ceiling is derived from 
the signal-to-noise ratio, corrected for the finite number of repetitions. The split-half estimator 
takes a different approach: it randomly splits the 80 repetitions into two halves of 40, averages 
each half, and computes the Pearson correlation of the two resulting response vectors across 
stimuli. This is repeated over 10 random splits and the Spearman-Brown correction is applied to 
each fold to project the half-repetition reliability to full-repetition reliability. The average 
across folds gives the final estimate.

We first plot the mean noise ceiling over time averaged across channels, shown separately for each 
estimator and then overlaid in a single plot to allow direct comparison. Plotting them separately 
first makes the temporal structure of each estimator visible including the standard deviation 
across channels, while the combined plot makes the differences between estimators easy to spot.

<div style="display: flex; gap: 10px; align-items: flex-start;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nc_over_time.png" style="width: 100%;"/>
    <figcaption>Mean noise ceiling over time with ± SEM across channels — separate subplots for each estimator</figcaption>
  </figure>
</div>

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: left; flex: 1;">
    <img src="images/fig_nc_over_time_same_plot.png" style="width: 60%;"/>
    <figcaption>Mean noise ceiling over time — all three estimators overlaid</figcaption>
  </figure>
</div>

All three estimators show the same temporal structure. The noise ceiling rises sharply from near 
zero at stimulus onset to around 30% by 0.1s, reflecting the onset of early visual responses. It 
remains elevated and peaks twice — first around 0.1–0.2s and again around 0.25–0.3s where it 
reaches its highest value of almost 35% — likely reflecting early and mid-latency visual 
processing stages. There is a local minimum around 0.35s before a second peak near 0.4s of 
similar height. After 0.4s the ceiling drops steeply and stays low for the remainder of the 0.8s 
window. This drop corresponds to when the third image in the RSVP sequence appears, at which point 
overlapping responses dominate and the signal is no longer stimulus-specific. The standard 
deviation across channels is largest around the peaks, confirming that channels differ 
substantially in how strongly they are driven by the visual stimulus. The low mean values after 
0.45s mean that responses there are not reliably stimulus-driven, and no model should be expected 
to predict them well. In the combined plot, the variance-based trace is invisible because it 
overlaps exactly with the provided ceiling. The split-half trace follows the same shape but sits 
slightly below the other two, particularly at the peaks, indicating it is consistently more 
conservative. This already suggests that the stored ceilings were generated using the 
variance-based method.

We next plot the mean noise ceiling over channels, averaged across all 80 time points, to identify 
which channels are reliably driven by the visual stimulus.

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: left; flex: 1;">
    <img src="images/fig_nc_over_channels.png" style="width: 70%;"/>
    <figcaption>Mean noise ceiling over channels (averaged across time) — all three estimators overlaid</figcaption>
  </figure>
</div>

Channels around indices 10–20 and 40–50 show the highest mean noise ceilings, suggesting these 
electrodes overlie visually responsive cortex. Most other channels show low average reliability. 
Again the variance-based and provided ceilings overlap completely. The split-half estimator follows 
the same overall pattern but shows more pronounced negative peaks at channels 13 and 53, and to a 
lesser extent channel 33. These are exactly the channels flagged as problematic during QC in 
Section 1.2, where they showed extreme amplitude jumps and were identified as likely faulty. The 
split-half estimator is more sensitive to these channels because the Spearman-Brown correction 
becomes unstable when the raw half-rep correlation is near zero or negative, which happens for 
genuinely noisy channels. The variance-based estimator is more robust in this regime since it uses 
all 80 repetitions simultaneously rather than pairs of 40-rep halves.

To see both the spatial and temporal structure of reliability at once, we plot channel × time 
heatmaps for all three estimators side by side. This is more informative than either of the 
previous plots alone since it shows whether the low-reliability channels are consistently low 
across all time points or only at specific windows.

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nc_heatmaps.png" style="width: 100%;"/>
    <figcaption>Channel × time noise ceiling heatmaps — variance-based, split-half, and provided side by side</figcaption>
  </figure>
</div>

High-reliability regions appear in the first 0.4s for channels around indices 10–20 and 40–50. 
After 0.4s even those channels drop to near zero. Channels 13, 53 and to a lesser extent 33 show 
visibly lower values in the split-half heatmap compared to the other two, while the variance-based 
and provided heatmaps are indistinguishable by eye. These channels are consistently low across the 
entire time window, confirming they are genuinely unreliable rather than just noisy at specific 
time points.

To quantify where the estimators differ from the provided ceiling, we subtract the provided ceiling 
from each estimator pointwise and plot the resulting difference heatmaps. This makes any systematic 
spatial or temporal bias immediately visible.

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nc_diff_heatmaps.png" style="width: 70%;"/>
    <figcaption>Pointwise difference from provided ceiling — variance-based (left) and split-half (right). Note that the colorbar range of the left panel is on the order of 1e-7, meaning the variance-based estimator is numerically identical to the provided ceiling up to floating point precision.</figcaption>
  </figure>
</div>

The left panel confirms that the variance-based and provided ceilings are numerically identical — 
the colorbar range of 1e-7 reflects only floating point rounding errors. The right panel shows the 
split-half minus provided difference. No systematic spatial or temporal trend is visible beyond the 
channel-specific effects at channels 13 and 53, which appear as strongly negative patches 
confirming that split-half assigns much lower reliability to those channels than the provided 
ceiling does.

To compare the overall value distributions, we plot step histograms of all three estimators and 
then the bin-wise density difference between split-half and provided. The histogram shows the 
shape of each distribution while the difference plot makes the shift between split-half and 
provided explicit at each ceiling value.

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nc_histogram.png" style="width: 70%;"/>
    <figcaption>Distribution of noise ceiling values across all channel × time units — step histograms for all three estimators</figcaption>
  </figure>
</div>

The variance-based and provided distributions are identical with a mean of 14.7%. The split-half 
distribution has a mean of 13.0%, 1.7 percentage points lower. Both distributions are strongly 
right-skewed with the majority of channel × time units having low noise ceilings, reflecting that 
most electrodes and time points are not strongly driven by the visual stimulus.

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nc_diff_counts.png" style="width: 70%;"/>
    <figcaption>Bin-wise density difference between split-half and provided ceiling. Positive bars mean split-half has more units at that ceiling value, negative bars mean fewer.</figcaption>
  </figure>
</div>

The density difference plot makes the distributional shift explicit. Split-half has substantially 
more mass in the first bin (0–2%) and slightly more in the second and third bins. From the fourth 
bin onwards the difference flips and the provided ceiling consistently has more mass, meaning the 
variance-based method assigns more units to moderate and high reliability values. This pattern is 
consistent with the split-half estimator being more conservative overall, driven primarily by the 
problematic channels pulling mass towards zero.

Finally we plot the direct scatter comparison between each estimator and the provided ceiling, 
which is the most direct test of how well each estimator reproduces the stored values point by 
point across all channel × time units.

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nc_scatter_comparison.png" style="width: 60%;"/>
    <figcaption>Scatter comparison of each estimator against the provided ceiling across all channel × time units</figcaption>
  </figure>
</div>

The variance-based estimator achieves r = 1.000 with the provided ceiling — a perfect match 
confirming these are numerically identical. The split-half estimator achieves r = 0.957, which is 
high but not perfect. The scatter shows that most points lie close to the diagonal, but there is a 
clear population of outliers with high provided ceiling values of up to 50% that correspond to 
near-zero split-half values. These outliers are channels 13 and 53, and they drive both the lower 
correlation and the excess low-value mass seen in the histogram. For well-behaved channels the two 
estimators agree closely, suggesting the difference is not a fundamental methodological 
disagreement but rather a sensitivity difference for genuinely noisy channels.

In summary, the variance-based estimator reproduces the stored ceilings exactly, confirming it was 
used to generate them. The split-half estimator is slightly more conservative on average and 
substantially more sensitive to problematic channels, which can be an advantage when the goal is 
to identify unreliable units but a disadvantage when the goal is to match a provided reference.

---

## 1.4 Compare the noise ceiling estimators statistically on EEG2

In `things_eeg2.h5`, we provided noise ceilings computed using one of the two methods you implemented. Can you determine which one it is by comparing the stored ceilings to your computed ones?

Perform a hypothesis test to compare the stored ceilings to each of your computed estimators. For example, you could compute the mean squared error between the stored ceilings and each estimator per subject/time/channel, and then use a paired t-test to see if one estimator is significantly closer to the stored values than the other.

<div style="background:#eef5fb; border-left:4px solid #4c78a8; padding:8px 12px; border-radius:6px; font-weight:700; color:#26445e;">What you must do</div>

- State clearly what each estimator assumes.
- Define a quantitative comparison to the stored EEG noise ceilings.
- Run at least one simple statistical test or formal comparison.

Examples:

- mean absolute deviation from the stored values,
- paired comparison across channel × time units,
- correlation with the stored values.


```python
import pandas as pd
from scipy import stats

# Flatten all arrays to 1D for comparison
flat_stored = nc_stored.ravel()
flat_vb     = nc_vb.ravel()
flat_sh     = nc_sh_pct.ravel()
mask        = np.isfinite(flat_stored) & np.isfinite(flat_vb) & np.isfinite(flat_sh)

# --- Quantitative comparison table ---
def comparison_metrics(nc_ref, nc_est, name):
    r, p   = stats.pearsonr(nc_ref[mask], nc_est[mask])
    mad    = np.abs(nc_ref[mask] - nc_est[mask]).mean()
    mse    = ((nc_ref[mask] - nc_est[mask]) ** 2).mean()
    max_d  = np.abs(nc_ref[mask] - nc_est[mask]).max()
    return dict(Estimator=name,
                Pearson_r=round(r, 6),
                MAD=round(mad, 6),
                MSE=round(mse, 6),
                Max_abs_diff=round(max_d, 6))

rows = [
    comparison_metrics(flat_stored, flat_vb, "Variance-based"),
    comparison_metrics(flat_stored, flat_sh, "Split-half"),
]
df_cmp = pd.DataFrame(rows).set_index("Estimator")
print("Quantitative comparison to stored noise ceilings\n")
print(df_cmp.to_string())

# --- Paired t-test on absolute errors ---
err_vb = np.abs(flat_stored[mask] - flat_vb[mask])
err_sh = np.abs(flat_stored[mask] - flat_sh[mask])
t_stat, p_val = stats.ttest_rel(err_vb, err_sh)

print(f"\nPaired t-test: |VB − stored| vs |SH − stored|")
print(f"  t = {t_stat:.4f},  p = {p_val:.4e}")
print(f"  Mean absolute error — VB: {err_vb.mean():.6f}%,  SH: {err_sh.mean():.3f}%")

better = "Variance-based" if err_vb.mean() < err_sh.mean() else "Split-half"
if p_val < 0.05:
    print(f"  → {better} is significantly closer to the stored values (p < 0.05).")
else:
    print(f"  → No significant difference between the two estimators (p = {p_val:.3f}).")
```

<div style="background:#f3f6fa; border-left:4px solid #7a93ac; padding:8px 12px; border-radius:6px; font-weight:700; color:#32475b;">Required deliverables</div>

You must include all of the following:

1. **One quantitative comparison table** comparing both estimators to the stored EEG noise ceilings.
2. **One statistical test or one formal quantitative comparison** such as a paired test, correlation analysis, or mean absolute deviation analysis.
3. **One concise written conclusion** stating which estimator better matches the stored values and why.

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 1.4</strong><br>Which estimator is more likely to have been used to generate the stored EEG noise ceilings? Justify your answer with both visual and quantitative evidence.</div>

To formally determine which estimator was used to generate the stored noise ceilings we 
computed four comparison metrics across all channel × time units for sub-01 / whole_brain: 
Pearson correlation, mean absolute deviation, mean squared error, and the maximum absolute 
difference anywhere.

<table style="border-collapse: collapse; width: 33%; margin: 10px 0;">
  <thead>
    <tr style="border-bottom: 2px solid #333;">
      <th style="text-align: left; padding: 6px 12px;">Estimator</th>
      <th style="text-align: center; padding: 6px 12px;">Pearson r</th>
      <th style="text-align: center; padding: 6px 12px;">MAD (%)</th>
      <th style="text-align: center; padding: 6px 12px;">MSE (%²)</th>
      <th style="text-align: center; padding: 6px 12px;">Max |diff| (%)</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom: 1px solid #ccc;">
      <td style="text-align: left; padding: 6px 12px;">Variance-based</td>
      <td style="text-align: center; padding: 6px 12px;">1.000000</td>
      <td style="text-align: center; padding: 6px 12px;">0.000000</td>
      <td style="text-align: center; padding: 6px 12px;">0.000000</td>
      <td style="text-align: center; padding: 6px 12px;">0.000001</td>
    </tr>
    <tr>
      <td style="text-align: left; padding: 6px 12px;">Split-half</td>
      <td style="text-align: center; padding: 6px 12px;">0.957</td>
      <td style="text-align: center; padding: 6px 12px;">2.298</td>
      <td style="text-align: center; padding: 6px 12px;">29.250</td>
      <td style="text-align: center; padding: 6px 12px;">66.383</td>
    </tr>
  </tbody>
</table>

The variance-based numbers are essentially zero everywhere — the maximum absolute difference 
across all 5040 channel × time units is 0.000001 percentage points, which is floating point 
rounding and nothing else. The split-half estimator correlates well (r = 0.957) but deviates 
on average by 2.3 percentage points per unit, with a worst case of 66.4 percentage points 
at the problematic channels we identified earlier.

We ran a paired t-test on the absolute errors of the two estimators across all channel × 
time units to confirm this statistically. The result is t = −33.32, p = 3.71 × 10⁻²²⁰, 
meaning the variance-based errors are significantly smaller at essentially every unit. The 
p-value is so extreme that it really just confirms what the table already shows — the 
variance-based estimator and the stored ceiling are the same thing up to numerical precision.

The stored noise ceilings were generated using the variance-based estimator. The two agree 
to floating point precision across all channel × time units, with r = 1.000 and a mean 
absolute deviation of zero. A paired t-test confirms this is not a coincidence — the 
variance-based errors are significantly smaller than the split-half errors at essentially 
every unit (t = −33.32, p = 3.71 × 10⁻²²⁰). The split-half estimator tracks the same 
overall pattern well but is consistently more conservative, particularly at channels 13 and 
53 where it assigns near-zero reliability while the stored ceiling does not. As discussed 
in Section 1.3, this reflects a sensitivity difference between the two methods rather than 
an error in either one.


```python
# TODO: define estimator comparison metric
# TODO: run statistical comparison
# TODO: summarize which estimator best matches stored values
```

---

## 1.5 Convert NSD ncsnr to noise ceiling and visualize it on cortex

Some datasets, such as NSD, provide reliability estimates with the data release. In this section, you will visualize the provided NSD reliability estimates on the cortical surface and convert them into noise ceilings for later use in predictive analyses.

The provided NSD reliability estimates are stored as **ncsnr** values on the fsaverage surface. To use them as noise ceilings for voxel-wise analyses, you need to convert ncsnr to noise ceiling using the formula provided in the NSD methods paper.

Parcellations and atlases provide group-level anatomical labels for brain regions. They are often defined on a standard surface or volume space (e.g., fsaverage, MNI) and can be used to summarize or interpret neural data. For this exercise, use the Destrieux atlas to anatomically label the regions with the highest and lowest noise ceilings. It is available in fsaverage space and can be accessed through `nilearn`. Compute the average noise ceiling within each atlas region and identify which regions have the highest and lowest reliability.

If the available atlas is in a different surface resolution (e.g. `fsaverage5`), you can interpolate either the atlas or the noise ceiling map to the same space before visualization. Prefer downsampling rather than upsampling to avoid introducing artificial precision.

You can use `nibabel` to load the `.mgh` files and `nilearn` to visualize the resulting noise ceiling on the fsaverage surface.


<div style="background:#eef5fb; border-left:4px solid #4c78a8; padding:8px 12px; border-radius:6px; font-weight:700; color:#26445e;">What you must do</div>

- Load the provided `.mgh` files for subject 01.
- Convert **ncsnr** to a **noise ceiling estimate** using the formula described in the NSD paper.
- Visualize the resulting noise ceiling on the fsaverage surface.
- Overlay a cortical parcellation.
- Compute parcel-wise average values.

<div style="background:#f3f6fa; border-left:4px solid #7a93ac; padding:8px 12px; border-radius:6px; font-weight:700; color:#32475b;">Required deliverables</div>

You must include all of the following:

1. **One histogram of ncsnr values**
2. **One cortical surface plot** of ncsnr or the derived noise ceiling
3. **One cortical surface plot with parcel overlay**
4. **One parcel-wise summary figure or one parcel-wise summary table**

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 1.5</strong><br>Which cortical regions appear most reliable, and which appear least reliable? Explain how the parcellation helps interpret the surface maps.</div>

The NSD dataset provides reliability estimates as ncsnr values on the fsaverage surface 
rather than directly as noise ceilings. We load the provided <code>.mgh</code> files for 
subject 01 and convert them to noise ceilings using the formula from Allen et al. (2022):

$$NC = \frac{\text{ncsnr}^2}{\text{ncsnr}^2 + \frac{1}{n}}$$

where $n = 3$ reflects the fact that trial-wise betas are averaged across three presentations 
of each image before fitting the encoding model. The resulting noise ceiling is in the range 
[0, 1] and directly interpretable as the maximum fraction of response variance that any model 
could theoretically explain for a given voxel.

We first inspect the distribution of ncsnr values and the derived noise ceilings across all 
fsaverage vertices.

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nsd_ncsnr_histogram.png" style="width: 80%;"/>
    <figcaption>Distribution of ncsnr values (blue) and derived noise ceilings (orange) 
    across all fsaverage vertices for subject 01. Only non-zero vertices are shown. Both 
    distributions are strongly right-skewed, reflecting that most cortical vertices are not 
    reliably driven by the visual stimuli. The compression from ncsnr to noise ceiling is 
    a nonlinear effect of the conversion formula — even the most reliable voxels only reach 
    a ceiling of around 0.87, reflecting the fundamental limit imposed by averaging only 
    three repetitions.</figcaption>
  </figure>
</div>

Both hemispheres show nearly identical distributions, confirming the data quality is 
consistent across hemispheres. The large spike near zero reflects the majority of cortical 
vertices that lie outside visually responsive areas. The long right tail of the ncsnr 
distribution represents a small number of highly reliable voxels, most likely in early 
visual cortex.

We then visualize the noise ceiling on the inflated fsaverage surface alongside the top 10 
most reliable Destrieux parcels to allow direct comparison between the continuous reliability 
map and the discrete anatomical boundaries.

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nsd_nc_left_lateral.png" style="width: 93%;"/>
    <figcaption>Left lateral — noise ceiling</figcaption>
  </figure>
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nsd_nc_top10_left_lateral.png" style="width: 80%;"/>
    <figcaption>Left lateral — top 10 parcels</figcaption>
  </figure>
</div>

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nsd_nc_left_medial.png" style="width: 93%;"/>
    <figcaption>Left medial — noise ceiling</figcaption>
  </figure>
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nsd_nc_top10_left_medial.png" style="width: 80%;"/>
    <figcaption>Left medial — top 10 parcels</figcaption>
  </figure>
</div>

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nsd_nc_right_lateral.png" style="width: 93%;"/>
    <figcaption>Right lateral — noise ceiling</figcaption>
  </figure>
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nsd_nc_top10_right_lateral.png" style="width: 80%;"/>
    <figcaption>Right lateral — top 10 parcels</figcaption>
  </figure>
</div>

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nsd_nc_right_medial.png" style="width: 93%;"/>
    <figcaption>Right medial — noise ceiling</figcaption>
  </figure>
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nsd_nc_top10_right_medial.png" style="width: 80%;"/>
    <figcaption>Right medial — top 10 parcels</figcaption>
  </figure>
</div>

The pattern is clear and anatomically consistent across both hemispheres. The highest noise 
ceilings are concentrated in the posterior occipital cortex, particularly in the lateral 
views where the occipital pole is visible at the back of the brain, and in the medial views 
where a bright strip runs along the bottom of the surface corresponding to the calcarine 
sulcus — the location of primary visual cortex. Reliability drops off steeply as you move 
anteriorly towards frontal and temporal cortex. The two hemispheres look nearly symmetric.

To identify which specific brain regions are most and least reliable, we use the Destrieux 
atlas to compute parcel-wise average noise ceilings. The Destrieux atlas divides the cortical 
surface into 74 named regions per hemisphere based on sulcal and gyral landmarks. Since the 
atlas is defined on fsaverage5 (10242 vertices per hemisphere) rather than the full fsaverage 
resolution, we first downsample our noise ceiling map using nearest-neighbor interpolation 
before averaging within each parcel.

<div style="display: flex; gap: 10px; align-items: flex-start; margin-top: 15px;">
  <figure style="text-align: center; flex: 1;">
    <img src="images/fig_nsd_nc_parcels.png" style="width: 80%;"/>
    <figcaption>Top 10 most reliable (left) and bottom 10 least reliable (right) Destrieux 
    regions by average noise ceiling across hemispheres. Blue bars show left hemisphere 
    values, orange bars show right hemisphere values, and the black marker shows the 
    bilateral average.</figcaption>
  </figure>
</div>

The top 10 regions are entirely occipital — the occipital pole, the posterior collateral 
sulcus, the middle occipital gyrus, the anterior occipital sulcus and the lateral 
occipito-temporal gyrus which includes the fusiform face area. The most reliable region 
overall is the posterior transverse collateral sulcus with an average noise ceiling of 0.54, 
followed by the anterior occipital sulcus at 0.52 and the occipital pole at 0.51. These 
values mean that even the most reliable regions have around half their response variance 
explained by the stimulus, with the other half being noise — reflecting the fundamental 
challenge of single-subject fMRI with limited repetitions.

The bottom 10 regions are all non-visual — motor cortex, frontal cortex, temporal pole and 
auditory cortex — with average noise ceilings below 0.03, essentially zero. This means they 
produce no reliable stimulus-driven responses to the NSD images as expected.

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 1.5</strong><br>

The most reliable cortical regions are concentrated in occipital cortex, particularly 
around the occipital pole, the posterior collateral sulcus, and the calcarine sulcus where 
primary visual cortex sits. Average noise ceilings in these regions reach around 0.50 to 
0.54, meaning roughly half of the response variance is reliably stimulus-driven. The least 
reliable regions are motor cortex, frontal cortex, temporal pole and auditory cortex, all 
with noise ceilings below 0.03. This pattern is exactly what you would expect from a 
dataset of visual images — areas that process visual information are reliably driven by 
the stimuli, while areas involved in motor control, language and audition are not.

The Destrieux parcellation is useful here because it translates the continuous surface map 
into specific anatomical names, making it possible to say concretely which regions are 
reliable rather than just pointing at blobs. It also reveals subtle differences between 
hemispheres — for example the posterior collateral sulcus has a noise ceiling of 0.516 in 
the left hemisphere but 0.566 in the right, suggesting slightly stronger visual responses 
on the right side for this subject. Whether this reflects a genuine hemispheric asymmetry 
or subject-specific variability would require comparison across subjects.
</div>


```python
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# Load ncsnr maps for subject 01
lh_img = nib.load(NSD_NCSNR_LH)
rh_img = nib.load(NSD_NCSNR_RH)

lh_ncsnr = lh_img.get_fdata().squeeze()
rh_ncsnr = rh_img.get_fdata().squeeze()

print(f"LH ncsnr shape: {lh_ncsnr.shape}, range: {lh_ncsnr.min():.3f} – {lh_ncsnr.max():.3f}")
print(f"RH ncsnr shape: {rh_ncsnr.shape}, range: {rh_ncsnr.min():.3f} – {rh_ncsnr.max():.3f}")

# Convert ncsnr to noise ceiling using the NSD formula (Allen et al. 2022)
# ncsnr = signal / noise
# noise ceiling (explained variance) = ncsnr^2 / (ncsnr^2 + 1/n_avg)
# For NSD, n_avg = 3 (average number of repetitions per image for the test set)
n_avg = 3
lh_nc = lh_ncsnr**2 / (lh_ncsnr**2 + 1.0 / n_avg)
rh_nc = rh_ncsnr**2 / (rh_ncsnr**2 + 1.0 / n_avg)

print(f"\nLH noise ceiling range: {lh_nc.min():.3f} – {lh_nc.max():.3f}")
print(f"RH noise ceiling range: {rh_nc.min():.3f} – {rh_nc.max():.3f}")
```


```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for ax, ncsnr, nc, hemi in zip(
    axes,
    [lh_ncsnr, rh_ncsnr],
    [lh_nc, rh_nc],
    ["Left hemisphere", "Right hemisphere"],
):
    # only plot non-zero vertices (zero = outside cortex / medial wall)
    mask = ncsnr > 0
    ax2 = ax.twinx()
    ax.hist(ncsnr[mask], bins=80, color="steelblue", histtype="step", lw=2,
            label="ncsnr")
    ax2.hist(nc[mask], bins=80, color="darkorange", histtype="step", lw=2,
             label="noise ceiling")
    ax.set_xlabel("Value")
    ax.set_ylabel("Count (ncsnr)", color="steelblue")
    ax2.set_ylabel("Count (noise ceiling)", color="darkorange")
    ax.set_title(f"{hemi}")
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

fig.suptitle("Distribution of ncsnr and derived noise ceiling — subj01", fontsize=13)
fig.tight_layout()
plt.savefig("images/fig_nsd_ncsnr_histogram.png", dpi=150, bbox_inches="tight")
plt.show()
```


```python
from nilearn import plotting as nlplt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

views = ["lateral", "medial"]
hemis = [("left", lh_nc), ("right", rh_nc)]

sm = cm.ScalarMappable(cmap="hot", norm=mcolors.Normalize(vmin=0, vmax=0.9))
sm.set_array([])

for hemi, nc in hemis:
    for view in views:
        fig = plt.figure(figsize=(7, 5))
        ax = fig.add_subplot(111, projection="3d")
        nlplt.plot_surf_stat_map(
            fsaverage[f"infl_{hemi}"],
            stat_map=nc,
            hemi=hemi,
            view=view,
            colorbar=False,
            cmap="hot",
            vmax=0.9,
            bg_map=fsaverage[f"sulc_{hemi}"],
            axes=ax,
            title=f"{hemi} — {view}",
        )
        fig.colorbar(sm, ax=ax, shrink=0.5, pad=0.05, label="Noise ceiling")
        plt.savefig(f"images/fig_nsd_nc_{hemi}_{view}.png",
                    dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Saved: {hemi} — {view}")
```


```python
fig, axes = plt.subplots(1, 2, figsize=(16, 5),
                         subplot_kw={"projection": "3d"})
nlplt.plot_surf_stat_map(
    fsaverage["infl_left"],
    stat_map=lh_nc,
    hemi="left",
    view="lateral",
    colorbar=False,
    cmap="hot",
    vmax=0.9,
    bg_map=fsaverage["sulc_left"],
    axes=axes[0],
    title="Left — lateral",
)
nlplt.plot_surf_stat_map(
    fsaverage["infl_right"],
    stat_map=rh_nc,
    hemi="right",
    view="lateral",
    colorbar=False,
    cmap="hot",
    vmax=0.9,
    bg_map=fsaverage["sulc_right"],
    axes=axes[1],
    title="Right — lateral",
)
# add shared colorbar
import matplotlib.cm as cm
import matplotlib.colors as mcolors
sm = cm.ScalarMappable(cmap="hot", norm=mcolors.Normalize(vmin=0, vmax=0.9))
sm.set_array([])
fig.colorbar(sm, ax=axes, shrink=0.5, label="Noise ceiling")
fig.suptitle("NSD noise ceiling — subj01", fontsize=13)
plt.savefig("images/fig_nsd_nc_surface.png", dpi=150, bbox_inches="tight")
plt.show()
```


```python
from nilearn import datasets
import pandas as pd

# Load Destrieux atlas — labels on fsaverage5 (10242 vertices per hemi)
destrieux = datasets.fetch_atlas_surf_destrieux()
lh_labels = destrieux["map_left"]   # (10242,) integer labels
rh_labels = destrieux["map_right"]  # (10242,) integer labels
label_names = [name.decode() if isinstance(name, bytes) else name 
               for name in destrieux["labels"]]

print(f"LH labels shape: {lh_labels.shape}")
print(f"Number of regions: {len(label_names)}")
print(f"NC map LH shape: {lh_nc.shape}")  # 163842

# Downsample fsaverage NC to fsaverage5 by loading fsaverage5 coordinates
# and finding nearest fsaverage vertex for each fsaverage5 vertex
fsaverage5 = datasets.fetch_surf_fsaverage(mesh='fsaverage5')
fsaverage_full = datasets.fetch_surf_fsaverage(mesh='fsaverage')

from nilearn import surface

# Load coordinates of both meshes
coords_fs5_lh, _ = surface.load_surf_mesh(fsaverage5["pial_left"])
coords_fs_lh, _  = surface.load_surf_mesh(fsaverage_full["pial_left"])
coords_fs5_rh, _ = surface.load_surf_mesh(fsaverage5["pial_right"])
coords_fs_rh, _  = surface.load_surf_mesh(fsaverage_full["pial_right"])

# For each fsaverage5 vertex find nearest fsaverage vertex
from scipy.spatial import cKDTree

tree_lh = cKDTree(coords_fs_lh)
_, idx_lh = tree_lh.query(coords_fs5_lh)
lh_nc_fs5 = lh_nc[idx_lh]

tree_rh = cKDTree(coords_fs_rh)
_, idx_rh = tree_rh.query(coords_fs5_rh)
rh_nc_fs5 = rh_nc[idx_rh]

print(f"Downsampled LH NC shape: {lh_nc_fs5.shape}")
print(f"Downsampled RH NC shape: {rh_nc_fs5.shape}")

# Compute parcel-wise averages
rows = []
for i, name in enumerate(label_names):
    lh_mask = lh_labels == i
    rh_mask = rh_labels == i
    lh_mean = lh_nc_fs5[lh_mask].mean() if lh_mask.sum() > 0 else np.nan
    rh_mean = rh_nc_fs5[rh_mask].mean() if rh_mask.sum() > 0 else np.nan
    avg = np.nanmean([lh_mean, rh_mean])
    rows.append(dict(Region=name, LH=round(lh_mean, 3), 
                     RH=round(rh_mean, 3), Average=round(avg, 3)))

df_parcels = pd.DataFrame(rows).set_index("Region")
df_parcels = df_parcels.sort_values("Average", ascending=False)

print("\nTop 10 most reliable regions:")
print(df_parcels.head(10).to_string())
print("\nBottom 10 least reliable regions:")
print(df_parcels.tail(10).to_string())
```


```python
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

for ax, df_sub, title in zip(
    axes,
    [df_parcels.dropna().head(10), df_parcels.dropna().iloc[-10:]],
    ["Top 10 most reliable regions", "Bottom 10 least reliable regions"],
):
    regions = df_sub.index[::-1]
    y = np.arange(len(regions))
    width = 0.3

    ax.barh(y + width/2, df_sub["LH"][::-1], width, 
            color="steelblue", alpha=0.8, label="LH")
    ax.barh(y - width/2, df_sub["RH"][::-1], width,
            color="darkorange", alpha=0.8, label="RH")
    ax.plot(df_sub["Average"][::-1], y, "k|", 
            markersize=10, markeredgewidth=2, label="Average")

    ax.set_yticks(y)
    ax.set_yticklabels(regions, fontsize=9)
    ax.set_xlabel("Noise ceiling")
    ax.set_title(title)
    ax.legend()
    ax.axvline(0, color="k", lw=0.5)

fig.suptitle("Parcel-wise noise ceiling — subj01 (Destrieux atlas)", fontsize=13)
fig.tight_layout()
plt.savefig("images/fig_nsd_nc_parcels.png", dpi=150, bbox_inches="tight")
plt.show()
```


```python
import numpy as np

# Get top 10 region names (excluding Unknown/NaN)
top10_names = list(df_parcels.dropna().head(10).index)

# Create label maps that only show top 10 regions, rest = 0
def make_top10_map(labels, label_names, top10_names):
    out = np.zeros_like(labels, dtype=float)
    for i, name in enumerate(label_names):
        if name in top10_names:
            rank = top10_names.index(name) + 1  # 1 = most reliable
            out[labels == i] = rank
    return out

lh_top10_map = make_top10_map(lh_labels, label_names, top10_names)
rh_top10_map = make_top10_map(rh_labels, label_names, top10_names)

# Plot all 4 views
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

configs = [
    ("left",  lh_top10_map, "lateral",  fsaverage5["infl_left"],  fsaverage5["sulc_left"]),
    ("left",  lh_top10_map, "medial",   fsaverage5["infl_left"],  fsaverage5["sulc_left"]),
    ("right", rh_top10_map, "lateral",  fsaverage5["infl_right"], fsaverage5["sulc_right"]),
    ("right", rh_top10_map, "medial",   fsaverage5["infl_right"], fsaverage5["sulc_right"]),
]

for hemi, nc_map, view, surf, sulc in configs:
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    nlplt.plot_surf_stat_map(
        surf,
        stat_map=nc_map,
        hemi=hemi,
        view=view,
        colorbar=False,
        cmap="tab10",
        vmin=0,
        vmax=10,
        bg_map=sulc,
        axes=ax,
        title=f"{hemi} — {view}",
    )
    # add legend for top 10 regions
    cmap = cm.get_cmap("tab10", 10)
    patches = [mpatches.Patch(color=cmap(i), 
                              label=f"{i+1}. {top10_names[i]}") 
               for i in range(10)]
    ax.legend(handles=patches, loc="lower left", fontsize=7,
              bbox_to_anchor=(0, 0))
    plt.savefig(f"images/fig_nsd_nc_top10_{hemi}_{view}.png",
                dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {hemi} — {view}")
```


```python
# TODO: load lh/rh ncsnr maps
# TODO: convert ncsnr to noise ceiling
# TODO: plot histogram
# TODO: visualize on fsaverage
# TODO: compute parcel-wise summary
```

---

# 2. Brain–Model Alignment

In this section, you will compare neural responses and model features using **both representational metrics and predictive linear models**. You must complete both parts of this section. The goal is not only to report scores, but also to compare what different metrics reveal about model–brain alignment.

## 2.1 Representational alignment: RSA

RSA stands for representational similarity analysis. It is one of the most widely used analyses in fMRI and model–brain alignment research. It compares the geometry of two representational spaces through their representational dissimilarity matrices (RDMs). Given two response matrices, `X` and `Y`, with rows corresponding to the same stimuli, we first compute an RDM for each matrix using correlation distance:

$$
D^X_{ij} = 1 - \mathrm{corr}(X[i,:], X[j,:]),
\qquad
D^Y_{ij} = 1 - \mathrm{corr}(Y[i,:], Y[j,:]),
$$

for stimulus pairs $i \neq j$.

We then vectorize the upper triangle of each RDM and compute RSA as the Spearman correlation between these two vectors:

$$
\mathrm{RSA}(X, Y)
=
\rho_{\mathrm{Spearman}}
\left(
\mathrm{vec}(D^X),\,
\mathrm{vec}(D^Y)
\right).
$$

In this project, `X` will usually denote model features from one candidate layer, and `Y` will denote neural responses from one dataset, ROI, subject, or time slice, depending on the analysis.

- Implement RSA between two representation matrices.
- Support at least one dissimilarity measure and one similarity measure.
- Use your implementation to compare model layers to neural responses.


```python
import importlib
import utils
importlib.reload(utils)
from utils import RepresentationalSimilarityAnalysis

# quick sanity check
rsa = RepresentationalSimilarityAnalysis(dissimilarity="correlation", 
                                          similarity_metric="spearman")
X = np.random.randn(20, 100)
Y = np.random.randn(20, 50)
print(f"RSA between random matrices: {rsa(X, Y):.4f}  (should be near 0)")
print(f"RSA of matrix with itself:   {rsa(X, X):.4f}  (should be 1.0)")
```

### Starter code


```python
from typing import Literal
import numpy as np

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
        ### TODO
        pass

    def __call__(self, X: np.ndarray, Y: np.ndarray) -> float:
        """
        Compute RSA similarity between X and Y.

        Parameters
        ----------
        X, Y : np.ndarray
            Arrays of shape (n_conditions, ...) that may need to be flattened
            along feature dimensions.

        Returns
        -------
        rsa_similarity : float
            Correlation between the vectorized upper triangles of the two RDMs.
        """
        return self.forward(X, Y)

    def forward(self, X: np.ndarray, Y: np.ndarray) -> float:
        ### TODO
        pass

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
        ### TODO
        pass

    def compare_rdms(self, rdm1: np.ndarray, rdm2: np.ndarray) -> float:
        """
        Compare two RDMs by correlating their upper triangles.
        """
        ### TODO
        pass
```

## 2.2 Representational alignment: unbiased linear CKA

CKA stands for centered kernel alignment. It is commonly used in interpretability and representation analysis to test how strongly the internal computations of two systems align. As a second mapping-free alignment metric, we want to compute unbiased linear centered kernel alignment (CKA) between model features and neural responses. Let

$$
X \in \mathbb{R}^{n \times d}, \qquad
Y \in \mathbb{R}^{n \times p},
$$

where both matrices are measured on the same $n$ stimuli. We form linear Gram matrices

$$
K = XX^\top,
\qquad
L = YY^\top.
$$

We then estimate dependence using the unbiased (U-statistic) HSIC estimator, $\mathrm{HSIC}_u(K, L)$, and define CKA as

$$
\mathrm{CKA}(X, Y)
=
\frac{\mathrm{HSIC}_u(K, L)}
{\sqrt{\mathrm{HSIC}_u(K, K)\,\mathrm{HSIC}_u(L, L)}}.
$$

Like RSA, CKA compares representational structure directly without fitting a predictive mapping. In this notebook, `X` and `Y` again refer to aligned model and neural response matrices evaluated on the same set of stimuli.

- Implement **unbiased linear CKA** only.
- Use your implementation to compare model layers to neural responses.


```python
import importlib
import utils
importlib.reload(utils)
from utils import CenteredKernelAlignment

cka = CenteredKernelAlignment()

X = np.random.randn(100, 50)
Y = np.random.randn(100, 30)

print(f"CKA between random matrices:  {cka(X, Y):.4f}  (should be near 0)")
print(f"CKA of matrix with itself:    {cka(X, X):.4f}  (should be near 1)")
print(f"CKA with scaled version:      {cka(X, X * 2):.4f}  (should be near 1 — scale invariant)")
print(f"CKA with orthogonal rotation: {cka(X, X @ np.linalg.qr(np.random.randn(50,50))[0]):.4f}  (should be near 1)")
```

### Starter code


```python
import numpy as np

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
        ### TODO
        pass

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

        X : [n, d_x]
        Y : [n, d_y]
        """
        ### TODO
        pass

    def _unbiased_linear_cka(self, X: np.ndarray, Y: np.ndarray) -> float:
        """
        Unbiased linear CKA:

            CKA_unb(X, Y) =
                HSIC_unb(X, Y) / sqrt(HSIC_unb(X, X) * HSIC_unb(Y, Y))
        """
        ### TODO
        pass
```

## 2.3 Apply RSA and CKA

<div style="background:#eef5fb; border-left:4px solid #4c78a8; padding:8px 12px; border-radius:6px; font-weight:700; color:#26445e;">What you must do</div>

- Compare layers within each model.
- Compare the two models.
- For EEG, show how representational similarity changes over time.
- For TVSD and NSD, compare across ROIs.

<div style="background:#f3f6fa; border-left:4px solid #7a93ac; padding:8px 12px; border-radius:6px; font-weight:700; color:#32475b;">Required deliverables</div>

You must include all of the following:

1. **Layer-wise RSA results** for both models.
2. **Layer-wise CKA results** for both models.
3. **One direct comparison between the two models** using representational metrics.
4. **One EEG time-resolved analysis** or **one ROI-wise analysis** for TVSD/NSD.
5. **One short written interpretation** in Answer box 2.1.

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 2.1</strong><br>Do RSA and CKA tell the same story? Identify at least one case where they agree and one case where they disagree, and explain what that might mean.</div>


```python
# TODO: implement RSA
# TODO: implement unbiased linear CKA
# TODO: compute scores across layers
# TODO: compare across models and ROIs / time windows
```


```python
with h5py.File(FEAT_A_THINGS, "r") as f:
    f.visititems(lambda name, obj: print(name, "→", obj.shape if hasattr(obj, "shape") else "group"))
```


```python
with h5py.File(FEAT_B_THINGS, "r") as f:
    f.visititems(lambda name, obj: print(name, "→", obj.shape if hasattr(obj, "shape") else "group"))
```


```python
with h5py.File(TVSD_PATH, "r") as f:
    f.visititems(lambda name, obj: print(name, "→", obj.shape if hasattr(obj, "shape") else "group"))
```


```python
import importlib
import utils
importlib.reload(utils)
from utils import RepresentationalSimilarityAnalysis, CenteredKernelAlignment, get_feat_rows

# Define layers for both models
with h5py.File(FEAT_A_THINGS, "r") as f:
    layers_A = sorted(f["features"].keys())

with h5py.File(FEAT_B_THINGS, "r") as f:
    layers_B = sorted(f["features"].keys())

print("Model A layers:", layers_A)
print("Model B layers:", layers_B)

# Instantiate metrics
rsa = RepresentationalSimilarityAnalysis(dissimilarity="correlation",
                                          similarity_metric="spearman")
cka = CenteredKernelAlignment()
```


```python
# Load TVSD test data — all ROIs and both monkeys
tvsd_rois   = ["V1", "V4", "IT"]
tvsd_monkeys = ["monkeyF", "monkeyN"]
tvsd_test    = {}
tvsd_nc      = {}

with h5py.File(TVSD_PATH, "r") as f:
    # stimulus IDs are shared
    tvsd_test_ids = f["test/stimulus_ids"][:]
    
    for monkey in tvsd_monkeys:
        for roi in tvsd_rois:
            key = f"{monkey}_{roi}"
            tvsd_test[key]  = f[f"test/neural_data/{monkey}/{roi}"][:]
            tvsd_nc[key]    = f[f"noise_ceilings/{monkey}/{roi}"][:]
            print(f"{key}: responses {tvsd_test[key].shape}, "
                  f"nc {tvsd_nc[key].shape}")

print(f"\nTest stimulus IDs shape: {tvsd_test_ids.shape}")
print(f"Example IDs: {tvsd_test_ids[:3]}")
```


```python
# Match TVSD stimulus IDs to feature rows
with h5py.File(FEAT_A_THINGS, "r") as f:
    feat_ids_A = f["ids"][:]

with h5py.File(FEAT_B_THINGS, "r") as f:
    feat_ids_B = f["ids"][:]

# Build index maps
id_to_idx_A = {id_: i for i, id_ in enumerate(feat_ids_A)}
id_to_idx_B = {id_: i for i, id_ in enumerate(feat_ids_B)}

# Get feature row indices for TVSD test stimuli
feat_idx_A = np.array([id_to_idx_A[x] for x in tvsd_test_ids])
feat_idx_B = np.array([id_to_idx_B[x] for x in tvsd_test_ids])

print(f"Feature indices shape: {feat_idx_A.shape}")
print(f"First 3 indices A: {feat_idx_A[:3]}")

# Compute RSA and CKA across layers for each monkey/ROI combination
results = []

for layer_key, feat_path, feat_idx, model_name in [
    *[(f"features/{l}", FEAT_A_THINGS, feat_idx_A, "ResNet152") for l in layers_A],
    *[(f"features/{l}", FEAT_B_THINGS, feat_idx_B, "Qwen3-VL") for l in layers_B],
]:
    # Load features for matched stimuli
    sort_idx = np.argsort(feat_idx)
    unsort_idx = np.argsort(sort_idx)
    with h5py.File(feat_path, "r") as f:
        feats = f[layer_key][feat_idx[sort_idx]][unsort_idx]  # (100, 30000)

    layer_name = layer_key.replace("features/", "")

    for key, neural in tvsd_test.items():
        rsa_score = rsa(feats, neural)
        cka_score = cka(feats, neural)
        monkey, roi = key.split("_")
        results.append(dict(
            model=model_name,
            layer=layer_name,
            monkey=monkey,
            roi=roi,
            rsa=rsa_score,
            cka=cka_score,
        ))
        print(f"{model_name} | {layer_name} | {key}: RSA={rsa_score:.3f}, CKA={cka_score:.3f}")

import pandas as pd
df_tvsd = pd.DataFrame(results)
print("\nDone. Shape:", df_tvsd.shape)
```


```python
import seaborn as sns

# Define layer order for each model (by depth)
layer_order_A = ['layer1-0', 'layer2-0', 'layer3-0', 'layer3-5', 'layer3-10',
                 'layer3-15', 'layer3-20', 'layer3-25', 'layer3-30', 'layer4-1']
layer_order_B = ['visual-blocks-2', 'visual-blocks-6', 'visual-blocks-10',
                 'visual-blocks-14', 'visual-blocks-18', 'visual-blocks-22',
                 'language_model-layers-3', 'language_model-layers-8',
                 'language_model-layers-11', 'language_model-layers-16']

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

for col, (model_name, layer_order) in enumerate([
    ("ResNet152", layer_order_A),
    ("Qwen3-VL", layer_order_B),
]):
    df_model = df_tvsd[df_tvsd["model"] == model_name].copy()
    df_model["layer"] = pd.Categorical(df_model["layer"], 
                                        categories=layer_order, ordered=True)
    df_model = df_model.sort_values("layer")

    for row, metric in enumerate(["rsa", "cka"]):
        ax = axes[row, col]
        for roi in ["V1", "V4", "IT"]:
            # average over monkeys
            df_roi = df_model[df_model["roi"] == roi].groupby("layer")[metric].mean()
            ax.plot(range(len(layer_order)), df_roi.values, 
                    marker="o", lw=2, label=roi)
        
        ax.set_xticks(range(len(layer_order)))
        ax.set_xticklabels(layer_order, rotation=45, ha="right", fontsize=8)
        ax.set_xlabel("Layer")
        ax.set_ylabel(metric.upper())
        ax.set_title(f"{model_name} — {metric.upper()} — TVSD")
        ax.legend()
        ax.axhline(0, color="k", lw=0.5, ls="--")

fig.suptitle("Layer-wise RSA and CKA — TVSD (averaged over monkeys)", fontsize=13)
fig.tight_layout()
plt.savefig("images/fig_tvsd_rsa_cka_layers.png", dpi=150, bbox_inches="tight")
plt.show()
```

---

## 2.4 Predictive alignment: linear encoding models

## Linear encoding model

In the predictive part of the project, you will map model features to neural responses using a **linear encoding model with L2 regularization (ridge regression)**.

For a stimulus $\mathbf{x}$, let $\mathbf{z}_{\ell}(\mathbf{x})$ denote the feature vector extracted from model layer $\ell$. For a given subject $s$ and neural target $r$ (for example an ROI, a group of voxels, or a set of channels / time points), the predicted neural response is

$$
\widehat{\mathbf{y}}_{r,s}(\mathbf{x})
=
W_{r,s}\,\mathbf{z}_{\ell}(\mathbf{x}) + \mathbf{b}_{r,s},
$$

where:
- $\mathbf{z}_{\ell}(\mathbf{x}) \in \mathbb{R}^{d}$ is the model feature vector,
- $\widehat{\mathbf{y}}_{r,s}(\mathbf{x}) \in \mathbb{R}^{p}$ is the predicted neural response,
- $W_{r,s} \in \mathbb{R}^{p \times d}$ is the learned linear mapping,
- $\mathbf{b}_{r,s} \in \mathbb{R}^{p}$ is a bias term.

We fit the mapping on the training split using ridge regression:

$$
\min_{W_{r,s},\,\mathbf{b}_{r,s}}
\sum_{\mathbf{x}\in\mathcal{D}_{\mathrm{train}}}
\left\|
\mathbf{y}_{r,s}(\mathbf{x}) - \widehat{\mathbf{y}}_{r,s}(\mathbf{x})
\right\|_2^2
\;+\;
\alpha \left\|W_{r,s}\right\|_F^2.
$$

Here, $\mathbf{y}_{r,s}(\mathbf{x})$ is the measured neural response, and $\alpha$ controls the strength of L2 regularization. Larger $\alpha$ penalizes large weights more strongly, which can improve generalization when the feature dimension is high. You should select $\alpha$ using only the training data, for example with a validation split or cross-validation, and then evaluate the final model on the held-out test set.

<div style="background:#eef8f4; border-left:4px solid #5b9a7a; padding:8px 12px; border-radius:6px; font-weight:700; color:#285943;">Select the required targets</div>

Use the following targets:

- **TVSD:** all ROIs
- **EEG2:** `occipital_parietal`
- **NSD:** `V1v`, `V2v`, `V3v`, `hV4`, `FFA-1`, `VWFA-1`, `PPA`, `OPA`, `EBA`

You may explore additional ROIs if you wish.

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 2.2</strong><br>Briefly explain why these targets are scientifically interesting. Are they chosen mainly for reliability, interpretability, or both?</div>


```python
# TODO: define target ROIs / regions
# TODO: load corresponding neural data
```

<div style="background:#eef5fb; border-left:4px solid #4c78a8; padding:8px 12px; border-radius:6px; font-weight:700; color:#26445e;">What you must do</div>

For each dataset, target, model, and candidate layer:

- fit a **linear encoding model**,
- select hyperparameters without using the test split,
- evaluate on the test split.

Use iterative solvers (e.g. SGD, Adam) when needed to avoid memory issues, since `sklearn` Ridge might cause OOM.

<div style="background:#f3f6fa; border-left:4px solid #7a93ac; padding:8px 12px; border-radius:6px; font-weight:700; color:#32475b;">Required deliverables</div>

You must include all of the following:

1. **A clearly defined train/validation/test procedure** that does not use the test set for model selection.
2. **Linear encoding model results** for all required datasets and targets.
3. **The following predictive metrics:** Pearson correlation, noise-corrected Pearson correlation, explained variance, and noise-corrected explained variance.
4. **The following hybrid representational metrics on predicted responses:** encoding-RSA and encoding-CKA.
5. **Layer-wise plots** showing performance across candidate layers.
6. **One best-layer summary table** for the required targets.
7. **One comparison between the two models** using predictive results.
8. **One short written interpretation** in Answer box 2.3.

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 2.3</strong><br>Which model and which layer perform best for each dataset? Summarize the main trends in a short paragraph.</div>


```python
# TODO: define train/val/test procedure
# TODO: fit linear models across layers
# TODO: compute predictive metrics
# TODO: summarize best layers and best scores
```

---

## 2.5 Compare predictive and representational metrics

<div style="background:#eef5fb; border-left:4px solid #4c78a8; padding:8px 12px; border-radius:6px; font-weight:700; color:#26445e;">What you must do</div>

Compare the ranking of models and layers according to:

- Pearson correlation,
- explained variance,
- RSA,
- CKA.
- encoding-RSA/ encoding-CKA

Discuss whether the same layers are favored by all metrics.

<div style="background:#f3f6fa; border-left:4px solid #7a93ac; padding:8px 12px; border-radius:6px; font-weight:700; color:#32475b;">Required deliverables</div>

You must include all of the following:

1. **One figure comparing layer or model rankings across metrics**
2. **One concrete example where two metrics agree**
3. **One concrete example where two metrics disagree**
4. **One short written interpretation** in Answer box 2.4.

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 2.4</strong><br>Does a model that is representationally similar to the brain also predict neural responses well? Use at least one example from your results.</div>


```python
# TODO: compare ranking of layers across metrics
# TODO: identify agreements and disagreements
```

---

## 2.6 Relate layer hierarchy to brain hierarchy

<div style="background:#eef5fb; border-left:4px solid #4c78a8; padding:8px 12px; border-radius:6px; font-weight:700; color:#26445e;">What you must do</div>

Test whether deeper layers align better with higher-level neural targets.

- Does TVSD IT align with deeper layers than V1?
- Do higher-level NSD regions prefer later layers?
- For EEG, are particular time windows associated with later layers?

<div style="background:#f3f6fa; border-left:4px solid #7a93ac; padding:8px 12px; border-radius:6px; font-weight:700; color:#32475b;">Required deliverables</div>

You must include one of the following analyses:

1. **A heatmap of layer × ROI**
2. **A ranked-layer plot by ROI**
3. **A time-resolved EEG layer comparison**

You must also include a short written conclusion in Answer box 2.5 stating whether the results support a hierarchy correspondence.

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 2.5</strong><br>Is there evidence for a correspondence between model depth and neural hierarchy? State your conclusion clearly and support it with results.</div>


```python
# TODO: compare layers across ROIs / time windows
# TODO: create hierarchy figure(s)
```

---

## 2.7 Compare the two feature extractors

<div style="background:#eef5fb; border-left:4px solid #4c78a8; padding:8px 12px; border-radius:6px; font-weight:700; color:#26445e;">What you must do</div>

Compare **Qwen3-VL-2B-Instruct** and **Adv-ResNet152** across datasets, ROIs, layers, and metrics.

<div style="background:#f3f6fa; border-left:4px solid #7a93ac; padding:8px 12px; border-radius:6px; font-weight:700; color:#32475b;">Required deliverables</div>

You must include all of the following:

1. **One summary figure comparing Qwen3-VL-2B-Instruct and Adv-ResNet152**
2. **One table of best scores across datasets and targets**
3. **One short written interpretation** in Answer box 2.6.

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 2.6</strong><br>Does the vision-language model provide a clear advantage over the CNN? Is that advantage consistent across modalities and targets?</div>


```python
# TODO: aggregate results across both models
# TODO: create summary comparison figure/table
```

---

# 3. Open-Ended Research

So far you have explored a simple encoding model with a linear readout from a single layer per subject/ROI. In this section, you will extend the baseline pipeline in one clearly defined direction. The goal is to explore a meaningful extension that goes beyond the standard linear readout and to evaluate whether it provides a practically meaningful improvement. Depth is more important than breadth: a focused experiment is better than a broad but shallow exploration.

Possible directions include:

- readouts shared across ROIs,
- readouts shared across subjects,
- readouts shared across modalities,
- combining multiple layers,
- low-rank readouts,
- nonlinear readouts,
- temporal readouts for EEG,
- attention-based readouts,
- cross-subject pooling.

## What you must include

1. **Question**  
   What are you testing?

2. **Motivation**  
   Why is this extension interesting?

3. **Method**  
   What did you change relative to the linear baseline?

4. **Comparison**  
   How does it compare to the baseline?

5. **Interpretation**  
   Did it help, and why might that be?

<div style="background:#f3f6fa; border-left:4px solid #7a93ac; padding:8px 12px; border-radius:6px; font-weight:700; color:#32475b;">Required deliverables</div>

You must include all of the following:

1. **A clearly stated hypothesis**
2. **A short motivation for the extension**
3. **A clear description of the new method**
4. **One direct comparison against the linear baseline**
5. **At least one figure or one table summarizing the comparison**
6. **A short discussion of whether the extension helped in a practically meaningful way**

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box 3</strong><br>State your hypothesis, summarize your result, and say whether the new method helped in a practically meaningful way.</div>


```python
# TODO: define extension
# TODO: implement method
# TODO: compare against linear baseline
```

---

# Final Discussion

End the notebook with a short final discussion.

<div style="background:#eef5fb; border-left:4px solid #4c78a8; padding:8px 12px; border-radius:6px; font-weight:700; color:#26445e;">What you must address</div>

- Which dataset appeared noisiest?
- Which neural targets were most reliable?
- Which model aligned best overall?
- Which metrics were most consistent with each other?
- What was the main limitation of your analysis?
- What would you try next with more time?

<div style="background:#fff4c2; border:1px solid #c89b1f; border-left:6px solid #9a6f00; padding:10px 12px; border-radius:6px; margin-top:8px; margin-bottom:4px; color:#241a00; line-height:1.45;"><strong style="color:#5c4300;">Answer box final</strong><br>Write a concise final conclusion of 1–2 paragraphs summarizing your main findings and their limitations.</div>


```python
# No code required here unless you want to add final summary tables/figures.
```

---

# Report Content

Your **2-page PDF report** should tell a clear and coherent story. It does **not** need to reproduce every notebook result.

It can include:

1. **A brief dataset overview**
2. **An exploratory figure from Section 1**
3. **The EEG noise ceiling comparison**
4. **The NSD reliability visualization**
5. **One or two key brain–model alignment results from Section 2**


Rather, you should primarily focus on the open-ended extension you designed, describing:
- the motivation for your extension,
- the methods you implemented,
- the results you obtained,
- and the scientific insights you gained from it.


The report should emphasize interpretation, not just figures. Since the notebook is the main technical deliverable, the report should act as a **compressed scientific summary** of your most important findings rather than a figure dump.

---

# Detailed Grading Rubric

The project is graded out of **100 points** as follows:

- **Section 1: Inspection, Visualization, and Noise Ceiling Estimates — 20 points**
- **Section 2: Brain–Model Alignment — 20 points**
- **Section 3: Open-Ended Research — 30 points**
- **Report — 30 points**

**Section 0 is required but not graded separately.** It is treated as setup and reproducibility infrastructure for the rest of the notebook.

## Section 1 — 20 points

### 1.1 Dataset inspection — 3 points
- 1 pt: TVSD structure is correctly inspected and explained.
- 1 pt: EEG2 structure is correctly inspected and explained.
- 1 pt: NSD structure is correctly inspected and explained.

### 1.2 EEG visualization — 4 points
- 1 pt: example EEG time-course plot is present and readable.
- 1 pt: channel × time heatmap is present and readable.
- 1 pt: provided EEG noise ceiling visualization is present and readable.
- 1 pt: written interpretation identifies informative time windows or channel groups.

### 1.3 EEG noise ceiling estimation — 7 points
- 2 pts: variance-based estimator is implemented correctly.
- 2 pts: split-half estimator is implemented correctly.
- 1 pt: required summary visualizations are included.
- 1 pt: comparison to stored EEG noise ceilings is shown clearly.
- 1 pt: Answer box 1.3 interprets similarities and differences between estimators.

### 1.4 Statistical comparison of EEG noise ceilings — 3 points
- 1 pt: quantitative comparison table is present.
- 1 pt: statistical test or formal comparison is appropriate and correctly interpreted.
- 1 pt: final conclusion is clearly justified.

### 1.5 NSD reliability visualization — 3 points
- 1 pt: ncsnr is correctly converted and visualized on cortex.
- 1 pt: parcel overlay or parcel-wise summary is included.
- 1 pt: Answer box 1.5 correctly interprets reliable and unreliable regions.

## Section 2 — 20 points

### 2.1 RSA implementation — 3 points
- 1 pt: RDM computation is correct.
- 1 pt: RDM comparison is correct.
- 1 pt: implementation is used properly in later analyses.

### 2.2 Unbiased linear CKA implementation — 3 points
- 2 pts: unbiased linear CKA is implemented correctly.
- 1 pt: implementation is used properly in later analyses.

### 2.3 Representational analyses across layers, models, and targets — 4 points
- 1 pt: layer-wise RSA results are reported clearly.
- 1 pt: layer-wise CKA results are reported clearly.
- 1 pt: a model comparison is included.
- 1 pt: ROI-wise or time-resolved analysis is included and interpreted.

### 2.4 Predictive alignment with linear encoding models — 6 points
- 1 pt: required targets are selected and described correctly.
- 2 pts: train/validation/test procedure and ridge fitting are correct.
- 1 pt: required predictive metrics are reported correctly.
- 1 pt: encoding-RSA and encoding-CKA are reported correctly.
- 1 pt: best-layer summary and model comparison are included.

### 2.5 Compare predictive and representational metrics — 2 points
- 1 pt: ranking comparison figure is present and informative.
- 1 pt: agreement and disagreement between metrics are discussed clearly.

### 2.6 Layer hierarchy vs brain hierarchy — 1 point
- 1 pt: at least one hierarchy analysis is included and interpreted correctly.

### 2.7 Compare the two feature extractors — 1 point
- 1 pt: final comparison between Qwen3-VL and Adv-ResNet is clear and supported by results.

## Section 3 — 30 points

### Research question and motivation — 5 points
- 2 pts: research question is clear and focused.
- 3 pts: motivation is scientifically sensible and well connected to the baseline project.

### Method and implementation — 10 points
- 4 pts: the extension is described clearly.
- 4 pts: the method is implemented correctly.
- 2 pts: the design remains focused and technically appropriate for the project scope.

### Baseline comparison and evaluation — 10 points
- 4 pts: the comparison to the linear baseline is fair.
- 3 pts: at least one figure or table communicates the comparison clearly.
- 3 pts: evaluation supports the stated conclusion.

### Interpretation and limitations — 5 points
- 3 pts: the student explains whether the method helped in a practically meaningful way.
- 2 pts: limitations or caveats are acknowledged.

## Report — 30 points

### Structure and clarity — 6 points
- clear organization, readable flow, and concise scientific writing.

### Selection of results — 6 points
- the report focuses on the strongest and most relevant results rather than trying to include everything.

### Methodological correctness — 6 points
- metrics, comparisons, and claims are described accurately.

### Interpretation and synthesis — 6 points
- the report explains what the results mean and ties them back to the project goals.

### Figure quality and presentation — 6 points
- figures are readable, labeled, well-chosen, and integrated into the narrative.

## Important grading note

A submission that is technically correct but poorly interpreted will lose points. A submission with good intuition but missing required analyses will also lose points. The strongest submissions will be both **correct** and **scientifically well explained**.

---

# Final Checklist Before Submission

Before submitting, make sure that:

- group information is filled in,
- the notebook runs from top to bottom,
- all notebook outputs are cleared,
- figures have readable titles and labels,
- written answers are included in the answer boxes,
- the zip archive name follows the required format,
- no large unnecessary files are included.

---

# References

Use the references below when you need scientific context for the datasets, models, and analysis methods.

## Datasets

- Papale et al. (2025) — *An extensive dataset of spiking activity to reveal the syntax of the ventral stream*
- Gifford et al. (2022) — *A large and rich EEG dataset for modeling human visual object recognition*
- Allen et al. (2022) — *A massive 7T fMRI dataset to bridge cognitive neuroscience and artificial intelligence*
- van Bree, Styrnal, and Hebart (2025) — *How Much Variance Does Your Model Explain? A Clarifying Note On The Use Of Split-Half Reliability For Computing Noise Ceilings*

## Models

- Wong et al. (2020) — *Fast is better than free: Revisiting adversarial training*
- He et al. (2016) — *Deep Residual Learning for Image Recognition*
- Bai et al. (2025) — *Qwen3-VL Technical Report*

## Alignment and encoding

- Conwell et al. (2024) — *A large-scale examination of inductive biases shaping high-level visual representation in brains and machines*
- Gokce and Schrimpf (2025) — *Scaling Laws for Task-Optimized Models of the Primate Visual Ventral Stream*

Use these references selectively. You are not expected to read everything in full.
