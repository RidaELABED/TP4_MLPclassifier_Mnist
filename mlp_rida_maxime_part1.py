# -*- coding: utf-8 -*-
"""MLP_Rida_Maxime_Partie1234.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19SQmL6NKCJALOfB7PNBSwi_uWFtUF6ir
"""

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np 
from sklearn.datasets import fetch_openml
import time
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Perceptron
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


mnist = fetch_openml('mnist_784')
x = mnist.data
y = mnist.target

Xtrain,Xtest,ytrain,ytest =x[:60000],x[60000:],y[:60000],y[60000:]

XtrainPca = np.reshape(Xtrain, (-1, 784))
XtestPca = np.reshape(Xtest, (-1, 784))
XtrainPca = XtrainPca.astype('float32') / 255
XtestPca = XtestPca.astype('float32') / 255

pca_784 = PCA(n_components=784)
pca_784.fit(XtrainPca)

plt.grid()
plt.plot(np.cumsum(pca_784.explained_variance_ratio_ * 100))
plt.xlabel('Nombre de composantes')
plt.ylabel('Variance')

pca_100 = PCA(n_components=100)
pca_100.fit(XtrainPca)
XtrainPca = pca_100.transform(XtrainPca)
XtestPca = pca_100.transform(XtestPca)

#1.Perceptron sans preprocessing

tuned_parameters ={'alpha':[0.0001,0.001,0.01,0.1,1],'penalty':['l1','elasticnet','l2']}
grid = GridSearchCV(Perceptron(),tuned_parameters, cv=5)
grid.fit(Xtrain,ytrain)

print(grid.best_params_)

clf = Perceptron(alpha = 0.001, random_state=0,penalty="l1").fit(Xtrain,ytrain)
print(clf.score(Xtest,ytest))

#2.Perceptron avec preprocessing

tuned_parameters ={'alpha':[0.0001,0.001,0.01,0.1,1],'penalty':['l1','l2']}
grid = GridSearchCV(Perceptron(),tuned_parameters, cv=5)
grid.fit(XtrainPca,ytrain)

print(grid.best_params_)

clf = Perceptron(alpha = 0.01, random_state=0,penalty="none").fit(XtrainPca,ytrain)
print(clf.score(XtestPca,ytest))

#3. HL 300 sans preprocessing

start_time = time.time()

clf = MLPClassifier(hidden_layer_sizes=(300),solver='sgd',batch_size = 300,random_state=0).fit(Xtrain,ytrain)

end_time = time.time()
print("temps ecoule = "+str(end_time - start_time))
print("le score de classification est", clf.score(Xtest,ytest))


start_time = time.time()

clf = MLPClassifier(hidden_layer_sizes=(300),solver='lbfgs',batch_size = 300,random_state=0).fit(Xtrain,ytrain)

end_time = time.time()
print("temps ecoule = "+str(end_time - start_time))
print("le score de classification est", clf.score(Xtest,ytest))


start_time = time.time()

clf = MLPClassifier(hidden_layer_sizes=(300),solver='adam',batch_size = 300,random_state=0).fit(Xtrain,ytrain)

end_time = time.time()
print("temps ecoule = "+str(end_time - start_time))
print("le score de classification est", clf.score(Xtest,ytest))

#4. HL 300 avec preprocessing

start_time = time.time()

clf = MLPClassifier(hidden_layer_sizes=(300),solver='adam',random_state=0).fit(XtrainPca,ytrain)

end_time = time.time()
print("temps ecoule = "+str(end_time - start_time))
print("le score de classification est", clf.score(XtestPca,ytest))



start_time = time.time()

clf = MLPClassifier(hidden_layer_sizes=(300),solver='adam',batch_size = 300, alpha = 0.01,random_state=0).fit(XtrainPca,ytrain)

end_time = time.time()
print("temps ecoule = "+str(end_time - start_time))
print("le score de classification est", clf.score(XtestPca,ytest))