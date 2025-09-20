#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
ROOT="/home/nico/Projects/final_project"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"
LOGFILE="$LOG_DIR/environment_setup.log"

echo "[log] Environment setup started" | tee "$LOGFILE"

# --- 0) Conda Prerequisite Check ---
if ! command -v conda >/dev/null 2>&1; then
  echo "[error] Conda not found. Install Miniconda or Anaconda." | tee -a "$LOGFILE"
  exit 1
fi

# --- 1) Create/Activate Conda Environment ---
ENV_NAME="gaze-project"
PY_VER="3.11"
echo "[step] Creating/using conda env: $ENV_NAME (Python $PY_VER)" | tee -a "$LOGFILE"
source "$(conda info --base)/etc/profile.d/conda.sh"
if ! conda info --envs | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  conda create -n "$ENV_NAME" "python=$PY_VER" -y 2>&1 | tee -a "$LOGFILE"
fi
conda activate "$ENV_NAME"

# --- 2) Install System Dependencies ---
echo "[step] Installing system packages" | tee -a "$LOGFILE"
sudo apt-get update -y 2>&1 | tee -a "$LOGFILE"
sudo apt-get install -y build-essential cmake git pkg-config 2>&1 | tee -a "$LOGFILE"

# --- 3) Install PyTorch with CUDA ---
echo "[step] Installing PyTorch CUDA 12.4 wheels" | tee -a "$LOGFILE"
pip install --upgrade pip wheel setuptools 2>&1 | tee -a "$LOGFILE"
pip install --index-url https://download.pytorch.org/whl/cu124 \
  torch==2.4.1 torchvision==0.19.1 2>&1 | tee -a "$LOGFILE"

# --- 4) Install Pinned Python Requirements ---
echo "[step] Installing pinned Python requirements" | tee -a "$LOGFILE"
pip install -r "$ROOT/requirements.txt" 2>&1 | tee -a "$LOGFILE"

# --- 5) Build llama.cpp with CUDA ---
echo "[step] Building llama.cpp with CUDA" | tee -a "$LOGFILE"
cd "$ROOT"
if [ -d "llama.cpp" ]; then
  if ! git -C llama.cpp rev-parse HEAD >/dev/null 2>&1; then
    echo "[warn] Corrupted llama.cpp repo. Removing and recloning." | tee -a "$LOGFILE"
    rm -rf llama.cpp
  fi
fi
if [ ! -d "llama.cpp" ]; then
  git clone https://github.com/ggerganov/llama.cpp.git 2>&1 | tee -a "$LOGFILE"
fi
cd llama.cpp
DEFAULT_BRANCH=$(git remote show origin | awk '/HEAD branch/ {print $NF}')
git fetch origin "$DEFAULT_BRANCH" --depth 1 2>&1 | tee -a "$LOGFILE"
git checkout "$DEFAULT_BRANCH" 2>&1 | tee -a "$LOGFILE"
git reset --hard "origin/$DEFAULT_BRANCH" 2>&1 | tee -a "$LOGFILE"
mkdir -p build && cd build
cmake .. -DLLAMA_JSON=ON -DGGML_CUDA=ON 2>&1 | tee -a "$LOGFILE"
cmake --build . --config Release -j 2>&1 | tee -a "$LOGFILE"

# --- 6) Final Verification Imports ---
echo "[step] Verifying Python imports" | tee -a "$LOGFILE"
python - <<'PYCHECK' 2>&1 | tee -a "$LOGFILE"
import sys, torch, torchvision, pandas, numpy, cv2, yaml
print("python", sys.version.split()[0])
print("torch", torch.__version__, "cuda", torch.version.cuda, "is_available", torch.cuda.is_available())
print("torchvision", torchvision.__version__)
print("pandas", pandas.__version__)
print("numpy", numpy.__version__)
print("opencv", cv2.__version__)
PYCHECK

# --- 7) Generate Environment Manifest ---
echo "[step] Writing manifest" | tee -a "$LOGFILE"
python - <<'PYMANIFEST' 2>&1 | tee -a "$LOGFILE"
import json, os, platform, subprocess, time
from pathlib import Path
root = Path(r"/home/nico/Projects/final_project")
def git_rev(path: Path):
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root).decode().strip()
    except Exception:
        return None
manifest = {
  "project_root": str(root),
  "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
  "git_commit": git_rev(root),
  "platform": platform.platform(),
}
out = root / "outputs" / "artifacts"
out.mkdir(parents=True, exist_ok=True)
(out / "manifest.json").write_text(json.dumps(manifest, indent=2))
print(json.dumps(manifest, indent=2))
PYMANIFEST

echo "[done] Environment setup complete." | tee -a "$LOGFILE"
