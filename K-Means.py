import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load dataset
X, y = make_blobs(
    n_samples=300,
    centers=3,
    cluster_std=0.60,
    random_state=42
)

# Explore dataset
print("Shape of Features :", X.shape)
print("Shape of Target   :", y.shape)

# Visualize dataset
plt.figure(figsize=(6,6))
plt.scatter(X[:,0], X[:,1], s=40)
plt.title("Original Dataset")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()

# Create model
model = KMeans(
    n_clusters=3,
    random_state=42
)

# Train model
model.fit(X)

# Predictions
labels = model.labels_
centroids = model.cluster_centers_

# Evaluation
inertia = model.inertia_
silhouette = silhouette_score(X, labels)

print("\nCluster Labels:")
print(labels)

print("\nCluster Centers:")
print(centroids)

print("\nNumber of Clusters :", model.n_clusters)
print("Iterations :", model.n_iter_)
print("Inertia :", inertia)
print("Silhouette Score :", silhouette)

# Visualize clusters
plt.figure(figsize=(6,6))

plt.scatter(
    X[:,0],
    X[:,1],
    c=labels,
    cmap="viridis",
    s=40
)

plt.scatter(
    centroids[:,0],
    centroids[:,1],
    c="red",
    marker="X",
    s=250,
    label="Centroids"
)

plt.title("K-Means Clustering")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend()
plt.show()

# Elbow Method
inertia_values = []

for k in range(1,11):
    km = KMeans(
        n_clusters=k,
        random_state=42
    )
    km.fit(X)
    inertia_values.append(km.inertia_)

plt.figure(figsize=(6,6))
plt.plot(range(1,11), inertia_values, marker="o")
plt.title("Elbow Method")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.grid(True)
plt.show()

# Predict new sample
new_point = np.array([[5,2]])

predicted_cluster = model.predict(new_point)

print("\nNew Data Point :", new_point)
print("Predicted Cluster :", predicted_cluster)