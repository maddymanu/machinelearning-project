import pylab as pl


from Framework.DataSet import *

dataset = DataSet(
	datafile ='../data/raw.csv',
	na_values=['?'],
	string_columns=['state','communityname'],
	class_column='state',
)

dataset = dataset.fix_missing(drop_objects=True)
dataset = dataset.normalize()
dataset = dataset.discretize('arsons', 2);
dataset = dataset.set_class_column('arsons')

print ( dataset.classNames )


#dataset = dataset.normalize()
