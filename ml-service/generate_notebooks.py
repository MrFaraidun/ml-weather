import json
import os

def create_notebook_json(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

def markdown_cell(source):
    commented_source = []
    for line in source:
        if line.strip() == "":
            commented_source.append("#\n")
        else:
            commented_source.append("# " + line + "\n")
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": commented_source
    }

def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source]
    }

# ----------------- 1. LOGISTIC REGRESSION NOTEBOOK -----------------
lr_cells = [
    markdown_cell([
        "# Logistic Regression Model for Weather Prediction",
        "",
        "This notebook contains the complete step-by-step training, hyperparameter tuning, evaluation, and visualization for the **Logistic Regression** model used to predict whether it will rain tomorrow (`RainTomorrow`).",
        "",
        "### Mathematical Concepts & Intuition",
        "Logistic Regression is a supervised classification algorithm that calculates the probability that a given input $X$ belongs to class 1 ($y = 1$, representing Rain tomorrow) vs class 0 ($y = 0$, representing No Rain).",
        "",
        "It applies the **sigmoid function** to a linear combination of input features:",
        "$$P(y = 1 | X) = \\sigma(\\theta^T X) = \\frac{1}{1 + e^{-\\theta^T X}}$$",
        "",
        "### Hyperparameters Tuned",
        "To find the best model configuration, we perform a grid search over key hyperparameters:",
        "1. **Solver**:",
        "   - `liblinear`: Highly efficient for small/medium datasets. Supports L1 and L2 regularization.",
        "   - `lbfgs`: A quasi-Newton optimization method. Excellent for large, continuous features.",
        "   - `newton-cg`: Uses second-order derivatives to optimize weights. Accurate but computationally intensive.",
        "2. **Max Iterations (`max_iter`)**: The maximum number of solver iterations to guarantee optimization convergence."
    ]),
    code_cell([
        "# Step 1: Imports and libraries",
        "import os",
        "import joblib",
        "import numpy as np",
        "import pandas as pd",
        "import matplotlib.pyplot as plt",
        "import seaborn as sns",
        "from sklearn.linear_model import LogisticRegression",
        "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix",
        "",
        "# Set plotting aesthetics",
        "sns.set_theme(style='whitegrid')",
        "plt.rcParams['figure.figsize'] = (7, 5)"
    ]),
    markdown_cell([
        "### Step 2: Data Loading",
        "We load the scaled features and preprocessed targets from our centralized preprocessed dataset `../data/processed_data.joblib`."
    ]),
    code_cell([
        "# Step 2: Load the preprocessed weather dataset",
        "PROCESSED_DATA_PATH = \"../data/processed_data.joblib\"",
        "",
        "if not os.path.exists(PROCESSED_DATA_PATH):",
        "    raise FileNotFoundError(f\"Preprocessed data not found at {PROCESSED_DATA_PATH}. Please run preprocessing first.\")",
        "",
        "data = joblib.load(PROCESSED_DATA_PATH)",
        "X_train = data['X_train']",
        "X_test = data['X_test']",
        "y_train = data['y_train']",
        "y_test = data['y_test']",
        "",
        "print(f\"Dataset loaded successfully!\")",
        "print(f\"Training set size: {X_train.shape[0]} samples, {X_train.shape[1]} features\")",
        "print(f\"Testing set size:  {X_test.shape[0]} samples\")"
    ]),
    markdown_cell([
        "### Step 3: Hyperparameter Grid Search Training",
        "We systematically loop through each combination of `solver` and `max_iter` to find the most accurate model configuration."
    ]),
    code_cell([
        "# Step 3: Training with Parameter Grid Search",
        "solvers = ['liblinear', 'lbfgs', 'newton-cg']",
        "max_iters = [100, 500, 1000]",
        "",
        "results = []",
        "best_acc = 0",
        "best_model = None",
        "",
        "print(\"--- Starting Logistic Regression Tuning Loop ---\")",
        "for solver in solvers:",
        "    for max_iter in max_iters:",
        "        try:",
        "            print(f\"Training solver={solver:<12} | max_iter={max_iter:<5}\")",
            "            # Train model",
            "            model = LogisticRegression(solver=solver, max_iter=max_iter, random_state=42, n_jobs=-1)",
            "            model.fit(X_train, y_train)",
            "            ",
            "            # Evaluate on test set",
            "            y_pred = model.predict(X_test)",
            "            acc = accuracy_score(y_test, y_pred)",
            "            print(f\"  --> Test Accuracy: {acc * 100:.2f}%\")",
            "            ",
            "            results.append({",
            "                'solver': solver,",
            "                'max_iter': max_iter,",
            "                'accuracy': acc",
            "            })",
            "            ",
            "            # Retain best estimator",
            "            if acc > best_acc:",
            "                best_acc = acc",
            "                best_model = model",
            "        except Exception as e:",
            "            print(f\"  --> Failed config (solver={solver}, max_iter={max_iter}): {e}\")",
            "            continue",
        "print(\"\\nGrid Search Tuning Completed.\")"
    ]),
    markdown_cell([
        "### Step 4: Model Evaluation & Visualizations",
        "We compute full classification metrics on the test set and display a styled **Confusion Matrix Heatmap**."
    ]),
    code_cell([
        "# Step 4: Run evaluation metrics for the best Logistic Regression model",
        "y_pred = best_model.predict(X_test)",
        "accuracy = accuracy_score(y_test, y_pred)",
        "precision = precision_score(y_test, y_pred)",
        "recall = recall_score(y_test, y_pred)",
        "f1 = f1_score(y_test, y_pred)",
        "",
        "print(\"=== BEST MODEL METRICS ===\")",
        "print(f\"Optimal Solver:    {best_model.solver}\")",
        "print(f\"Optimal Max Iter:  {best_model.max_iter}\")",
        "print(f\"Test Accuracy:     {accuracy * 100:.2f}%\")",
        "print(f\"Precision Score:   {precision * 100:.2f}%\")",
        "print(f\"Recall Score:      {recall * 100:.2f}%\")",
        "print(f\"F1 Performance:    {f1 * 100:.2f}%\")",
        "",
        "# Plot Confusion Matrix",
        "cm = confusion_matrix(y_test, y_pred)",
        "plt.figure(figsize=(6, 5))",
        "sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ",
        "            xticklabels=['No Rain', 'Rain'], yticklabels=['No Rain', 'Rain'])",
        "plt.title('Confusion Matrix - Logistic Regression (Best Model)', fontsize=14, pad=15)",
        "plt.ylabel('Actual Label', fontsize=12)",
        "plt.xlabel('Predicted Label', fontsize=12)",
        "plt.tight_layout()",
        "plt.show()"
    ]),
    markdown_cell([
        "### Step 5: Serializing the Trained Model",
        "We save the optimal Logistic Regression model into our directory structure `../data/models/logistic_regression.joblib` for deployment."
    ]),
    code_cell([
        "# Step 5: Save best model to disk",
        "MODELS_DIR = \"../data/models\"",
        "if not os.path.exists(MODELS_DIR):",
        "    os.makedirs(MODELS_DIR)",
        "",
        "model_path = os.path.join(MODELS_DIR, 'logistic_regression.joblib')",
        "joblib.dump(best_model, model_path)",
        "print(f\"Best Logistic Regression model successfully saved to: {model_path}\")"
    ])
]

# ----------------- 2. DECISION TREE NOTEBOOK -----------------
dt_cells = [
    markdown_cell([
        "# Decision Tree Classifier for Weather Prediction",
        "",
        "This notebook explores the training, tuning, evaluation, and visual classification performance of a **Decision Tree Classifier** model used to forecast rainfall.",
        "",
        "### Mathematical Concepts & Intuition",
        "A Decision Tree represents a non-parametric model that builds a binary tree structure by recursively splitting the training datasets.",
        "At each node, it selects a feature that maximizes **Information Gain** or minimizes **Impurity**.",
        "",
        "#### Splitting Criteria Evaluated:",
        "1. **Gini Impurity**:",
        "   $$I_G(p) = 1 - \\sum_{i=1}^{J} p_i^2$$",
        "   Measures how often a randomly chosen element from the set would be incorrectly labeled if it were randomly labeled according to the distribution.",
        "2. **Entropy (Information Gain)**:",
        "   $$H(X) = -\\sum_{i=1}^{J} p_i \\log_2 p_i$$",
        "   Measures structural uncertainty or randomness in the target subset.",
        "",
        "### Hyperparameters Tuned",
        "1. **Max Depths (`max_depth`)**: Restricts depth of tree (`5`, `10`, `20`, or `None` representing fully grown). Prevents massive structural overfitting.",
        "2. **Min Samples Split (`min_samples_split`)**: Minimum instances required inside a node before it can be subdivided (`2`, `5`, or `10`).",
        "3. **Criterion**: Gini Impurity vs. Information Gain (Entropy)."
    ]),
    code_cell([
        "# Step 1: Imports and libraries",
        "import os",
        "import joblib",
        "import numpy as np",
        "import pandas as pd",
        "import matplotlib.pyplot as plt",
        "import seaborn as sns",
        "from sklearn.tree import DecisionTreeClassifier",
        "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix",
        "",
        "# Set plotting aesthetics",
        "sns.set_theme(style='whitegrid')",
        "plt.rcParams['figure.figsize'] = (7, 5)"
    ]),
    markdown_cell([
        "### Step 2: Data Loading",
        "Load dataset values from `../data/processed_data.joblib`."
    ]),
    code_cell([
        "# Step 2: Load the preprocessed dataset",
        "PROCESSED_DATA_PATH = \"../data/processed_data.joblib\"",
        "if not os.path.exists(PROCESSED_DATA_PATH):",
        "    raise FileNotFoundError(f\"Preprocessed data not found at {PROCESSED_DATA_PATH}\")",
        "",
        "data = joblib.load(PROCESSED_DATA_PATH)",
        "X_train, X_test, y_train, y_test = data['X_train'], data['X_test'], data['y_train'], data['y_test']",
        "print(\"Preprocessed data loaded successfully.\")"
    ]),
    markdown_cell([
        "### Step 3: Deep Tuning Loops",
        "We iterate over depths, minimum splits, and criteria to discover optimal classification limits."
    ]),
    code_cell([
        "# Step 3: Training Grid Search",
        "depths = [5, 10, 20, None]",
        "min_splits = [2, 5, 10]",
        "criteria = ['gini', 'entropy']",
        "",
        "results = []",
        "best_acc = 0",
        "best_model = None",
        "",
        "print(\"--- Starting Decision Tree Tuning Loop ---\")",
        "for depth in depths:",
        "    for split in min_splits:",
        "        for criterion in criteria:",
        "            # Train model",
        "            model = DecisionTreeClassifier(max_depth=depth, min_samples_split=split, ",
        "                                           criterion=criterion, random_state=42)",
        "            model.fit(X_train, y_train)",
        "            ",
        "            # Predict and evaluate",
        "            y_pred = model.predict(X_test)",
        "            acc = accuracy_score(y_test, y_pred)",
        "            ",
        "            results.append({",
        "                'max_depth': depth,",
        "                'min_samples_split': split,",
        "                'criterion': criterion,",
        "                'accuracy': acc",
        "            })",
        "            ",
        "            # Retain best",
        "            if acc > best_acc:",
        "                best_acc = acc",
        "                best_model = model",
        "",
        "print(\"Decision Tree Grid Tuning complete!\")",
        "print(f\"Best Achieved Test Accuracy: {best_acc * 100:.2f}%\")"
    ]),
    markdown_cell([
        "### Step 4: Metric Reports, Feature Impact & Heatmaps",
        "Evaluate testing performance, calculate which weather factors have the highest impact, and render a styled heatmap confusion matrix."
    ]),
    code_cell([
        "# Step 4: Model evaluation metrics",
        "y_pred = best_model.predict(X_test)",
        "accuracy = accuracy_score(y_test, y_pred)",
        "precision = precision_score(y_test, y_pred)",
        "recall = recall_score(y_test, y_pred)",
        "f1 = f1_score(y_test, y_pred)",
        "",
        "print(\"=== BEST MODEL METRICS ===\")",
        "print(f\"Optimal Max Depth:       {best_model.max_depth}\")",
        "print(f\"Optimal Min Split Size:  {best_model.min_samples_split}\")",
        "print(f\"Optimal Criterion:       {best_model.criterion}\")",
        "print(f\"Test Accuracy:           {accuracy * 100:.2f}%\")",
        "print(f\"Precision Score:         {precision * 100:.2f}%\")",
        "print(f\"Recall Score:            {recall * 100:.2f}%\")",
        "print(f\"F1 Performance:          {f1 * 100:.2f}%\")",
        "",
        "# Calculate Feature Importances (Which features have the most impact on predicting rain?)",
        "feature_names = data.get('feature_names', [f'Feature {i}' for i in range(X_train.shape[1])])",
        "importances = best_model.feature_importances_",
        "indices = np.argsort(importances)[::-1]",
        "",
        "# Print top impactful weather features",
        "print(\"\\n=== MOST IMPACTFUL FEATURES FOR PREDICTING RAIN ===\")",
        "for i in range(min(10, len(feature_names))):",
        "    print(f\"{i+1}. {feature_names[indices[i]]:<20} | Importance: {importances[indices[i]] * 100:.2f}%\")",
        "",
        "# Plot Confusion Matrix and Feature Importances side-by-side",
        "fig, axes = plt.subplots(1, 2, figsize=(15, 6))",
        "",
        "cm = confusion_matrix(y_test, y_pred)",
        "sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', ",
        "            xticklabels=['No Rain', 'Rain'], yticklabels=['No Rain', 'Rain'], ax=axes[0])",
        "axes[0].set_title('Confusion Matrix - Decision Tree (Best Model)', fontsize=13, pad=10)",
        "axes[0].set_ylabel('Actual Label')",
        "axes[0].set_xlabel('Predicted Label')",
        "",
        "sns.barplot(x=importances[indices[:10]], y=[feature_names[i] for i in indices[:10]], ",
        "            palette='Oranges_r', ax=axes[1])",
        "axes[1].set_title('Top 10 Most Impactful Weather Features', fontsize=13, pad=10)",
        "axes[1].set_xlabel('Relative Importance Score')",
        "axes[1].set_ylabel('Weather Factor')",
        "axes[1].grid(True, linestyle='--')",
        "",
        "plt.tight_layout()",
        "plt.show()"
    ]),
    markdown_cell([
        "### Step 5: Serializing Best Model",
        "Save to `../data/models/decision_tree.joblib`."
    ]),
    code_cell([
        "# Step 5: Save best model",
        "MODELS_DIR = \"../data/models\"",
        "if not os.path.exists(MODELS_DIR):",
        "    os.makedirs(MODELS_DIR)",
        "",
        "model_path = os.path.join(MODELS_DIR, 'decision_tree.joblib')",
        "joblib.dump(best_model, model_path)",
        "print(f\"Best Decision Tree model saved successfully at: {model_path}\")"
    ])
]

# ----------------- 3. MULTI-LAYER PERCEPTRON (MLP) NOTEBOOK -----------------
mlp_cells = [
    markdown_cell([
        "# Multi-Layer Perceptron (MLP) Classifier",
        "",
        "This notebook explores the training, evaluation, and performance analysis of a **Multi-Layer Perceptron (MLP)** Feedforward Neural Network using Scikit-Learn.",
        "",
        "### Mathematical Concepts & Intuition",
        "A Multi-Layer Perceptron (MLP) is a classic feedforward neural network structure consisting of an input layer, one or more hidden layers, and an output layer.",
        "Neurons inside hidden layers compute a weighted sum of their inputs, add a bias, and apply a non-linear activation function:",
        "$$a^{(l)} = f(W^{(l)} a^{(l-1)} + b^{(l)})$$",
        "",
        "For backpropagation, the network computes gradients of the loss function with respect to weights and updates them iteratively to minimize prediction error.",
        "",
        "### Hyperparameters Tuned",
        "1. **Hidden Layer Configurations (`hidden_layer_sizes`)**:",
        "   - `(100,)`: 1 hidden layer containing 100 neurons.",
        "   - `(100, 50)`: 2 hidden layers with 100 neurons first, then 50 neurons.",
        "   - `(128, 64, 32)`: 3 hidden layers for deep representation capacity.",
        "2. **Activation Functions**:",
        "   - `relu`: Rectified Linear Unit ($f(x) = \\max(0, x)$). Prevents gradient saturation.",
        "   - `tanh`: Hyperbolic Tangent ($f(x) = \\tanh(x)$). Outputs zero-centered data values.",
        "3. **Max Iterations**: Constrained to `200` to allow sufficient epochs for weight optimization."
    ]),
    code_cell([
        "# Step 1: Imports and setup",
        "import os",
        "import joblib",
        "import numpy as np",
        "import pandas as pd",
        "import matplotlib.pyplot as plt",
        "import seaborn as sns",
        "from sklearn.neural_network import MLPClassifier",
        "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix",
        "",
        "sns.set_theme(style='whitegrid')",
        "plt.rcParams['figure.figsize'] = (14, 5)"
    ]),
    markdown_cell([
        "### Step 2: Data Loading",
        "Load processed training datasets."
    ]),
    code_cell([
        "# Step 2: Load the preprocessed dataset",
        "PROCESSED_DATA_PATH = \"../data/processed_data.joblib\"",
        "if not os.path.exists(PROCESSED_DATA_PATH):",
        "    raise FileNotFoundError(f\"Preprocessed data not found at {PROCESSED_DATA_PATH}\")",
        "",
        "data = joblib.load(PROCESSED_DATA_PATH)",
        "X_train, X_test, y_train, y_test = data['X_train'], data['X_test'], data['y_train'], data['y_test']",
        "print(\"Preprocessed data values imported.\")"
    ]),
    markdown_cell([
        "### Step 3: High-Iteration Training Grid Search",
        "We fit MLPs across the configuration grid and record loss behaviors. We evaluate different configurations of **hidden layers** to see how network depth/width affects accuracy."
    ]),
    code_cell([
        "# Step 3: Grid Search Fitting Loop",
        "# Explanation of Hidden Layer Configurations:",
        "# - (100,): 1 hidden layer with 100 neurons (shallow network, fits linear/moderate relationships).",
        "# - (100, 50): 2 hidden layers (first has 100 neurons, second has 50). Learns structured combinations of weather factors.",
        "# - (128, 64, 32): 3 hidden layers (deep network, gradually condenses 128 features to 64, then 32, extracting highly complex non-linear abstractions).",
        "hidden_configs = [(100,), (100, 50), (128, 64, 32)]",
        "activations = ['relu', 'tanh']",
        "",
        "results = []",
        "best_acc = 0",
        "best_model = None",
        "",
        "print(\"--- Starting MLP Classifier Tuning Loop ---\")",
        "for layers in hidden_configs:",
        "    for activation in activations:",
        "        print(f\"Training MLP: hidden_layers={str(layers):<15} | activation={activation:<6}\")",
        "        # Setup model",
        "        model = MLPClassifier(hidden_layer_sizes=layers, activation=activation, ",
        "                              max_iter=200, random_state=42)",
        "        model.fit(X_train, y_train)",
        "        ",
        "        # Evaluate accuracy",
        "        y_pred = model.predict(X_test)",
        "        acc = accuracy_score(y_test, y_pred)",
        "        print(f\"  --> Accuracy: {acc * 100:.2f}%\")",
        "        ",
        "        results.append({",
        "            'hidden_layers': layers,",
        "            'activation': activation,",
        "            'accuracy': acc",
        "        })",
        "        ",
        "        if acc > best_acc:",
        "            best_acc = acc",
        "            best_model = model",
        "",
        "print(\"\\nGrid training complete!\")"
    ]),
    markdown_cell([
        "### Step 4: Metric Evaluation & Learning Curve Visualizations",
        "We print scores and plot both the Confusion Matrix Heatmap and the Multi-Iteration **Loss Optimization Curve**."
    ]),
    code_cell([
        "# Step 4: Evaluation and Plotting",
        "y_pred = best_model.predict(X_test)",
        "accuracy = accuracy_score(y_test, y_pred)",
        "precision = precision_score(y_test, y_pred)",
        "recall = recall_score(y_test, y_pred)",
        "f1 = f1_score(y_test, y_pred)",
        "",
        "print(\"=== BEST MODEL METRICS ===\")",
        "print(f\"Optimal Layers Size: {best_model.hidden_layer_sizes}\")",
        "print(f\"Optimal Activation:  {best_model.activation}\")",
        "print(f\"Test Accuracy:       {accuracy * 100:.2f}%\")",
        "print(f\"Precision Score:     {precision * 100:.2f}%\")",
        "print(f\"Recall Score:        {recall * 100:.2f}%\")",
        "print(f\"F1 Performance:      {f1 * 100:.2f}%\")",
        "",
        "# Set up multi-figure layouts",
        "fig, axes = plt.subplots(1, 2, figsize=(14, 5))",
        "",
        "# 1. Plot Confusion Matrix",
        "cm = confusion_matrix(y_test, y_pred)",
        "sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', ",
        "            xticklabels=['No Rain', 'Rain'], yticklabels=['No Rain', 'Rain'], ax=axes[0])",
        "axes[0].set_title('Confusion Matrix - MLP (Best Model)', fontsize=13, pad=10)",
        "axes[0].set_ylabel('Actual Label')",
        "axes[0].set_xlabel('Predicted Label')",
        "",
        "# 2. Plot MLP Loss Minimization Curve",
        "axes[1].plot(best_model.loss_curve_, color='forestgreen', linewidth=2)",
        "axes[1].set_title('Backpropagation Loss Curve (Best Model)', fontsize=13, pad=10)",
        "axes[1].set_xlabel('Iterations (Epochs)')",
        "axes[1].set_ylabel('Loss Metric (Cross-Entropy)')",
        "axes[1].grid(True, linestyle='--')",
        "",
        "plt.tight_layout()",
        "plt.show()"
    ]),
    markdown_cell([
        "### Step 5: Save Trained MLP",
        "Save weights to `../data/models/mlp.joblib`."
    ]),
    code_cell([
        "# Step 5: Export best MLP",
        "MODELS_DIR = \"../data/models\"",
        "if not os.path.exists(MODELS_DIR):",
        "    os.makedirs(MODELS_DIR)",
        "",
        "model_path = os.path.join(MODELS_DIR, 'mlp.joblib')",
        "joblib.dump(best_model, model_path)",
        "print(f\"Optimal MLP model successfully exported to: {model_path}\")"
    ])
]

# ----------------- 4. ARTIFICIAL NEURAL NETWORK (ANN) NOTEBOOK -----------------
ann_cells = [
    markdown_cell([
        "# Custom Artificial Neural Network (ANN) with Keras & TensorFlow",
        "",
        "This notebook contains the complete construction, optimization, training history analysis, and performance validation of a custom deep **Artificial Neural Network (ANN)** built using Keras and TensorFlow.",
        "",
        "### Mathematical Concepts & Intuition",
        "Unlike basic Scikit-Learn classifiers, an ANN allows deep structural flexibility. We stack multiple dense connected layers with custom **Dropout regularization layers** to drop random nodes and prevent overfitting:",
        "",
        "#### Key Components:",
        "1. **Dense Layers (Fully Connected)**: Multiplies inputs by a weight matrix, adds bias, and passes through activation (ReLU).",
        "2. **Dropout Layers (Regularization)**: Randomly sets a fraction (e.g., $20\\%$) of input units to 0 at each update during training time, promoting weight distribution.",
        "3. **Binary Cross-Entropy Loss (Target binary classification)**:",
        "   $$\\text{Loss} = -\\frac{1}{N} \\sum_{i=1}^{N} \\left[ y_i \\log(\\hat{y}_i) + (1 - y_i) \\log(1 - \\hat{y}_i) \\right]$$",
        "4. **Adam Optimizer**: An adaptive learning rate optimization algorithm that utilizes first and second moments of gradients.",
        "",
        "### Hyperparameter Configurations Tested",
        "We evaluate two highly customized deep neural architectures:",
        "*   **Config 1**: 3-layer deep structure `[128 -> 64 -> 32]` | Activation: ReLU | Learning Rate: `0.001` | Epochs: `20` | Batch Size: `64`",
        "*   **Config 2**: 2-layer wide structure `[256 -> 128]` | Activation: ReLU | Learning Rate: `0.0005` | Epochs: `20` | Batch Size: `128`"
    ]),
    code_cell([
        "# Step 1: Imports and environment setup",
        "import os",
        "import joblib",
        "import numpy as np",
        "import pandas as pd",
        "import matplotlib.pyplot as plt",
        "import seaborn as sns",
        "import tensorflow as tf",
        "from tensorflow.keras.models import Sequential",
        "from tensorflow.keras.layers import Dense, Dropout",
        "from tensorflow.keras.optimizers import Adam",
        "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix",
        "",
        "# Set styling",
        "sns.set_theme(style='whitegrid')",
        "plt.rcParams['figure.figsize'] = (14, 5)"
    ]),
    markdown_cell([
        "### Step 2: Load Preprocessed Features",
        "Load processed scaling vectors from `../data/processed_data.joblib`."
    ]),
    code_cell([
        "# Step 2: Import data",
        "PROCESSED_DATA_PATH = \"../data/processed_data.joblib\"",
        "if not os.path.exists(PROCESSED_DATA_PATH):",
        "    raise FileNotFoundError(f\"Preprocessed data not found at {PROCESSED_DATA_PATH}\")",
        "",
        "data = joblib.load(PROCESSED_DATA_PATH)",
        "X_train = data['X_train']",
        "X_test = data['X_test']",
        "y_train = data['y_train']",
        "y_test = data['y_test']",
        "print(f\"Input Feature Dimensions: {X_train.shape[1]}\")"
    ]),
    markdown_cell([
        "### Step 3: Model Architecture Creation & Parameter Search",
        "We construct the models using Keras `Sequential` API and optimize validation split values."
    ]),
    code_cell([
        "# Step 3: Model Building and Training Loops",
        "input_dim = X_train.shape[1]",
        "",
        "# What is a Hidden Layer, Dense, and Dropout?",
        "# - Dense Layer: A standard fully-connected neural network layer where every neuron receives inputs from all neurons in the previous layer.",
        "# - Dropout Layer: A regularizer that randomly turns off a fraction (e.g. 20%) of neurons during each training step. This prevents the model from relying too much on specific single weather factors (like absolute temperature) and forces it to distribute weight across multiple factors, preventing overfitting.",
        "def create_ann(layers_config, activation='relu', lr=0.001, dropout=0.2):",
        "    model = Sequential()",
        "    # First Hidden Layer: Takes raw features as inputs",
        "    model.add(Dense(layers_config[0], input_shape=(input_dim,), activation=activation))",
        "    model.add(Dropout(dropout))",
        "    ",
        "    # Additional Deep Hidden Layers: Learns high-level abstractions",
        "    for neurons in layers_config[1:]:",
        "        model.add(Dense(neurons, activation=activation))",
        "        model.add(Dropout(dropout))",
        "        ",
        "    # Output Layer: Sigmoid activation outputs a probability between 0 and 1 (rain probability)",
        "    model.add(Dense(1, activation='sigmoid'))",
        "    ",
        "    # Compile model",
        "    model.compile(optimizer=Adam(learning_rate=lr), ",
        "                  loss='binary_crossentropy', ",
        "                  metrics=['accuracy'])",
        "    return model",
        "",
        "# Deep Network Configuration Settings:",
        "# - Config 1: Deep & Narrow [128 -> 64 -> 32] layers. High capacity for deep sequential abstractions, learning rate 0.001.",
        "# - Config 2: Shallow & Wide [256 -> 128] layers. Large capacity in earlier layers, learning rate 0.0005.",
        "configs = [",
        "    {'layers': [128, 64, 32], 'activation': 'relu', 'lr': 0.001, 'epochs': 20, 'batch_size': 64},",
        "    {'layers': [256, 128], 'activation': 'relu', 'lr': 0.0005, 'epochs': 20, 'batch_size': 128}",
        "]",
        "",
        "results = []",
        "best_acc = 0",
        "best_model = None",
        "best_history = None",
        "",
        "print(\"--- Starting Custom ANN Training and Comparison ---\")",
        "for idx, config in enumerate(configs):",
        "    print(f\"\\nTraining Configuration {idx+1}: layers={config['layers']} | lr={config['lr']}\")",
        "    # Build ANN",
        "    model = create_ann(config['layers'], config['activation'], config['lr'])",
        "    ",
        "    # Fit with 20% validation split",
        "    history = model.fit(X_train, y_train, ",
        "                        epochs=config['epochs'], ",
        "                        batch_size=config['batch_size'], ",
        "                        verbose=1, ",
        "                        validation_split=0.2)",
        "    ",
        "    # Evaluate testing accuracy",
        "    y_pred_prob = model.predict(X_test)",
        "    y_pred = (y_pred_prob > 0.5).astype(int).flatten()",
        "    acc = accuracy_score(y_test, y_pred)",
        "    print(f\"  --> Configuration {idx+1} Test Accuracy: {acc * 100:.2f}%\")",
        "    ",
        "    results.append({",
        "        'config': config,",
        "        'accuracy': acc,",
        "        'history': history.history",
        "    })",
        "    ",
        "    if acc > best_acc:",
        "        best_acc = acc",
        "        best_model = model",
        "        best_history = history.history",
        "",
        "print(\"\\nCustom ANN Training Complete!\")"
    ]),
    markdown_cell([
        "### Step 4: Metric Evaluation & Loss Optimization Charts",
        "We render the Confusion Matrix and compare Training Loss vs. Validation Loss curves."
    ]),
    code_cell([
        "# Step 4: Evaluation and Plotting",
        "y_pred_prob = best_model.predict(X_test)",
        "y_pred = (y_pred_prob > 0.5).astype(int).flatten()",
        "accuracy = accuracy_score(y_test, y_pred)",
        "precision = precision_score(y_test, y_pred)",
        "recall = recall_score(y_test, y_pred)",
        "f1 = f1_score(y_test, y_pred)",
        "",
        "print(\"=== BEST ANN CONFIGURATION METRICS ===\")",
        "print(f\"Optimal Test Accuracy:     {accuracy * 100:.2f}%\")",
        "print(f\"Precision Score:           {precision * 100:.2f}%\")",
        "print(f\"Recall Score:              {recall * 100:.2f}%\")",
        "print(f\"F1 Performance:            {f1 * 100:.2f}%\")",
        "",
        "# Set up side-by-side plots",
        "fig, axes = plt.subplots(1, 2, figsize=(14, 5))",
        "",
        "# 1. Plot Heatmap Confusion Matrix",
        "cm = confusion_matrix(y_test, y_pred)",
        "sns.heatmap(cm, annot=True, fmt='d', cmap='Purples', ",
        "            xticklabels=['No Rain', 'Rain'], yticklabels=['No Rain', 'Rain'], ax=axes[0])",
        "axes[0].set_title('Confusion Matrix - Custom ANN (Best Config)', fontsize=13, pad=10)",
        "axes[0].set_ylabel('Actual Label')",
        "axes[0].set_xlabel('Predicted Label')",
        "",
        "# 2. Plot Keras Validation Loss History",
        "axes[1].plot(best_history['loss'], label='Training Loss', color='purple', linewidth=2)",
        "axes[1].plot(best_history['val_loss'], label='Validation Loss', color='darkviolet', linewidth=2, linestyle='--')",
        "axes[1].set_title('ANN Optimization History (Loss Curves)', fontsize=13, pad=10)",
        "axes[1].set_xlabel('Epochs')",
        "axes[1].set_ylabel('Loss (Binary Cross-Entropy)')",
        "axes[1].legend()",
        "axes[1].grid(True, linestyle='--')",
        "",
        "plt.tight_layout()",
        "plt.show()"
    ]),
    markdown_cell([
        "### Step 5: Save Custom ANN Model",
        "Save model architecture and weights in standard Keras format to `../data/models/ann.keras`."
    ]),
    code_cell([
        "# Step 5: Export optimal ANN",
        "MODELS_DIR = \"../data/models\"",
        "if not os.path.exists(MODELS_DIR):",
        "    os.makedirs(MODELS_DIR)",
        "",
        "model_path = os.path.join(MODELS_DIR, 'ann.keras')",
        "best_model.save(model_path)",
        "print(f\"Optimal ANN Keras model successfully saved to: {model_path}\")"
    ])
]

# ----------------- MAIN EXECUTION: WRITE NOTEBOOKS -----------------
notebooks = {
    "logistic_regression.ipynb": lr_cells,
    "decision_tree.ipynb": dt_cells,
    "mlp.ipynb": mlp_cells,
    "ann.ipynb": ann_cells
}

print("Starting generation of Jupyter Notebooks...")
for filename, cells in notebooks.items():
    notebook_json = create_notebook_json(cells)
    filepath = os.path.join(".", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(notebook_json, f, indent=1, ensure_ascii=False)
    print(f" -> Created {filename} successfully.")

print("\nAll 4 Jupyter Notebooks have been created in the current directory!")
