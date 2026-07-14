import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Load inbuilt diabetes dataset
diabetes = load_diabetes()
X = diabetes.data
y = diabetes.target
print("Shape of Features :", X.shape)
print("Shape of Target   :", y.shape)

# Explore Dataset
print("Feature Names:\n")
print(diabetes.feature_names)
print("\nFirst Sample:\n")
print(X[0])
print("\nTarget Value:")
print(y[0])

# Visualize Target Distribution
plt.figure(figsize=(8,5))
plt.hist(y,bins=25,edgecolor='black')
plt.title("Distribution of Target")
plt.xlabel("Disease Progression")
plt.ylabel("Frequency")
plt.show()

# Scatter Plot
plt.figure(figsize=(8,5))
plt.scatter(X[:,2],y)
plt.xlabel("BMI")
plt.ylabel("Disease Progression")
plt.title("BMI vs Disease Progression")
plt.show()

# Train-Test Split
X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

class LinearRegressionScratch:
    def __init__(self,learning_rate=0.01,epochs=1000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None
        self.loss_history = []

    def fit(self,X,y):
        n_samples,n_features = X.shape
        # Initialize weights with zeros
        self.weights = np.zeros(n_features)
        self.bias = 0
        for epoch in range(self.epochs):
            # Step 1 : Predictions
            y_pred = np.dot(X,self.weights)+self.bias

            # Step 2 : Calculate Loss (MSE)
            loss = np.mean((y-y_pred)**2)
            self.loss_history.append(loss)

            # Step 3 : Compute Gradients
            dw = (-2/n_samples)*np.dot(X.T,(y-y_pred))
            db = (-2/n_samples)*np.sum(y-y_pred)

            # Step 4 : Update Parameters
            self.weights -= self.learning_rate*dw
            self.bias -= self.learning_rate*db

    def predict(self,X):
        return np.dot(X,self.weights)+self.bias

# Train Model
model = LinearRegressionScratch(learning_rate=0.1,
epochs=1000
)
model.fit(X_train,y_train)

# Predict
predictions = model.predict(X_test)

# Evaluate
mae = np.mean(np.abs(y_test - predictions))
mse = np.mean((y_test-predictions)**2)
rmse = np.sqrt(mse)
r2 = r2_score(y_test,predictions)

print("Mean Absolute Error :", round(mae, 2))
print("Mean Squared Error :", round(mse, 2))
print("Root Mean Squared Error :", round(rmse, 2))
print("R2 Score :", round(r2, 2))

# Loss Curve
plt.figure(figsize=(8,5))
plt.plot(model.loss_history,color='red')
plt.title("Loss Curve")
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.grid(True)
plt.show()

# Actual vs Predicted 
plt.figure(figsize=(7,5))
plt.scatter(y_test,predictions)
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("Actual vs Predicted")
plt.grid(True)
plt.show()