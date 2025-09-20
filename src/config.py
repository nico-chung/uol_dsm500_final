# src/config.py
"""
Central configuration for the project.

Defines canonical paths, dataset descriptors, grouping, plotting styles,
and a few reproducibility defaults. Notebooks should declare important
analysis variables (e.g., SEED, ALPHA, BETA, BOOTSTRAP_B) inline so
readers can see them.
"""

from __future__ import annotations
from pathlib import Path

# ---------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------
# This file resides in src/, so the project root is one level up.
PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]

# Input data (CAT2000)
DATA_DIR: Path = PROJECT_ROOT / "data"
CAT2000_DIR: Path = DATA_DIR / "CAT2000" / "trainSet"
STIMULI_DIR: Path = CAT2000_DIR / "Stimuli"
FIXATIONLOCS_DIR: Path = CAT2000_DIR / "FIXATIONLOCS"
FIXATIONMAPS_DIR: Path = CAT2000_DIR / "FIXATIONMAPS"  # present in dataset; may be unused

# Output root (all notebooks should write under results/notebook{NN}/section{SS}/)
RESULTS_DIR: Path = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# Dataset configuration
# ---------------------------------------------------------------------
# Canonical category names (no renaming). Order is used everywhere.
CAT_ORDER = [
    "Action",
    "Affective",
    "Social",
    "Indoor",
    "OutdoorManMade",
    "OutdoorNatural",
]

# Backward-compat aliases (some early notebooks referenced these)
CATEGORIES = list(CAT_ORDER)
CATEGORY_ORDER = list(CAT_ORDER)

# Anthropomorphic vs Non-anthropomorphic groupings
ANTHROPOMORPHIC_CATEGORIES = ["Action", "Affective", "Social"]
NONANTHROPOMORPHIC_CATEGORIES = ["Indoor", "OutdoorManMade", "OutdoorNatural"]

GROUP_MAP = {
    "Action": "Anthropomorphic",
    "Affective": "Anthropomorphic",
    "Social": "Anthropomorphic",
    "Indoor": "Non-anthropomorphic",
    "OutdoorManMade": "Non-anthropomorphic",
    "OutdoorNatural": "Non-anthropomorphic",
}
GROUP_ORDER = ["Anthropomorphic", "Non-anthropomorphic"]

# CAT2000 image geometry
IMG_WIDTH: int = 1920
IMG_HEIGHT: int = 1080

# ---------------------------------------------------------------------
# ROI clustering (DBSCAN) defaults (Notebook 02 / appendix foil)
# ---------------------------------------------------------------------
DBSCAN_EPS: int = 60             # ~1.5 deg visual angle
DBSCAN_MIN_SAMPLES: int = 15     # minimum points to form dense region
MIN_ROI_DIM: int = 30            # minimum pixel dimension for valid ROI

# ---------------------------------------------------------------------
# VLM and segmentation assets (Notebook 03/04)
# ---------------------------------------------------------------------
QWEN_GGUF_PATH: Path = PROJECT_ROOT / "models" / "qwen" / "Qwen_Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf"
QWEN_MMPROJ_PATH: Path = PROJECT_ROOT / "models" / "qwen" / "mmproj-Qwen_Qwen2.5-VL-7B-Instruct-f16.gguf"
SAM_CHECKPOINT_PATH: Path = PROJECT_ROOT / "models" / "sam" / "sam2.1_hiera_large.state_dict.pt"

# Grammar files for constrained decoding
GRAMMARS_DIR: Path = PROJECT_ROOT / "src" / "grammars"
GRAMMAR_FILES = {
    "boolean": GRAMMARS_DIR / "binary_choice.gbnf"
}

# Reload large models periodically to mitigate VRAM fragmentation
MEMORY_RESET_INTERVAL: int = 10

# ---------------------------------------------------------------------
# Reproducibility (project default; notebooks should set their own SEED)
# ---------------------------------------------------------------------
RANDOM_SEED: int = 42  # notebooks typically override and print their SEED

# ---------------------------------------------------------------------
# Rendering & formatting
# ---------------------------------------------------------------------
# Numeric display (notebook writers should format to 3 decimals explicitly)
DEFAULT_DECIMALS: int = 3

# Segmentation overlay colors (RGBA)
PROMPT_COLORS = {
    "person": (0, 0, 255, 100),   # blue with alpha
    "face":   (0, 255, 0, 100),   # green with alpha
    "hand":   (255, 0, 0, 100),   # red with alpha
}

# Figures
FIG_DPI: int = 120
PLOT_LINEWIDTH: float = 1.6
BOXPLOT_WIDTH: float = 0.45

# Category color mapping (consistent across notebooks)
CATEGORY_COLORS = {
    "Action": "#7ad151",          # light green
    "Affective": "#414487",       # indigo
    "Social": "#fde725",          # yellow
    "Indoor": "#22a884",          # teal
    "OutdoorManMade": "#2a7886",  # blue-green
    "OutdoorNatural": "#440154",  # dark purple
}
CATEGORY_PALETTE = [CATEGORY_COLORS[c] for c in CAT_ORDER]

# ---------------------------------------------------------------------
# Center-bias & bootstrap defaults (kept minimal; notebooks decide details)
# ---------------------------------------------------------------------
# Many analyses in Notebook 05 use empirical center priors and notebook-level settings.
# Keep only minimal placeholders here if needed by earlier notebooks.
CENTER_BIAS_SIGMA_X_FRAC: float = 0.30 
CENTER_BIAS_SIGMA_Y_FRAC: float = 0.30