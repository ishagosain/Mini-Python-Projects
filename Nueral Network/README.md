# Diabetes Predictor Neural Network

A simple neural network built from scratch (no deep learning framework) to predict the likelihood of an individual having diabetes based on a synthetic dataset of health related features.

## Overview
The dataset contains synthetic information about individuals across 8 health related parameters. The target variable is `Outcome`, which indicates whether the individual has diabetes (1) or not (0). This project implements a basic 2 layer neural network using only NumPy to perform binary classification on this data.

## Parameters used
1. Age
2. Weight
3. Height
4. BMI (calculated from weight and height)
5. BloodPressure
6. Glucose
7. FamilyHistory (1 if a close relative has diabetes, 0 if not)
8. PhysicalActivity (hours of exercise per week)

## How it works
1. Generates a synthetic dataset using the parameters above, with a correlated diabetes outcome
2. Standardizes the features and splits the data into training and testing sets
3. Trains a neural network using forward propagation, backpropagation, and gradient descent
4. Evaluates the trained model on the test set using accuracy and a classification report

## Files
- `dataset.py` - generates the synthetic dataset
- `neural_network.py` - the neural network itself (forward/backward propagation, training loop, predict function)
- `main.py` - entry point that ties everything together and runs training + evaluation
- `requirements.txt` - project dependencies

All three `.py` files must be in the same folder since `main.py` imports from the other two.

## Requirements
```
pandas
numpy
scikit-learn
```

## Run it
```bash
pip install -r requirements.txt
python main.py
```