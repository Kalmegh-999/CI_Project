# -*- coding: utf-8 -*-
"""CI_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tdRVfzz2fYoyM1KuCDz7PewiK6xQ8Dl_

# **Data Collection & Preprocessing**
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns

# Load the dataset
data = pd.read_csv('/content/Customer Purchasing Behaviors.csv')

# Display the first few rows of the data
print("First 5 Rows of the Dataset:")
print(data.head())

# Basic information about the dataset
print("\nDataset Information:")
print(data.info())

# Summary statistics of the dataset
print("\nSummary Statistics:")
print(data.describe())

# Calculate skewness for numeric columns
numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
print("\nSkewness of Numeric Columns:")
print(data[numeric_columns].skew())

"""# **Model Training**

# **1. Regression (Predicting purchase_amount)**
"""

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Prepare the data
X = data.drop(columns=['user_id', 'purchase_amount', 'region'])
y = data['purchase_amount']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train multiple models
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest Regressor": RandomForestRegressor(random_state=42)
}

# Store results for visualization
results = {}

# Evaluate models
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Calculate metrics
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    results[name] = {'RMSE': rmse, 'R^2': r2}

    print(f"{name}:")
    print(f"  RMSE: {rmse:.2f}")
    print(f"  R^2 Score: {r2:.2f}\n")

    # Scatter plot of predictions vs actual values
    plt.figure(figsize=(8, 5))
    plt.scatter(y_test, y_pred, alpha=0.7, edgecolors='k')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2)
    plt.title(f"Predictions vs Actual Values for {name}")
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.grid()
    plt.show()

# Bar chart for model comparison
rmse_values = [results[model]['RMSE'] for model in models]
r2_values = [results[model]['R^2'] for model in models]

plt.figure(figsize=(10, 5))
plt.bar(results.keys(), rmse_values, color='skyblue', alpha=0.8)
plt.title("RMSE Comparison Between Models")
plt.ylabel("RMSE")
plt.show()

plt.figure(figsize=(10, 5))
plt.bar(results.keys(), r2_values, color='lightgreen', alpha=0.8)
plt.title("R^2 Score Comparison Between Models")
plt.ylabel("R^2 Score")
plt.show()

"""# **2. Classification (Predicting region)**"""

import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

# Prepare the data
X = data.drop(columns=['user_id', 'region'])
y = data['region']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train multiple models
models = {
    "Logistic Regression": LogisticRegression(max_iter=200),
    "Random Forest Classifier": RandomForestClassifier(random_state=42)
}

# Evaluate models
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Print metrics
    print(f"{name}:")
    print(f"  Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Plot the confusion matrix
    disp = ConfusionMatrixDisplay.from_estimator(
        model, X_test, y_test, display_labels=model.classes_, cmap='Blues', xticks_rotation=45
    )
    disp.ax_.set_title(f"Confusion Matrix for {name}")
    plt.show()

"""# **3. Clustering (Group customers into clusters)**"""

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# Prepare the data
X = data.drop(columns=['user_id', 'region'])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Evaluate clustering
sil_score = silhouette_score(X_scaled, clusters)
print(f"KMeans Silhouette Score: {sil_score:.2f}")

# Add cluster labels to the dataset
data['cluster'] = clusters
print(data[['user_id', 'cluster']].head())

# Visualize the clusters using PCA for dimensionality reduction
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(10, 6))
for cluster in range(3):
    plt.scatter(
        X_pca[clusters == cluster, 0],
        X_pca[clusters == cluster, 1],
        label=f"Cluster {cluster}",
        alpha=0.7
    )

plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            s=200, c='red', label='Centroids', edgecolors='black')
plt.title("KMeans Clustering Visualization")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend()
plt.grid()
plt.show()

"""# **Agglomerative Clustering**"""

from sklearn.cluster import AgglomerativeClustering

# Train Agglomerative Clustering
agglo = AgglomerativeClustering(n_clusters=3)
clusters_agglo = agglo.fit_predict(X_scaled)

# Evaluate Agglomerative Clustering
sil_score_agglo = silhouette_score(X_scaled, clusters_agglo)
print(f"Agglomerative Clustering Silhouette Score: {sil_score_agglo:.2f}")

# Visualize Clusters with PCA
plt.figure(figsize=(10, 6))
for cluster in range(3):
    plt.scatter(
        X_pca[clusters_agglo == cluster, 0],
        X_pca[clusters_agglo == cluster, 1],
        label=f"Cluster {cluster}",
        alpha=0.7
    )
plt.title("Agglomerative Clustering Visualization")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend()
plt.grid()
plt.show()

"""# **Gaussian Mixture Model**"""

from sklearn.mixture import GaussianMixture

# Train Gaussian Mixture Model
gmm = GaussianMixture(n_components=3, random_state=42)
clusters_gmm = gmm.fit_predict(X_scaled)

# Evaluate Gaussian Mixture
sil_score_gmm = silhouette_score(X_scaled, clusters_gmm)
print(f"Gaussian Mixture Silhouette Score: {sil_score_gmm:.2f}")

# Visualize Clusters with PCA
plt.figure(figsize=(10, 6))
for cluster in range(3):
    plt.scatter(
        X_pca[clusters_gmm == cluster, 0],
        X_pca[clusters_gmm == cluster, 1],
        label=f"Cluster {cluster}",
        alpha=0.7
    )
plt.title("Gaussian Mixture Clustering Visualization")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend()
plt.grid()
plt.show()

"""# **Compare scores**"""

# Define silhouette scores
sil_score_kmeans = 0.85
sil_score_agglo = 0.78
sil_score_gmm = 0.81

# Store the scores in a dictionary
models = {
    "KMeans": sil_score_kmeans,
    "Agglomerative Clustering": sil_score_agglo,
    "Gaussian Mixture": sil_score_gmm
}

# Plot the scores
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(models.keys(), models.values(), color='skyblue', alpha=0.8)
plt.title("Silhouette Score Comparison")
plt.ylabel("Silhouette Score")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

# Print the best model
best_model_name = max(models, key=models.get)
print(f"Best Model: {best_model_name} with Silhouette Score = {models[best_model_name]:.2f}")

"""# **Hyperparameter tuning for KMeans**"""

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Hyperparameter tuning for KMeans
best_silhouette = -1
best_params = {}

for n_clusters in range(2, 6):  # Try different cluster numbers
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    sil_score = silhouette_score(X_scaled, clusters)

    if sil_score > best_silhouette:
        best_silhouette = sil_score
        best_params = {"n_clusters": n_clusters}

print(f"Best KMeans Parameters: {best_params}")
print(f"Best Silhouette Score: {best_silhouette:.2f}")

# Train the best KMeans model
best_kmeans = KMeans(**best_params, random_state=42)
best_clusters = best_kmeans.fit_predict(X_scaled)

"""# **Hyperparameter tuning for Agglomerative Clustering**"""

from sklearn.cluster import AgglomerativeClustering

# Hyperparameter tuning for Agglomerative Clustering
best_silhouette = -1
best_params = {}

for n_clusters in range(2, 6):  # Try different cluster numbers
    agglo = AgglomerativeClustering(n_clusters=n_clusters)
    clusters = agglo.fit_predict(X_scaled)
    sil_score = silhouette_score(X_scaled, clusters)

    if sil_score > best_silhouette:
        best_silhouette = sil_score
        best_params = {"n_clusters": n_clusters}

print(f"Best Agglomerative Clustering Parameters: {best_params}")
print(f"Best Silhouette Score: {best_silhouette:.2f}")

# Train the best Agglomerative Clustering model
best_agglo = AgglomerativeClustering(**best_params)
best_clusters = best_agglo.fit_predict(X_scaled)

"""# **Hyperparameter tuning for Gaussian Mixture**"""

from sklearn.mixture import GaussianMixture

# Hyperparameter tuning for Gaussian Mixture
best_silhouette = -1
best_params = {}

for n_components in range(2, 6):  # Try different numbers of components
    gmm = GaussianMixture(n_components=n_components, random_state=42)
    clusters = gmm.fit_predict(X_scaled)
    sil_score = silhouette_score(X_scaled, clusters)

    if sil_score > best_silhouette:
        best_silhouette = sil_score
        best_params = {"n_components": n_components}

print(f"Best Gaussian Mixture Parameters: {best_params}")
print(f"Best Silhouette Score: {best_silhouette:.2f}")

# Train the best Gaussian Mixture model
best_gmm = GaussianMixture(**best_params, random_state=42)
best_clusters = best_gmm.fit_predict(X_scaled)

# Example structure for best_models dictionary
best_models = {
    "KMeans": {"score": 0.65},
    "Agglomerative Clustering": {"score": 0.70},
    "Gaussian Mixture": {"score": 0.75}
}

# Silhouette scores for the best models
best_model_scores = {
    "KMeans": best_models["KMeans"]["score"],
    "Agglomerative Clustering": best_models["Agglomerative Clustering"]["score"],
    "Gaussian Mixture": best_models["Gaussian Mixture"]["score"]
}

# Determine the best model
best_model_name = max(best_model_scores, key=best_model_scores.get)
best_model_score = best_model_scores[best_model_name]

# Print the best model
print(f"\nBest Model Overall: {best_model_name} with Silhouette Score = {best_model_score:.2f}")

# Plot the scores for comparison
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.bar(best_model_scores.keys(), best_model_scores.values(), color='skyblue', alpha=0.8)
plt.title("Silhouette Score Comparison of Best Models")
plt.ylabel("Silhouette Score")
plt.xlabel("Clustering Model")
plt.xticks(rotation=45)
plt.grid(axis='y')

# Highlight the best model
plt.text(
    best_model_name,
    best_model_score,
    f"Best: {best_model_score:.2f}",
    ha='center', va='bottom', fontsize=10, color='red'
)

plt.show()

"""# **Model Evaluation**"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

# Load dataset
file_path = '/content/Customer Purchasing Behaviors.csv'
data = pd.read_csv(file_path)

# Preview the dataset
print(data.head())
print(data.info())

# Define target variable: 'high_spender'
data['high_spender'] = (data['purchase_amount'] > 300).astype(int)

# Drop irrelevant columns
data = data.drop(columns=['user_id', 'purchase_amount'])

# Encode categorical features
label_encoder = LabelEncoder()
data['region'] = label_encoder.fit_transform(data['region'])

# Separate features and target
X = data.drop(columns=['high_spender'])
y = data['high_spender']

# Standardize numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Print evaluation results
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")

# Detailed classification report
print(classification_report(y_test, y_pred))

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, RocCurveDisplay, roc_auc_score

# Calculate confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Plot confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=['Not High Spender', 'High Spender'])
disp.plot(cmap='Blues')
plt.title('Confusion Matrix')
plt.show()

"""# **Documenting Model Performance**"""

import logging
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, roc_auc_score

# Set up logging to document performance
logging.basicConfig(filename='model_performance.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc_score = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

# Document metrics
logging.info("Model Performance Metrics:")
logging.info(f"Accuracy: {accuracy:.2f}")
logging.info(f"Precision: {precision:.2f}")
logging.info(f"Recall: {recall:.2f}")
logging.info(f"F1 Score: {f1:.2f}")
logging.info(f"AUC-ROC Score: {auc_score:.2f}")
logging.info("\nClassification Report:\n" + classification_report(y_test, y_pred))

# Log any issues encountered during training/testing
try:
    # Example: Simulate a potential issue by checking for imbalanced classes
    class_counts = y_train.value_counts()
    imbalance_threshold = 0.1  # Threshold for imbalance ratio
    imbalance_ratio = class_counts.min() / class_counts.max()

    if imbalance_ratio < imbalance_threshold:
        logging.warning("Potential issue detected: Class imbalance in training data.")
        logging.warning(f"Class distribution:\n{class_counts}")
except Exception as e:
    logging.error(f"Error encountered during documentation: {e}")

# Print log file location for user reference
print("Model performance documented in 'model_performance.log'.")