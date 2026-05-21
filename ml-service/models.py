import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import json
import os

PROCESSED_DATA_PATH = "../data/processed_data.joblib"
MODELS_DIR = "../data/models"
RESULTS_PATH = "../data/model_results.json"

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

def load_data():
    return joblib.load(PROCESSED_DATA_PATH)

def train_logistic_regression(X_train, y_train, X_test, y_test):
    print("Training Intense Logistic Regression...")
    results = []
    solvers = ['liblinear', 'lbfgs', 'newton-cg']
    max_iters = [100, 500, 1000]

    best_acc = 0
    best_model = None

    for solver in solvers:
        for max_iter in max_iters:
            try:
                model = LogisticRegression(solver=solver, max_iter=max_iter, random_state=42, n_jobs=-1)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                
                results.append({
                    'model': 'Logistic Regression',
                    'params': {'solver': solver, 'max_iter': max_iter},
                    'metrics': {
                        'accuracy': acc,
                        'precision': precision_score(y_test, y_pred),
                        'recall': recall_score(y_test, y_pred),
                        'f1': f1_score(y_test, y_pred),
                        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
                    }
                })
                if acc > best_acc:
                    best_acc = acc
                    best_model = model
            except:
                continue

    joblib.dump(best_model, os.path.join(MODELS_DIR, 'logistic_regression.joblib'))
    return results

def train_decision_tree(X_train, y_train, X_test, y_test):
    print("Training Deep Decision Trees...")
    results = []
    depths = [5, 10, 20, None]
    min_splits = [2, 5, 10]
    criteria = ['gini', 'entropy']

    best_acc = 0
    best_model = None

    for depth in depths:
        for split in min_splits:
            for criterion in criteria:
                model = DecisionTreeClassifier(max_depth=depth, min_samples_split=split, criterion=criterion, random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                
                results.append({
                    'model': 'Decision Tree',
                    'params': {'max_depth': depth, 'min_samples_split': split, 'criterion': criterion},
                    'metrics': {
                        'accuracy': acc,
                        'precision': precision_score(y_test, y_pred),
                        'recall': recall_score(y_test, y_pred),
                        'f1': f1_score(y_test, y_pred),
                        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
                    }
                })
                if acc > best_acc:
                    best_acc = acc
                    best_model = model

    joblib.dump(best_model, os.path.join(MODELS_DIR, 'decision_tree.joblib'))
    return results

def train_mlp(X_train, y_train, X_test, y_test):
    print("Training High-Iter MLP...")
    results = []
    hidden_configs = [(100,), (100, 50), (128, 64, 32)]
    activations = ['relu', 'tanh']

    best_acc = 0
    best_model = None

    for layers in hidden_configs:
        for activation in activations:
            model = MLPClassifier(hidden_layer_sizes=layers, activation=activation, max_iter=200, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            
            results.append({
                'model': 'MLP',
                'params': {'hidden_layers': layers, 'activation': activation, 'max_iter': 200},
                'metrics': {
                    'accuracy': acc,
                    'precision': precision_score(y_test, y_pred),
                    'recall': recall_score(y_test, y_pred),
                    'f1': f1_score(y_test, y_pred),
                    'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
                    'loss_curve': model.loss_curve_
                }
            })
            if acc > best_acc:
                best_acc = acc
                best_model = model

    joblib.dump(best_model, os.path.join(MODELS_DIR, 'mlp.joblib'))
    return results

def train_ann(X_train, y_train, X_test, y_test):
    print("Training Ultra-Deep ANN (20 Epochs)...")
    results = []
    input_dim = X_train.shape[1]

    def create_ann(layers_config, activation, lr, dropout=0.2):
        model = Sequential()
        model.add(Dense(layers_config[0], input_shape=(input_dim,), activation=activation))
        model.add(Dropout(dropout))
        for neurons in layers_config[1:]:
            model.add(Dense(neurons, activation=activation))
            model.add(Dropout(dropout))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer=Adam(learning_rate=lr), loss='binary_crossentropy', metrics=['accuracy'])
        return model

    configs = [
        {'layers': [128, 64, 32], 'activation': 'relu', 'lr': 0.001, 'epochs': 20, 'batch_size': 64},
        {'layers': [256, 128], 'activation': 'relu', 'lr': 0.0005, 'epochs': 20, 'batch_size': 128}
    ]

    best_acc = 0
    best_model = None

    for config in configs:
        model = create_ann(config['layers'], config['activation'], config['lr'])
        history = model.fit(X_train, y_train, epochs=config['epochs'], batch_size=config['batch_size'], verbose=0, validation_split=0.2)
        
        y_pred_prob = model.predict(X_test)
        y_pred = (y_pred_prob > 0.5).astype(int).flatten()
        acc = accuracy_score(y_test, y_pred)
        
        results.append({
            'model': 'ANN',
            'params': config,
            'metrics': {
                'accuracy': acc,
                'precision': precision_score(y_test, y_pred),
                'recall': recall_score(y_test, y_pred),
                'f1': f1_score(y_test, y_pred),
                'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
                'loss_curve': history.history['loss'],
                'val_loss_curve': history.history['val_loss']
            }
        })
        if acc > best_acc:
            best_acc = acc
            best_model = model

    best_model.save(os.path.join(MODELS_DIR, 'ann.keras'))
    return results

def run_training():
    data = load_data()
    X_train, X_test, y_train, y_test = data['X_train'], data['X_test'], data['y_train'], data['y_test']
    
    all_results = []
    all_results.extend(train_logistic_regression(X_train, y_train, X_test, y_test))
    all_results.extend(train_decision_tree(X_train, y_train, X_test, y_test))
    all_results.extend(train_mlp(X_train, y_train, X_test, y_test))
    all_results.extend(train_ann(X_train, y_train, X_test, y_test))
    
    with open(RESULTS_PATH, 'w') as f:
        json.dump(all_results, f)
    
    print(f"Deep Training Completed. Results saved to {RESULTS_PATH}")
    return all_results

if __name__ == "__main__":
    run_training()
