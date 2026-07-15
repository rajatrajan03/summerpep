import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
diabetes = load_diabetes()
X = diabetes.data
y = diabetes.target

# Dataset info
print("Shape of Features :", X.shape)
print("Shape of Target :", y.shape)

# Feature names
print("Feature Names :", diabetes.feature_names)

# First 5 Rows
print("First 5 Rows :")
print(X[:5])

print("First 5 Targets :")
print(y[:5])

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = DecisionTreeRegressor(
    max_depth=3,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("MAE :", round(mae,2))
print("MSE :", round(mse,2))
print("RMSE :", round(rmse,2))
print("R2 Score :", round(r2,4))

# Actual vs Predicted
plt.figure(figsize=(7,5))
plt.scatter(y_test, y_pred)

plt.plot(
    [y.min(), y.max()],
    [y.min(), y.max()],
    color="red",
    linewidth=2
)

plt.title("Actual vs Predicted")
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")

plt.grid(True)
plt.tight_layout()
plt.show()

# Feature importance
print("Feature Importance :")

for i in range(len(diabetes.feature_names)):
    print(f"{i+1}. {diabetes.feature_names[i]} : {model.feature_importances_[i]:.4f}")

# Tree depth
print("Tree Depth :", model.get_depth())

# Number of leaves
print("Number of Leaves :", model.get_n_leaves())

# Visualize tree
plt.figure(figsize=(18,10))

plot_tree(
    model,
    feature_names=diabetes.feature_names,
    filled=True,
    rounded=True,
    fontsize=9
)

plt.title("Decision Tree Regressor")
plt.tight_layout()
plt.show()