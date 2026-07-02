# Operating Guide

This guide describes how to reproduce the Ob-Int CART workflow from a clean checkout.

## 1. Prepare the Dataset

The dataset is not included in this repository. Download it from the supporting information of the manuscript:

```text
Interpretable decision tree-assisted optimization of PLD growth of EuBa2Cu3O7-delta films
```

Place the downloaded CSV file at:

```text
data/train.csv
```

## 2. Prepare Python Environment

Python 3.10 or later is recommended.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Register the environment as a Jupyter kernel:

```bash
python -m ipykernel install --user --name ob-int-cart --display-name "Python (Ob-Int CART)"
```

## 3. Start JupyterLab

From the repository root:

```bash
jupyter lab
```

Open:

```text
Ob-Int CART.ipynb
```

Select the `Python (Ob-Int CART)` kernel if prompted.

## 4. Run the Workflow

Run the cells from top to bottom.

The notebook executes the following workflow:

1. Load `data/train.csv`.
2. Define four process features and one target label.
3. Plot the sample-set distribution.
4. Define the Ob-Int CART model.
5. Search Ob-Int CART hyperparameters using LOOCV.
6. Define the base CART model.
7. Search base CART hyperparameters using LOOCV.
8. Train the final base CART model and export its tree.
9. Report training-set RMSE and LOOCV RMSE.
10. Analyze training-set RMSE as a function of tree depth.

## 5. Normalization in LOOCV

Min-Max normalization is fitted inside each LOOCV fold using only the training subset:

```python
scaler = MinMaxScaler()
X_train_normalized = scaler.fit_transform(train_X)
X_val_scaled = scaler.transform(X_val)
```

This avoids information leakage from the held-out validation sample. The full-dataset normalization outside LOOCV is used only for final model fitting after hyperparameter selection.

## 6. Optional Command-Line Execution

The notebook can also be executed from the command line:

```bash
python scripts/run_notebook.py "Ob-Int CART.ipynb"
```

This creates:

```text
Ob-Int CART_executed.ipynb
```

If the notebook metadata points to an unavailable kernel, override it by setting `KERNEL_NAME`.

Windows PowerShell:

```powershell
$env:KERNEL_NAME="ob-int-cart"
python scripts/run_notebook.py "Ob-Int CART.ipynb"
```

Linux/macOS:

```bash
KERNEL_NAME=ob-int-cart python scripts/run_notebook.py "Ob-Int CART.ipynb"
```

## 7. Hyperparameter Search

For base CART:

```python
min_samples_split_vals = [1, 2, 3, 4, 5, 6, 7, 8]
```

For Ob-Int CART:

```python
min_samples_split_vals = [2, 3, 4, 5]
lambda_vals = np.linspace(0.05, 1.0, 96)
```

`lambda_` is the Ridge regression penalty coefficient used in the oblique splitting step. LOOCV RMSE is used as the model-selection criterion.

## 8. Output Interpretation

The notebook reports:

- Best hyperparameters for Ob-Int CART.
- Best hyperparameters for base CART.
- LOOCV RMSE for both models.
- Training-set RMSE for both models.
- Tree-depth-dependent training-set RMSE.

RMSE has the same unit as the target label `Jc_6`, i.e., MA/cm^2.

## 9. Graphviz Troubleshooting

The Python package `graphviz` is listed in `requirements.txt`, but tree rendering also requires the Graphviz system executable `dot`.

If `dot` is not installed or not on `PATH`, PDF/SVG tree rendering may fail. The notebook is designed to continue execution and save DOT source files instead:

```text
Ob_Int_CART.dot
cart_tree.dot
```

To render PDF/SVG trees, install Graphviz from:

```text
https://graphviz.org/download/
```

Then add the Graphviz `bin` directory to the system `PATH` and rerun the notebook.

## 10. Common Errors

### `FileNotFoundError: data/train.csv`

Download the dataset from the manuscript supporting information and place it at `data/train.csv`.

### `ModuleNotFoundError`

Install dependencies:

```bash
pip install -r requirements.txt
```

### Graphviz executable not found

Install system Graphviz or use the saved `.dot` files.
