import numpy as np
import pandas as pd

import pylab as pl

from sklearn import decomposition

#>>> X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
#>>> pca = PCA(n_components=2)
#>>> pca.fit(X)


from pandas.tools.plotting import parallel_coordinates


class PCA:
	def __init__(self, dataset):
		"""Performs the principal component analysis"""
		# First, nominals and rows with missing values must be dropped
		dataset = dataset.drop_nominals().fix_missing(drop_objects=True)

		# Center to zero mean
		Y = dataset.center().X

		U,S,V = np.linalg.svd(Y, full_matrices=False)
		print(S)
		# computes variance explained by principal components
		self.rho = pd.Series((S*S) / (S*S).sum())
		# projects the centered data onto principal component space, Z
		V = V.T
		self.Z = Y.dot(V)

	def plot(self):
		pl.subplot(2, 2, 1)
		pl.scatter(self.Z[:, 0], self.Z[:, 1])
		pl.title('Transformed data')
		pl.xlabel('PCA #1')
		pl.ylabel('PCA #2')

		pl.subplot(2, 2, 2)
#		parallel_coordinates(self.dataset.df, 'communityCode')

		pl.subplot(2, 2, 3)
		cumsum = self.rho.cumsum()
		cumsum.plot()
		pl.title('Varaince')
		pl.xlabel('Number of principal components')
		pl.ylabel('Explained Varaince')

		pl.show()

	def auto(self):
		pca = decomposition.PCA(n_components=2)
		pca.fit(dataset.X)
		X = pca.fit_transform(dataset.X)
		print(X)
		pl.scatter(X[:, 0], X[:, 1])
		pl.show()

	def wat(self):
		X     = dataset.X
		Y     = X - X.mean(0)
		U,S,V = np.linalg.svd(Y, full_matrices=False)
		print(S)
		# computes variance explained by principal components
		self.rho = pd.Series((S*S) / (S*S).sum())
		# projects the centered data onto principal component space, Z
		V = V.T
		self.Z = Y.dot(V)

	def __repr__(self):
		return "hi"