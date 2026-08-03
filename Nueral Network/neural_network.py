"""
A simple 2-layer neural network built from scratch with NumPy.
No deep learning framework used.
"""

import numpy as np


def create_model(num_features, hidden_size, num_outputs):
    np.random.seed(0)
    hidden_weights = np.random.randn(hidden_size, num_features) * np.sqrt(1 / num_features)
    hidden_bias = np.zeros((hidden_size, 1))
    output_weights = np.random.randn(num_outputs, hidden_size) * np.sqrt(1 / hidden_size)
    output_bias = np.zeros((num_outputs, 1))
    return {
        'hidden_weights': hidden_weights,
        'hidden_bias': hidden_bias,
        'output_weights': output_weights,
        'output_bias': output_bias
    }


def sigmoid(value):
    return 1 / (1 + np.exp(-value))


def forward_pass(features, model):
    hidden_weights = model['hidden_weights']
    hidden_bias = model['hidden_bias']
    output_weights = model['output_weights']
    output_bias = model['output_bias']

    hidden_input = np.dot(hidden_weights, features.T) + hidden_bias
    hidden_output = sigmoid(hidden_input)

    output_input = np.dot(output_weights, hidden_output) + output_bias
    predicted_prob = sigmoid(output_input)

    cache = {
        'hidden_output': hidden_output,
        'predicted_prob': predicted_prob
    }
    return predicted_prob, cache


def compute_loss(predicted_prob, actual_labels):
    num_samples = actual_labels.shape[0]
    actual_labels = actual_labels.reshape(1, -1)
    small_number = 1e-8  # avoid log(0)
    loss = -np.sum(
        actual_labels * np.log(predicted_prob + small_number)
        + (1 - actual_labels) * np.log(1 - predicted_prob + small_number)
    ) / num_samples
    return loss


def backward_pass(features, actual_labels, model, cache):
    num_samples = features.shape[0]
    actual_labels = actual_labels.reshape(1, -1)
    output_weights = model['output_weights']
    hidden_output = cache['hidden_output']
    predicted_prob = cache['predicted_prob']

    output_error = predicted_prob - actual_labels
    output_weights_gradient = np.dot(output_error, hidden_output.T) / num_samples
    output_bias_gradient = np.sum(output_error, axis=1, keepdims=True) / num_samples

    hidden_error = np.dot(output_weights.T, output_error)
    hidden_error = hidden_error * hidden_output * (1 - hidden_output)  # sigmoid derivative
    hidden_weights_gradient = np.dot(hidden_error, features) / num_samples
    hidden_bias_gradient = np.sum(hidden_error, axis=1, keepdims=True) / num_samples

    return {
        'hidden_weights_gradient': hidden_weights_gradient,
        'hidden_bias_gradient': hidden_bias_gradient,
        'output_weights_gradient': output_weights_gradient,
        'output_bias_gradient': output_bias_gradient
    }


def apply_gradients(model, gradients, learning_rate):
    model['hidden_weights'] -= learning_rate * gradients['hidden_weights_gradient']
    model['hidden_bias'] -= learning_rate * gradients['hidden_bias_gradient']
    model['output_weights'] -= learning_rate * gradients['output_weights_gradient']
    model['output_bias'] -= learning_rate * gradients['output_bias_gradient']
    return model


def train(features, labels, hidden_size=10, learning_rate=0.1, epochs=5000, print_every=500):
    model = create_model(features.shape[1], hidden_size, 1)
    for epoch in range(epochs):
        predicted_prob, cache = forward_pass(features, model)
        loss = compute_loss(predicted_prob, labels)
        gradients = backward_pass(features, labels, model, cache)
        model = apply_gradients(model, gradients, learning_rate)
        if epoch % print_every == 0:
            print(f"Epoch {epoch:5d} | Loss: {loss:.4f}")
    return model


def predict(features, model):
    predicted_prob, _ = forward_pass(features, model)
    return (predicted_prob > 0.5).astype(int).ravel()