# Oblique-Interval CART (Ob-Int CART)

This repository provides the computational workflow used to train, validate, compare, and visualize an oblique-interval extension of the classic Classification and Regression Tree (CART) model for PLD-grown EuBCO films.

The implementation is designed for small experimental materials datasets where the process-property relationship is both non-monotonic and coupled. Instead of using only traditional point-threshold splits, Ob-Int CART combines:

- **Interval-based splitting**, which separates samples according to whether a feature or projection score lies within a learned interval `[left_bound, right_bound]`.
- **Oblique splitting**, which uses regularized linear combinations of features to represent coupled process-parameter effects.
- **Ridge regularization**, controlled by `lambda_`, to stabilize the oblique splitting weights.
- **Leave-one-out cross-validation (LOOCV)** for hyperparameter selection on the small experimental dataset.
- **Base CART comparison**, using the same validation strategy.

## Repository Structure

```text
Ob-Int-CART-main/
|-- Ob-Int CART.ipynb          # Main Jupyter Notebook
|-- data/
|   `-- README.md              # Dataset access instructions and column definitions
|-- figures/
|   `-- README.md              # Tree-output description
|-- docs/
|   `-- OPERATING_GUIDE.md     # Step-by-step execution and troubleshooting guide
|-- scripts/
|   `-- run_notebook.py        # Optional command-line notebook execution helper
|-- requirements.txt           # Python dependencies
|-- LICENSE
`-- readme.md
```

## Dataset

The experimental dataset is **not included in this GitHub repository**. It is provided as supporting information for the manuscript:

```text
Interpretable decision tree-assisted optimization of PLD growth of EuBa2Cu3O7-delta films
```

After downloading the supporting dataset, place it at:

```text
data/train.csv
```

The notebook expects 16 experimental samples with four input features:

| Column | Meaning | Unit |
|---|---|---|
| `laser energy` | Laser pulse energy during PLD | mJ |
| `oxygen pressure` | Oxygen partial pressure during deposition | mTorr |
| `deposition_temp` | Deposition temperature | degree C |
| `TD_distance` | Target-to-substrate distance | mm |

The target label is:

| Column | Meaning | Unit |
|---|---|---|
| `Jc_6` | Critical current density at 50 K and 6 T | MA/cm^2 |

The sample-set distribution is visualized in the notebook by plotting histograms for the four input features.

## Environment Setup

Python 3.10 is recommended. Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Optional: register the environment as a Jupyter kernel:

```bash
python -m ipykernel install --user --name ob-int-cart --display-name "Python (Ob-Int CART)"
```

## Running the Notebook

Start JupyterLab or Jupyter Notebook in the repository root:

```bash
jupyter lab
```

Open:

```text
Ob-Int CART.ipynb
```

Then run the cells sequentially. The notebook performs the following operations:

1. Load data/train.csv.
2. Define the input features and target label.
3. Visualize the sample-set distribution.
4. Define the Ob-Int CART model.
5. Perform nested CV for Ob-Int CART.
6. Define the base CART model.
7. Perform the same nested CV procedure for the base CART model.
8. Train the final models using the selected hyperparameters.
9. Export and visualize the resulting decision trees.
10. Report nested-CV RMSE and fold-wise RMSE statistics for model comparison.
11. Analyze RMSE variation with tree depth and model configuration.

The notebook metadata may retain a local kernel name from the development computer. If the kernel is not found, select `Python (Ob-Int CART)` manually in JupyterLab, or use the command-line runner with `KERNEL_NAME=ob-int-cart`.

##Nested Cross-Validation

To obtain an unbiased estimate of model generalization performance while optimizing the model hyperparameters, the notebook employs a nested cross-validation (nested CV) framework.

The nested CV consists of:

Complete dataset 
        |
        |-- Outer leave 2 out CV
        |     |
        |     |-- outer training set
        |     |
        |     `-- outer test set
        |
        `-- Inner LOOCV 
              |
              |-- inner training set
              |
              `-- inner validation set

Outer leave 2 out Cross-Validation

Leave 2 out cross-validation (L2OCV) is used in the outer loop. For a dataset containing (n) samples, all possible pairs of samples are successively held out as independent test sets.

Inner Leave-One-Out Cross-Validation

For each outer fold, hyperparameter optimization is performed exclusively on the samples in the outer training set.

An inner LOOCV procedure is applied:

LOOCV outer-training samples
        |
        |-- inner model training
        |
        `-- 1 sample  -> inner validation

The hyperparameter configuration yielding the minimum inner RMSE is selected for that outer fold.

The selected hyperparameters are then used to retrain the model using all outer-training samples. The resulting model is evaluated on the two previously unseen outer test samples.

## Normalization and Data Leakage Control

For LOOCV, Min-Max normalization is performed **inside each fold**. In each fold, the scaler is fitted only on the training subset and then applied to the held-out validation sample:

```python
scaler = MinMaxScaler()
X_train_normalized = scaler.fit_transform(train_X)
X_val_scaled = scaler.transform(X_val)
```

This fold-wise normalization avoids information leakage from the held-out validation sample. A separate full-dataset normalization is used only after hyperparameter selection for fitting the final model and describing training-set fitting behavior.

## Hyperparameters

For the base CART model, the minimum number of samples required for a split is treated as the hyperparameter:

```python
min_samples_split_vals = [1, 2, 3, 4, 5, 6, 7, 8]
```

For the Ob-Int CART model, two hyperparameters are selected:

```python
min_samples_split_vals = [2, 3, 4, 5]
lambda_vals = np.linspace(0.05, 1.0, 96)
```

Here, `lambda_` is the Ridge regression penalty coefficient used to estimate the weights of the oblique splitting feature. The optimal hyperparameters are selected by minimizing LOOCV RMSE.

## Algorithmic Workflow

At each node, the model evaluates candidate splits by minimizing the weighted mean squared error (MSE) of the child nodes.

### Interval Split

For a splitting score `s`, Ob-Int CART searches for an interval:

```text
left_bound <= s <= right_bound
```

Samples inside this interval are assigned to one child node, and samples outside the interval are assigned to the other child node. This allows a single node to represent a finite high-performance process window.

### Oblique Split

After the root node, the splitting score can be a linear combination of the latest generated projection feature and a remaining raw feature:

```text
s = a1 * z_previous + a2 * x_j
```

The weights `a1` and `a2` are estimated using Ridge regression. The resulting projection score is then evaluated using the same interval-splitting strategy.

### Leaf Prediction

For regression, each terminal node predicts the mean `Jc_6` value of the samples assigned to that leaf.

## Output Files

Depending on the local environment, the notebook may generate tree visualization files:

```text
Ob_Int_CART.pdf or Ob_Int_CART.dot
cart_tree.pdf or cart_tree.dot
```

If the Graphviz executable `dot` is not installed, the notebook saves `.dot` source files instead of stopping execution. Install Graphviz and add its `bin` directory to `PATH` if PDF/SVG tree rendering is required.

## Reproducibility Notes

- The dataset should be obtained from the manuscript supporting information and placed at `data/train.csv`.
- The full model implementation is contained in `Ob-Int CART.ipynb`.
- LOOCV is used because the dataset contains only 16 experimental samples.
- RMSE is reported in the same unit as the target label, i.e., MA/cm^2.
- The repository includes the preprocessing, model implementation, hyperparameter selection, comparison, tree visualization, and metric-reporting procedures required to reproduce the computational workflow.

## Troubleshooting

See:

```text
docs/OPERATING_GUIDE.md
```

for detailed operating instructions and common issues.

## License

This implementation is released under the MIT License.

## Contact

Created by Guangyao Lin. For bugs, questions, or feature requests, please open an issue on GitHub.
