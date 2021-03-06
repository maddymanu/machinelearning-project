import pylab as pl


from Framework.DataSet import *

crime = DataSet(datafile='../data/raw.csv', nominals=['state','communityname','countyCode','communityCode'])

#crime = crime.drop(['state', 'communityname']) 	  # Drop strings
#crime = crime.drop(['countyCode','communityCode']) # Drop nominals
crime = crime.drop_columns([
	'fold',
	'murders', 'murdPerPop',
	'rapes', 'rapesPerPop',
	'robberies', 'robbbPerPop',
#	'assaults', 'assaultPerPop',
	'burglaries', 'burglPerPop',
	'larcenies', 'larcPerPop',
	'autoTheft', 'autoTheftPerPop',
	#'arsons', 'arsonsPerPop',
	'ViolentCrimesPerPop',
	#'nonViolPerPop',
])
print(type(crime.X))

crime = crime.normalize()


crime = crime.take_columns(['nonViolPerPop', 'arsons'])
#print(crime)