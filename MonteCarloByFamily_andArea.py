import random
import csv
from scipy.stats import pearsonr
#from numpy import percentile
#import numpy as np

random.seed(777)

number_of_perms = 5000

family_field_name = "gFam"


def quantile(xs, q = 0.15):
	return list(sorted(xs))[int(q*len(xs))]

#def quantile(xs, q = 0.15):
#	return percentile(xs,q*100, interpolation = 'lower')

  
def pickOneFromEachFamily(d, families,areas):
	# Brute-force find a set of d that are independent in terms of family AND area
	# Assumes there are fewer unique areas than families
	# make a dictionary of indices of d that belong to each family
# 	fdict = {}
# 	for i in range(len(families)):
# 		try:
# 			fdict[families[i]].append(i)
# 		except:
# 			fdict[families[i]] = [i]
	adict = {}
	for i in range(len(areas)):
		try:
			adict[areas[i]].append(i)
		except:
			adict[areas[i]] = [i]
	
	sel = []
	sel_fam = [0,0]
	# while there are duplicates in sel_fam
	while len(sel_fam) > len(set(sel_fam)):
		# select some languages that are independent by area
		rchoice = [random.choice(inds) for inds in adict.values()]
		# get the humidity
		sel = [d[x] for x in rchoice]
		# get the families they belong to
		# (if they are duplicates, then
		sel_fam = [families[x] for x in rchoice]
	return sel


def differenceBetweenTwoGroups(d, inGroup1, families, areas, q = 0.15, returnMeasure="Q"):

	# select values of d that belong to group 1
	group1 = [x for (i,x) in enumerate(d) if inGroup1[i]]
	# identify corresponding families for each value of d that belong to group 1
	families1  = [x for (i,x) in enumerate(families) if inGroup1[i]]
	areas1 = [x for (i,x) in enumerate(areas) if inGroup1[i]]
	# pick independent samples for group 1
	independentSamples1 = pickOneFromEachFamily(group1, families1,areas1)
	
	# the randomised version of group 1 can be drawn from any family
	group1R = d
	families1R  = families
	areas1R = areas
	randomisedSamples = pickOneFromEachFamily(group1R,families1R, areas1R)
	
	# Second group is simple
	group2 = [x for (i,x) in enumerate(d) if not inGroup1[i]]
	families2  = [x for (i,x) in enumerate(families) if not inGroup1[i]]
	areas2  = [x for (i,x) in enumerate(areas) if not inGroup1[i]]
	# pick independent samples for group 2
	independentSamples2 = pickOneFromEachFamily(group2, families2,areas2)
	
	# make sure the sample sizes are the same
	minSize = min([len(independentSamples1),len(independentSamples2)])
	independentSamples1 = random.sample(independentSamples1, minSize)
	independentSamples2 = random.sample(independentSamples2, minSize)
	randomisedSamples  = random.sample(randomisedSamples ,minSize)
	
	# optionally return difference in means
	if returnMeasure =="Mean":
		q1 = sum(independentSamples1)/float(len(independentSamples1))
		q2 = sum(independentSamples2)/float(len(independentSamples2))
		q1R = sum(randomisedSamples)/float(len(randomisedSamples))
	# by default, measure quantiles
	if returnMeasure == "Q":
		# get quantile measures
		q1 = quantile(independentSamples1, q)
		q2 = quantile(independentSamples2, q)
		q1R = quantile(randomisedSamples, q)
	
	# return difference between q1 and q2, and difference between q1R and q2
	return q1 - q2, q1R - q2

def independentCorrelation(humidity, ntones,families,areas):
	chosenIndices = pickOneFromEachFamily(range(len(humidity)), families,areas)
	
	hx = [humidity[i] for i in chosenIndices]
	tx = [ntones[i] for i in chosenIndices]
	
	return pearsonr(hx,tx)
			


#############
# Load data #
#############
dataX = []
with open('ANU_numTones_SpecificHumidity_GlottoFams.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in spamreader:
		dataX.append(row)
		
header = dataX[0]

#############
# Run Tests #
#############

# Run tests on glottolog (gFam) and ANU (Family) families
# for family_field_name in ["Family","gFam"]:
# 	print "RUNNING TESTS ON",family_field_name,"\n"
# 	data = dataX[:]# copy list
# 	remove languages without family data
# 	data = [x for x in data if x[header.index(family_field_name)]!="NA"]
# 
# 
# 	humidity = [float(x[header.index("specH.mean")]) for x in data[1:-1]]
# 	family = [x[header.index(family_field_name)] for x in data[1:-1]]
# 	area = [x[header.index("Autotyp.area")] for x in data[1:-1]]
# 	number_of_tones = [int(x[header.index("Number.of.tones")]) for x in data[1:-1]]
# 	
# 	
# 	
# 	complex = [x >=3 for x in number_of_tones]
# 
# 	print "Difference between complex and non-complex humidity"
# 	trueDiffs = {}
# 	for qx in [0.15,0.25,0.5, 0.75]:
# 		trueDiff = [differenceBetweenTwoGroups(humidity, complex, family, area, q = qx) for x in range(number_of_perms)]
# 		print qx,"th Test 2:", sum([x[0] > 0 for x in trueDiff]) / float(len(trueDiff))
# 		print qx,"th Test 3:", sum([x[0] > x[1] for x in trueDiff]) / float(len(trueDiff))		
# 		trueDiffs[qx] = trueDiff
# 
# 
# 	print "Difference in means"
# 
# 	trueDiff = [differenceBetweenTwoGroups(humidity, complex, family, area, returnMeasure="Mean") for x in range(number_of_perms)]
# 	
# 	print sum([x[0] > 0 for x in trueDiff]) / float(len(trueDiff))
# 	print sum([x[0] > x[1] for x in trueDiff]) / float(len(trueDiff))
# 	
# 	
# 	print "\n\n\n"
# print "Correlations"	
# for family_field_name in ["Family","gFam"]:
# 	print "RUNNING TESTS ON",family_field_name,"\n"
# 	data = dataX[:]# copy list
# 	# remove languages without family data
# 	data = [x for x in data if x[header.index(family_field_name)]!="NA"]
# 
# 
# 	humidity = [float(x[header.index("specH.mean")]) for x in data[1:-1]]
# 	family = [x[header.index(family_field_name)] for x in data[1:-1]]
# 	area = [x[header.index("Autotyp.area")] for x in data[1:-1]]
# 	number_of_tones = [int(x[header.index("Number.of.tones")]) for x in data[1:-1]]
# 	
# 	corRes = [independentCorrelation(humidity, number_of_tones,family,area) for x in range(number_of_perms)]
# 	print "r",sum([x[0] for x in corRes]) / float(len(corRes))
# 	print "p",sum([x[1] for x in corRes]) / float(len(corRes))
# 	print "\n\n\n"
# 	
lowHumidity = 0.01324937	
print "Low humidity correlations"	
for family_field_name in ["Family","gFam"]:
	print "RUNNING TESTS ON",family_field_name,"\n"
	data = dataX[:]# copy list
	# remove languages without family data
	data = [x for x in data if x[header.index(family_field_name)]!="NA"]
	
	
	
	humidity = [float(x[header.index("specH.mean")]) for x in data[1:-1]]

	data = [x for i,x in enumerate(data[1:-1]) if humidity[i] < lowHumidity]
	
	humidity = [float(x[header.index("specH.mean")]) for x in data[1:-1]]
	family = [x[header.index(family_field_name)] for x in data[1:-1]]
	area = [x[header.index("Autotyp.area")] for x in data[1:-1]]
	number_of_tones = [int(x[header.index("Number.of.tones")]) for x in data[1:-1]]
	
	corRes = [independentCorrelation(humidity, number_of_tones,family,area) for x in range(number_of_perms)]
	print "Low H r",sum([x[0] for x in corRes]) / float(len(corRes))
	print "Low H p",sum([x[1] for x in corRes]) / float(len(corRes))
	print "\n\n\n"