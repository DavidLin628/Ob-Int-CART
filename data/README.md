# Dataset Access and Schema

The experimental dataset is not included in this GitHub repository. It is provided as supporting information for the manuscript:

```text
Interpretable decision tree-assisted optimization of PLD growth of EuBa2Cu3O7-delta films
```

After downloading the supporting dataset, place it in this directory as:

```text
data/train.csv
```

## Expected Columns

| Column | Role | Description | Unit |
|---|---|---|---|
| `sample id` | identifier | Sample index | none |
| `laser energy` | feature | Laser pulse energy used during PLD | mJ |
| `oxygen pressure` | feature | Oxygen partial pressure during PLD growth | mTorr |
| `deposition_temp` | feature | Deposition temperature | degree C |
| `TD_distance` | feature | Target-to-substrate distance | mm |
| `Jc_6` | target | Critical current density measured at 50 K and 6 T | MA/cm^2 |

## Dataset Size

The dataset used in the manuscript contains 16 experimental samples.

## Use in the Notebook

The notebook reads the file with:

```python
train_set = pd.read_csv("data/train.csv")
```

The feature matrix is:

```python
features = ["laser energy", "oxygen pressure", "deposition_temp", "TD_distance"]
X = np.array(train_set[features])
```

The regression target is:

```python
y = np.array(train_set["Jc_6"])
```

## Preprocessing and Leakage Control

For LOOCV, Min-Max normalization is performed inside each fold. The scaler is fitted only on the training subset and then applied to the held-out validation sample:

```python
scaler = MinMaxScaler()
X_train_normalized = scaler.fit_transform(train_X)
X_val_scaled = scaler.transform(X_val)
```

This avoids information leakage from the validation sample. A separate full-dataset normalization is used only after hyperparameter selection for final model fitting and training-set fitting analysis.
