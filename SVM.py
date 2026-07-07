import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.inspection import DecisionBoundaryDisplay

# Load Dataset
cancer = load_breast_cancer()
X = cancer.data[:, :2]
y = cancer.target

print("Features :", cancer.feature_names[:2])
print("Samples :", X.shape[0])
print("Classes :", cancer.target_names)

# Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Train Model
svm = SVC(kernel="linear", C=1, probability=True)
svm.fit(X_train, y_train)

# Prediction
y_pred = svm.predict(X_test)

# Evaluation
print("\nAccuracy :", accuracy_score(y_test, y_pred))

print("\nClassification Report\n")
print(classification_report(y_test, y_pred))

print("Confusion Matrix\n")
print(confusion_matrix(y_test, y_pred))

# Support Vectors
print("\nNumber of Support Vectors :", len(svm.support_vectors_))
print("Support Vectors Per Class :", svm.n_support_)

# Hyperplane
w = svm.coef_[0]
b = svm.intercept_[0]

print("\nWeights :", w)
print("Bias :", b)

print("\nHyperplane Equation")
print(f"{w[0]:.4f}x1 + {w[1]:.4f}x2 + {b:.4f} = 0")

# Margin
margin = 2 / np.linalg.norm(w)

print("\nMargin :", margin)
print("||w|| :", np.linalg.norm(w))

# Decision Function
print("\nDecision Function Values")
print(svm.decision_function(X_test[:10]))

# Probability
print("\nPrediction Probabilities")
print(svm.predict_proba(X_test[:5]))

# Single Prediction
sample = X_test[0].reshape(1, -1)

print("\nActual :", y_test[0])
print("Predicted :", svm.predict(sample)[0])

# Misclassified Samples
mis = np.where(y_test != y_pred)[0]

print("\nMisclassified Indices :", mis)
print("Total Misclassified :", len(mis))

# Decision Boundary
plt.figure(figsize=(10, 7))

DecisionBoundaryDisplay.from_estimator(
    svm,
    X_train,
    response_method="predict",
    cmap="Pastel1",
    alpha=0.5,
    xlabel=cancer.feature_names[0],
    ylabel=cancer.feature_names[1],
)

plt.scatter(
    X_train[:, 0],
    X_train[:, 1],
    c=y_train,
    cmap="coolwarm",
    edgecolors="black",
    s=40,
)

plt.scatter(
    svm.support_vectors_[:, 0],
    svm.support_vectors_[:, 1],
    s=170,
    facecolors="none",
    edgecolors="black",
    linewidth=2,
    label="Support Vectors",
)

ax = plt.gca()

xlim = ax.get_xlim()
ylim = ax.get_ylim()

xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)

YY, XX = np.meshgrid(yy, xx)

xy = np.vstack([XX.ravel(), YY.ravel()]).T

Z = svm.decision_function(xy).reshape(XX.shape)

ax.contour(
    XX,
    YY,
    Z,
    levels=[-1, 0, 1],
    colors="black",
    linestyles=["--", "-", "--"],
)

plt.title("Linear SVM Decision Boundary")
plt.legend()
plt.show()

# Support Vector Plot
plt.figure(figsize=(7, 6))

plt.scatter(
    svm.support_vectors_[:, 0],
    svm.support_vectors_[:, 1],
    c="yellow",
    edgecolors="black",
    s=150,
)

plt.title("Support Vectors")
plt.xlabel(cancer.feature_names[0])
plt.ylabel(cancer.feature_names[1])
plt.grid(True)
plt.show()

# Effect of C
print("\nEffect of C Parameter")

for c in [0.01, 0.1, 1, 10, 100]:

    model = SVC(kernel="linear", C=c)
    model.fit(X_train, y_train)

    print(
        f"C={c:<5}  Accuracy={model.score(X_test, y_test):.4f}  Support Vectors={len(model.support_vectors_)}"
    )

# Kernel Comparison
print("\nKernel Comparison")

for kernel in ["linear", "poly", "rbf", "sigmoid"]:

    model = SVC(kernel=kernel)
    model.fit(X_train, y_train)

    print(
        f"{kernel:<10} Accuracy = {model.score(X_test, y_test):.4f}"
    )
    