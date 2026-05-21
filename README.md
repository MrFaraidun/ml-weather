# 🌦️ Machine Learning Weather Prediction System

A complete 3-tier web application that predicts weather conditions using various Machine Learning models (Logistic Regression, Decision Trees, Multi-Layer Perceptron, and Artificial Neural Networks).

---

## 🏛️ Project Architecture

The system consists of three main components:
1. **Frontend (`/client`)**: A React application built with Vite providing interactive UI visualizations.
2. **Middleware API (`/server`)**: A Node.js & Express API serving as a gateway, routing requests and managing middleware logic.
3. **ML Service (`/ml-service`)**: A Python-based Flask service that trains, runs, and serves predictions from four machine learning models.

---

## 🤖 Machine Learning Models
The ML service evaluates and runs four models:
* **Logistic Regression**
* **Decision Tree Classifier**
* **Multi-Layer Perceptron (MLP)**
* **Artificial Neural Network (ANN)**

Detailed Jupyter Notebooks for each model (with mathematical theory, hyperparameter grid search tuning, Seaborn heatmaps, and model saving steps) can be found in `ml-service/`.

---

## 🚀 Getting Started

We provide a convenient startup script to run all services simultaneously.

### Prerequisites
Ensure you have the following installed:
* **Node.js** (v18+)
* **Python 3.10+** (with virtual environment support)

### Run all services in development mode
Simply execute the startup script from the root directory:
```bash
./start_project.sh
```
This script will automatically:
1. Kill any existing processes running on ports `3001` (Node), `5000` (Flask), and `5173` (Vite).
2. Activate the Python virtual environment and launch the Flask ML service on port `5000`.
3. Start the Express middleware server on port `3001`.
4. Start the Vite React development server on port `5173` and launch the UI.

Press `Ctrl + C` in the terminal to clean up and shut down all services safely.
