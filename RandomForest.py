# RandomForestRegressor

# Import libraries
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# Load dataset
diabetes = load_diabetes()

# Features and target
X = diabetes.data
y = diabetes.target

# Dataset information
print("Shape of Features :", X.shape)
print("Shape of Target   :", y.shape)

print("Feature Names")
print(diabetes.feature_names)

print("First 5 Features")
print(X[:5])

print("First 5 Target Values")
print(y[:5])

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
print("\nR2 Score :", r2_score(y_test, y_pred))
print("MAE      :", mean_absolute_error(y_test, y_pred))
print("MSE      :", mean_squared_error(y_test, y_pred))
print("RMSE     :", np.sqrt(mean_squared_error(y_test, y_pred)))

# Actual vs Predicted
plt.figure(figsize=(6,6))
plt.scatter(y_test, y_pred)
plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    color="red"
)
plt.title("Actual vs Predicted")
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.grid(True)
plt.show()

# Feature importance
importance = model.feature_importances_

plt.figure(figsize=(10,5))
plt.bar(diabetes.feature_names, importance)
plt.title("Feature Importance")
plt.xlabel("Features")
plt.ylabel("Importance")
plt.grid(True)
plt.show()

# Prediction error
error = y_test - y_pred

plt.figure(figsize=(6,5))
plt.scatter(y_test, error)
plt.axhline(y=0, color="red")
plt.title("Prediction Error")
plt.xlabel("Actual Values")
plt.ylabel("Error")
plt.grid(True)
plt.show()

plt.figure(figsize=(8,5))
plt.plot(y_test[:30], label="Actual", marker="o")
plt.plot(y_pred[:30], label="Predicted", marker="x")
plt.title("Actual vs Predicted (First 30 Samples)")
plt.xlabel("Samples")
plt.ylabel("Target")
plt.legend()
plt.grid(True)
plt.show()


# Random Forest Classification
# Import libraries
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay, classification_report

# Load breast cancer dataset
cancer = load_breast_cancer()

# Store feature and target values
X = cancer.data
y = cancer.target

# Check dataset shape
print("Shape of Features :", X.shape)
print("Shape of Target   :", y.shape)

# Print target names
print("\nTarget Names")
print(cancer.target_names)

# Print feature names
print("\nFeature Names")
print(cancer.feature_names)

# Display first 5 rows
print("\nFirst 5 Rows")
print(X[:5])

# Display first 5 target values
print("\nFirst 5 Target Values")
print(y[:5])

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Print accuracy
print("\nAccuracy :", accuracy_score(y_test, y_pred))

# Print confusion matrix
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix")
print(cm)

# Print classification report
print("\nClassification Report")
print(classification_report(y_test, y_pred))

# Plot confusion matrix
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=cancer.target_names
)

disp.plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.show()

# Plot feature importance
importance = model.feature_importances_

plt.figure(figsize=(12,5))
plt.bar(cancer.feature_names, importance)
plt.xticks(rotation=90)
plt.title("Feature Importance")
plt.xlabel("Features")
plt.ylabel("Importance")
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot class distribution
labels = cancer.target_names
sizes = [sum(y == 0), sum(y == 1)]

plt.figure(figsize=(6,6))
plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Class Distribution")
plt.show()

plt.figure(figsize=(10,4))
plt.plot(y_test[:30], "o-", label="Actual")
plt.plot(y_pred[:30], "x--", label="Predicted")

plt.title("Actual vs Predicted Classes")
plt.xlabel("Samples")
plt.ylabel("Class")
plt.legend()
plt.grid(True)
plt.show()

from sklearn.metrics import RocCurveDisplay
RocCurveDisplay.from_estimator(model, X_test, y_test)
plt.title("ROC Curve")
plt.grid(True)
plt.show()