'''
Oblique Interval CART
A CART-inspired decision tree that learns oblique splits via linear combinations of features and interval-based partitioning.

This implementation extends the classic Classification and Regression Tree (CART) algorithm by introducing oblique splits through linear combinations of features and interval-based partitioning instead of the traditional threshold-based splits. It enables more expressive decision boundaries, particularly useful for datasets where feature interactions significantly impact the target.

Features:
Oblique Splits: Learns linear combinations a₁·f₁ + a₂·f₂ to create richer decision boundaries.
Interval-Based Splitting: Splits data using intervals [left_bound, right_bound] instead of single thresholds.
Recursive Feature Combination: Dynamically builds composite features during tree construction and passes them down to child nodes.
Ridge Regularization: Uses ridge regression (alpha = lambda_) to stabilize linear weights.
Customizable: Supports both classification and regression tasks.
Visualization: Generates PDF/SVG graphs of the learned tree with interpretable labels.
Depth Analysis: Evaluates model performance per leaf depth or max depth.

File Structure (Suggested)
your-project/
├── Ob-Int CART.ipynb           # This file
├── README.md                   # This document
├── data/                       # Input data directory
│   └── train.csv               # Input data file
└── figures/                    # Output tree graphs

Contact & Contributions
Created by Guangyao Lin.
For bugs, feature requests, or improvements, please open an issue on GitHub.
This implementation is open-source and free to use under MIT license.
'''
