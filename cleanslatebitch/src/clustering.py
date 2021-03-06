from Framework.DataSet import *

from pylab import *
from scipy.io import loadmat
from toolbox_02450 import clusterplot
from sklearn.mixture import GMM
from sklearn import cross_validation

crime = DataSet(datafile='../data/normalized.csv')

#crime = crime.drop(['state', 'communityname']) 	  # Drop strings
#crime = crime.drop(['countyCode','communityCode']) # Drop nominals
# crime = crime.drop_columns([
# 	'fold',
# 	'murders', 'murdPerPop',
# 	'rapes', 'rapesPerPop',
# 	'robberies', 'robbbPerPop',
# #	'assaults', 'assaultPerPop',
# 	'burglaries', 'burglPerPop',
# 	'larcenies', 'larcPerPop',
# 	'autoTheft', 'autoTheftPerPop',
# 	'arsons', 'arsonsPerPop',
# 	'ViolentCrimesPerPop',
# 	'nonViolPerPop',
# ])
crime = crime.take_columns([
	'racePctHisp', 
	'racePctWhite',
	#'racepctblack',
	#'racePctAsian',
	'medIncome', 'NumStreet', 'NumImmig',
	'PctEmploy', 'PctPopUnderPov', 'pctUrban'
	])
crime = crime.fix_missing(fill_mean=True)
crime = crime.standardize()
#crime = crime.normalize()
#crime = crime.drop_nominals()

crime = crime.take_first_n_rows(200)

crime = crime.discretize('racePctWhite', 2)
crime = crime.set_class_column('racePctWhite')
#crime = DataSet(dataframe=crime.df[:200])
#print(crime.df.assaults)
print(crime.y)
#col = crime.one_of_k('pctUrban', 2)
#print(col)
#dataset = crime.discretize('pctUrban', 2)
#dataset = crime.set_class_column('pctUrban')
#print(dataset.y)

# Variables of interest
N, M = crime.N, crime.M
#print(M)
#C = len(crime.classNames)
X = crime.X

# fig = plt.figure()
# ax = Axes3D(fig)
# ax.plot(X[0], X[1], X[2])

# plt.show()

# Range of K's to try
KRange = range(1,11)
T = len(KRange)

covar_type = 'full'     # you can try out 'diag' as well
reps = 15                # number of fits with different initalizations, best result will be kept

# Allocate variables
BIC = np.zeros((T,1))
AIC = np.zeros((T,1))
CVE = np.zeros((T,1))

# K-fold crossvalidation
CV = cross_validation.KFold(N,10,shuffle=True)

for t,K in enumerate(KRange):
	print('Fitting model for K={0}\n'.format(K))
	# Fit Gaussian mixture model
	gmm = GMM(n_components=K, covariance_type=covar_type, n_init=reps, params='wmc').fit(X)
	# Get BIC and AIC
	BIC[t,0] = gmm.bic(X)
	AIC[t,0] = gmm.aic(X)
	cds = gmm.means_       # extract cluster centroids (means of gaussians)
	print(cds)
	cls = gmm.predict(X)    # extract cluster labels
	print(cls)
	# For each crossvalidation fold
	for train_index, test_index in CV:
		# extract training and test set for current CV fold
		X_train = X[train_index]
		X_test = X[test_index]
		# Fit Gaussian mixture model to X_train
		gmm = GMM(n_components=K, covariance_type=covar_type, n_init=reps, params='wmc').fit(X_train)
		cds = gmm.means_       # extract cluster centroids (means of gaussians)
		#print(cds)
		covs = gmm.covars_      # extract cluster shapes (covariances of gaussians)
		# compute negative log likelihood of X_test
		#print(gmm.score(X_test))
		CVE[t] += - gmm.score(X_test).sum()
            

# Plot results

figure(1); hold(True)
plot(KRange, BIC)
plot(KRange, AIC)
plot(KRange, 2*CVE)
legend(['BIC', 'AIC', 'Crossvalidation'])
xlabel('K')
show()

