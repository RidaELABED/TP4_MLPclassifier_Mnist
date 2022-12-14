# -*- coding: utf-8 -*-
"""mlp_rida_maxime_part2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zpJUH23GZVlk_6LiproeieUZ2W3KgylJ
"""

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from keras.datasets import mnist
from sklearn.linear_model import Perceptron

from sklearn.metrics import classification_report, accuracy_score, log_loss

from sklearn.decomposition import PCA

import numpy as np
import time

(xtrain,ytrain),(xtest,ytest) = mnist.load_data()
xtrain = xtrain.reshape(60000, 28*28).astype('float32')
xtest = xtest.reshape(10000, 28*28).astype('float32')

xtrain /= 255
xtest /= 255

xtrain2 = xtrain[:10000,:]
ytrain2 = ytrain[:10000]

pca = PCA(n_components=100)
pca.fit(xtrain)
pca_xtrain = pca.transform(xtrain)
pca_xtest = pca.transform(xtest)

#Perceptron sans preprocessing
start_time = time.time()
pctr = Perceptron(tol=1e-3, random_state=0)
pctr.fit(xtrain, ytrain)
end_time = time.time()
print(f"Temps entraînement = {end_time - start_time}s")
y_pred = pctr.predict(xtest)

accuracy_score(ytest, y_pred)

#Perceptron avec preprocessing
start_time = time.time()
pipe_pctr = Pipeline([('minmax', MinMaxScaler()), ('pctr', Perceptron(tol=1e-3, alpha=0.001, validation_fraction=0.05, random_state=0))])
pipe_pctr.fit(xtrain, ytrain)
end_time = time.time()
print(f"Temps entraînement = {end_time - start_time}s")
y_pred = pipe_pctr.predict(xtest)

accuracy_score(ytest, y_pred)

#MLP 1 HL 300 sans preprocessing
start_time = time.time()
MLP1HL300 = MLPClassifier(hidden_layer_sizes=(300), random_state=0).fit(xtrain, ytrain)
end_time = time.time()
print(f"Temps entraînement = {end_time - start_time}s")
y_pred = MLP1HL300.predict(xtest)

print(classification_report(ytest, y_pred))

accuracy_score(ytest, y_pred)

#MLP 1 HL 300 avec preprocessing

start_time = time.time()
std_MLP1HL300 = Pipeline([('minmax', MinMaxScaler()), ('mlp', MLPClassifier(hidden_layer_sizes=(300), random_state=0))]).fit(xtrain, ytrain)
end_time = time.time()
print(f"Temps entraînement = {end_time - start_time}s")
y_pred = std_MLP1HL300.predict(xtest)

accuracy_score(ytest, y_pred)

start_time = time.time()
std_MLP2HL500300 = MLPClassifier(solver='adam', hidden_layer_sizes=(500, 300), tol=1e-3,batch_size=250, max_iter=100, alpha=0.1, random_state=0)
#std_MLP1HL300.out_activation_='softmax'
std_MLP2HL500300.fit(xtrain2, ytrain2)
end_time = time.time()
print(f"Temps entraînement = {end_time - start_time}s")
y_pred = std_MLP2HL500300.predict(xtest)

accuracy_score(ytest, y_pred)

std_MLP2HL500300.n_iter_

std_MLP2HL500300.out_activation_

start_time = time.time()
std_MLP2HL500300 = MLPClassifier(solver='adam', hidden_layer_sizes=(500, 300),
                                 tol=1e-4, batch_size=256, max_iter=50,
                                 alpha=0.01, random_state=0)
#std_MLP1HL300.out_activation_='softmax'
std_MLP2HL500300.fit(xtrain, ytrain)
end_time = time.time()
print(f"Temps entraînement = {end_time - start_time}s")
y_pred = std_MLP2HL500300.predict(xtest)

accuracy_score(ytest, y_pred)

std_MLP2HL500300.n_iter_

start_time = time.time()
std_MLP2HL500300 = MLPClassifier(solver='adam', hidden_layer_sizes=(500, 300),
                                 tol=1e-4, batch_size=300, max_iter=150,
                                 alpha=0.01, random_state=0)
#std_MLP1HL300.out_activation_='softmax'
std_MLP1HL300.fit(pca_xtrain, ytrain)
end_time = time.time()
print(f"Temps entraînement = {end_time - start_time}s")
y_pred = std_MLP1HL300.predict(pca_xtest)

accuracy_score(ytest, y_pred)

"""
param_grid = {
    'max_iter': [50, 100, 150],
    'solver': ['sgd', 'adam', 'lbfgs'],
    'alpha': [0.005, 0.05, 0.5, 1],
    'learning_rate': ['constant','adaptive'],
    'batch_size': [100, 200, 300]
}
"""


param_grid = {
    'max_iter': [50, 100, 150],
    'solver': ['sgd', 'adam', 'lbfgs'],
    'alpha': [0.005, 0.05, 0.5, 1],
}

grid = GridSearchCV(MLPClassifier(random_state=0), param_grid, cv=5)
grid.fit(xtrain2, ytrain2)

print(grid.best_params_)

grid.best_params_

