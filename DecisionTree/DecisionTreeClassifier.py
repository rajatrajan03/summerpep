import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Load dataset
iris = load_iris()
X = iris.data
y = iris.target

# Dataset info
print("Shape of Features :", X.shape)
print("Shape of Target :", y.shape)

# Feature names
print("Feature Names :", iris.feature_names)

# Target names
print("Target Classes :", iris.target_names)

# First five rows
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
model = DecisionTreeClassifier(
    criterion="gini",
    max_depth=3,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy :", accuracy)

# Classification report
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred,target_names=iris.target_names))

# Confusion matrix
# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,5))
plt.imshow(cm, cmap="Blues")

plt.title("Confusion Matrix")
plt.xlabel("Predicted Class")
plt.ylabel("Actual Class")

plt.xticks([0,1,2], iris.target_names)
plt.yticks([0,1,2], iris.target_names)

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, cm[i, j],
                 ha="center",
                 va="center",
                 fontsize=12,
                 fontweight="bold",
                 color="black")

plt.tight_layout()
plt.show()

# Feature importance
print("Feature Importance :")

for i in range(len(iris.feature_names)):
    print(f"{i+1}. {iris.feature_names[i]} : {model.feature_importances_[i]:.4f}")
# Tree depth
print("Tree Depth :", model.get_depth())

# Number of leaves
print("Number of Leaves :", model.get_n_leaves())

# Visualize decision tree
plt.figure(figsize=(14,8))
plot_tree(
    model,
    feature_names=iris.feature_names,
    class_names=iris.target_names,
    filled=True,
    rounded=True,
    fontsize=11
)

plt.title("Decision Tree Classifier")
plt.tight_layout()
plt.show()