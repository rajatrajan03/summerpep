import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Load Dataset
data = load_breast_cancer()

X = data.data[:, :2]
y = data.target

print("Shape of Features :", X.shape)
print("Shape of Target   :", y.shape)

# Dataset Plot
plt.figure(figsize=(7,6))
plt.scatter(X[:,0], X[:,1], c=y, cmap="bwr", edgecolors="k")
plt.xlabel(data.feature_names[0])
plt.ylabel(data.feature_names[1])
plt.title("Breast Cancer Dataset")
plt.show()

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Feature Scaling
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

class LogisticRegressionScratch:

    # Constructor
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None
        self.losses = []

    # Sigmoid Function
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    # Train Model
    def fit(self, X, y):

        n_samples, n_features = X.shape

        self.weights = np.zeros(n_features)
        self.bias = 0

        for epoch in range(self.epochs):

            linear_model = np.dot(X, self.weights) + self.bias

            predictions = self.sigmoid(linear_model)

            loss = -np.mean(
                y * np.log(predictions + 1e-9) +
                (1-y) * np.log(1-predictions + 1e-9)
            )

            self.losses.append(loss)

            dw = (1/n_samples) * np.dot(X.T, (predictions-y))
            db = (1/n_samples) * np.sum(predictions-y)

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

            if epoch % 100 == 0:
                print(f"Epoch {epoch} Loss : {loss:.4f}")

    # Predict Probability
    def predict_proba(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        return self.sigmoid(linear_model)

    # Predict Class
    def predict(self, X):
        probabilities = self.predict_proba(X)
        return (probabilities >= 0.5).astype(int)

# Train Model
model = LogisticRegressionScratch(
    learning_rate=0.01,
    epochs=1000
)

model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy :", accuracy)

# Loss Curve
plt.figure(figsize=(7,5))
plt.plot(model.losses)
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training Loss")
plt.grid(True)
plt.show()

# Decision Boundary
# w1*x1 + w2*x2 + b = 0

x_min, x_max = X_train[:,0].min()-1, X_train[:,0].max()+1
y_min, y_max = X_train[:,1].min()-1, X_train[:,1].max()+1

xx, yy = np.meshgrid(
    np.arange(x_min, x_max, 0.02),
    np.arange(y_min, y_max, 0.02)
)

grid = np.c_[xx.ravel(), yy.ravel()]

Z = model.predict(grid)
Z = Z.reshape(xx.shape)

plt.figure(figsize=(8,6))
plt.contourf(xx, yy, Z, alpha=0.3, cmap="bwr")
plt.scatter(X_train[:,0], X_train[:,1], c=y_train, cmap="bwr", edgecolors="k")
plt.xlabel(data.feature_names[0])
plt.ylabel(data.feature_names[1])
plt.title("Decision Boundary")
plt.show()