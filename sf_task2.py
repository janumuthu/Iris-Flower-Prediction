# -*- coding: utf-8 -*-
"""SF-Task2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KqOvC2rH-o5vULwvI-ueC7IAYfmGfVOx

# Graduate Rotational Internship Program @ The Sparks Foundation
# Data Science and Business Analytics Intern

# Prediction using UnSupervised ML

## (Level - Beginner)

# From the given ‘Iris’ dataset, predict the optimum number of clusters and represent it visually. 
# ● Use R or Python or perform this task
# ● Dataset : https://bit.ly/3kXTdox

# Author - **Divya Janani.S**

# Unsupervised learning, also known as unsupervised machine learning, uses machine learning algorithms to analyze and cluster unlabeled datasets. These algorithms discover hidden patterns or data groupings without the need for human intervention.

# **K-Means Clustering is an Unsupervised Learning algorithm, which groups the unlabeled dataset into different clusters. Here K defines the number of pre-defined clusters that need to be created in the process, as if K=2, there will be two clusters, and for K=3, there will be three clusters, and so on**.

# **It is a centroid-based algorithm, where each cluster is associated with a centroid. The main aim of this algorithm is to minimize the sum of distances between the data point and their corresponding clusters.**

# IMPORTING NECESSARY PYTHON LIBRARIES
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn

"""# LOADING THE DATASET"""

iris=pd.read_csv("/content/Iris.csv")
iris.head()

"""# DATA PREPROCESSING"""

iris.shape   # checking the shape of the data set

iris.columns   # checking the col names

iris.isnull().sum()     # checking the null values

iris.duplicated().sum()      # checking the duplicate values

iris.describe().transpose()    # checking the count and mean of the col

iris=iris.drop('Id', axis='columns')  # dropping the irrelevant col

iris.dtypes # checking the datatypes

iris.corr()  # checking the relationship between the col

"""# HEATMAP FOR CORRELATION"""

sns.heatmap(iris.corr(),annot=True,cmap='YlGnBu')
plt.title("Correlation Heatmap")
plt.show()

"""# VISUALIZATION - CHECKING FOR OUTLIERS IN THE DATASET"""

sns.boxplot(x='SepalLengthCm', data=iris, color='orange')
plt.show()

sns.boxplot(x='SepalWidthCm', data=iris, color='green')
plt.show()

sns.boxplot(x='PetalLengthCm', data=iris, color='blue')
plt.show()

sns.boxplot(x='PetalWidthCm', data=iris, color='red')
plt.show()

"""# OUTLIERS ARE PRESENT IN SEPALWIDTH COL - DETECTING THE OUTLIERS AND TREATING IT"""

IQR = iris['SepalWidthCm'].quantile(0.75) - iris['SepalWidthCm'].quantile(0.25)
lower_limit = iris['SepalWidthCm'].quantile(0.25) - (IQR * 1.5)
upper_limit = iris['SepalWidthCm'].quantile(0.75) + (IQR * 1.5)
print(lower_limit)
print(upper_limit)

iris['iris_replaced'] = pd.DataFrame(np.where(iris['SepalWidthCm'] > upper_limit, upper_limit, np.where(iris['SepalWidthCm'] < lower_limit, lower_limit, iris['SepalWidthCm'])))

sns.boxplot(iris.iris_replaced);plt.title('Boxplot of SepalWidth');plt.show()

"""# VARIANT ANALYSIS"""

x=iris['SepalLengthCm']
y=iris['SepalWidthCm']
sns.scatterplot(x=x,y=y,hue='Species',data=iris)
plt.show()

sns.set_palette(sns.color_palette("icefire_r"))
sns.pairplot(data=iris,hue='Species')
plt.show()

x=iris.iloc[:,[0,1,2,3]].values

"""# FINDING THE OPTIMUM NO OF CLUSTERS USING ELBOW CURVE"""

from sklearn.cluster import KMeans

TWSS = []
k = list(range(2, 9))

for i in k:
    kmeans = KMeans(n_clusters = i)
    kmeans.fit(x)
    TWSS.append(kmeans.inertia_)
    
TWSS

"""# SCREE PLOT/ELBOW CURVE"""

plt.plot(k, TWSS, 'g:',marker='s', mfc='r',mec='k',ms=7)
plt.xlabel("No_of_Clusters")
plt.ylabel("total_within_SS")
plt.show()

"""# SELECTING NO OF CLUSTERS = 3

# FITTING THE MODEL - KMEANS
"""

model = KMeans(n_clusters = 3)
model.fit(x)

model.labels_                        # getting the labels of clusters assigned to each row 
iris_clust = pd.Series(model.labels_)        # converting numpy array into pandas series object  

iris_clust_new= iris_clust+1                           # changing the starting no of cluster with 1 instead of 0
iris['cluster'] = iris_clust_new                   # creating a  new column and assigning it to new column

y=model.fit_predict(x)

y

iris.head()

iris['cluster'].value_counts()

"""# VISUALIZATION OF CLUSTERS"""

plt.scatter(x[y == 0, 0], x[y == 0, 1], 
            s = 100, c = 'red', label = 'Iris-setosa')
plt.scatter(x[y == 1, 0], x[y == 1, 1], 
            s = 100, c = 'green', label = 'Iris-versicolour')
plt.scatter(x[y == 2, 0], x[y == 2, 1],
            s = 100, c = 'cyan', label = 'Iris-virginica')

# Plotting the centroids of the clusters
plt.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:,1], 
            s = 100, c = 'black', label = 'Centroids')

plt.legend()
plt.show()

"""# SAVING THE MODEL IN PICKLE"""

import pickle
pickle.dump(model,open("model.pkl","wb"))

"""# THANK YOU"""