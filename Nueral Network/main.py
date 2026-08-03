
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
 
from dataset import generate_synthetic_diabetes_dataset
from neural_network import train, predict
 
 
def main():
    dataset = generate_synthetic_diabetes_dataset()
    print(f"Generated synthetic dataset with {len(dataset)} rows.")
    print(f"Class balance -> Diabetic: {dataset['Outcome'].sum()}, Non-diabetic: {(dataset['Outcome']==0).sum()}\n")
    print("Parameters used:", ", ".join(dataset.columns[:-1]), "\n")
 
    features = dataset.drop('Outcome', axis=1).values.astype(float)
    labels = dataset['Outcome'].values.astype(float)
 
    # Standardize features
    feature_means = features.mean(axis=0)
    feature_stds = features.std(axis=0)
    features = (features - feature_means) / feature_stds
 
    train_features, test_features, train_labels, test_labels = train_test_split(
        features, labels, test_size=0.2, random_state=0
    )
 
    print("Training neural network...\n")
    model = train(train_features, train_labels, hidden_size=10, learning_rate=0.1, epochs=5000)
 
    predicted_labels = predict(test_features, model)
 
    accuracy = accuracy_score(test_labels, predicted_labels)
    report = classification_report(test_labels, predicted_labels)
 
    print(f"\nAccuracy: {accuracy * 100:.2f}%")
    print(report)
 
 
if __name__ == "__main__":
    main()