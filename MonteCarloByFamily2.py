import random
import csv


random.seed(777)

number_of_perms = 5000


def quantile(xs, q = 0.15):
	return list(sorted(xs))[int(q*len(xs))]

#def quantile(xs, q = 0.15):
#	return percentile(xs,q*100, interpolation = 'lower')
    
def pickOneFromEachFamily(d, families):
	# make a dictionary of indices of d that belong to each family
	fdict = {}
	for i in range(len(families)):
		try:
			fdict[families[i]].append(i)
		except:
			fdict[families[i]] = [i]
	
	# for each family (key) choose one index
	# return the value of d that corresponds to that index
	return [d[random.choice(inds)] for inds in fdict.values()]
	
def pickTwoFromEachFamily(d,families,inGroup):
	fdict = {}
	for i in range(len(d)):
		t = inGroup[i]
		dx = d[i]
		fam = families[i]
		try:
			fdict[fam][t].append(i)
		except:
			if not fam in fdict.keys():
				fdict[fam] = {}
			fdict[fam][t] = [i]
	# return 4 values - a random choice for each family
	#   2 from outside the group
	#   1 Within the group
	#   1 From either within or outside the group
	return [(d[random.choice(inds[0])], d[random.choice(inds[0])], d[random.choice(inds[1])], d[random.choice(inds[0]+inds[1])]) for inds in fdict.values() if len(inds.keys())==2]


def differenceBetweenTwoGroups(d, inGroup1, families, q = 0.15, returnMeasure="Q"):
	# select values of d that belong to group 1
	group1 = [x for (i,x) in enumerate(d) if inGroup1[i]]
	# identify corresponding families for each value of d that belong to group 1
	families1  = [x for (i,x) in enumerate(families) if inGroup1[i]]
	
	# pick independent samples for group 1
	independentSamples1 = pickOneFromEachFamily(group1, families1)
	
	# the randomised version of group 1 can be drawn from any family
	group1R = d
	families1R  = families
	randomisedSamples = pickOneFromEachFamily(group1R,families1R)
	
	# Second group is simple
	group2 = [x for (i,x) in enumerate(d) if not inGroup1[i]]
	families2  = [x for (i,x) in enumerate(families) if not inGroup1[i]]
	
	# pick independent samples for group 2
	independentSamples2 = pickOneFromEachFamily(group2, families2)
	
	# pick another random sample of tone languages for group 2B
	independentSamples2B = pickOneFromEachFamily(group2, families2)
	
	# make sure the sample sizes are the same
	minSize = min([len(independentSamples1),len(independentSamples2)])
	independentSamples1 = random.sample(independentSamples1, minSize)
	independentSamples2 = random.sample(independentSamples2, minSize)
	independentSamples2B = random.sample(independentSamples2B, minSize)
	randomisedSamples = random.sample(randomisedSamples, minSize)
#	chooseSamp2 = random.sample(range(len(independentSamples2)),minSize)
#	independentSamples2 = [x for (i,x) in enumerate(independentSamples2) if i in chooseSamp2]
#	independentSamples2B = [x for (i,x) in enumerate(independentSamples2B) if i in chooseSamp2]
	
	# optionally return difference in means
	if returnMeasure =="Mean":
		q1 = sum(independentSamples1)/float(len(independentSamples1))
		q2 = sum(independentSamples2)/float(len(independentSamples2))
		q2B = sum(independentSamples2B)/float(len(independentSamples2B))
		q1R = sum(randomisedSamples)/float(len(randomisedSamples))
	# by default, measure quantiles
	if returnMeasure == "Q":
		# get quantile measures
		q1 = quantile(independentSamples1, q)
		q2 = quantile(independentSamples2, q)
		q2B = quantile(independentSamples2B, q)
		q1R = quantile(randomisedSamples, q)
	
	# return difference between q1 and q2, and difference between q1R and q2
	return q1 - q2, q1R - q2, q2B - q2

def differenceBetweenTwoGroups_sameFamilies(d, inGroup1, families, q = 0.15, returnMeasure="Q"):
	
	# pick independent samples for group 1
	independentSamples = pickTwoFromEachFamily(d, families, inGroup1)
	independentSamples1 = [x[2] for x in independentSamples]
	independentSamples2 = [x[0] for x in independentSamples]
	independentSamples2B = [x[1] for x in independentSamples]	
	randomisedSamples = [x[3] for x in independentSamples]
	
	# optionally return difference in means
	if returnMeasure =="Mean":
		q1 = sum(independentSamples1)/float(len(independentSamples1))
		q2 = sum(independentSamples2)/float(len(independentSamples2))
		q2B = sum(independentSamples2B)/float(len(independentSamples2B))
		q1R = sum(randomisedSamples)/float(len(randomisedSamples))
	# by default, measure quantiles
	if returnMeasure == "Q":
		# get quantile measures
		q1 = quantile(independentSamples1, q)
		q2 = quantile(independentSamples2, q)
		q2B = quantile(independentSamples2B, q)
		q1R = quantile(randomisedSamples, q)
	
	# return difference between q1 and q2, and difference between q1R and q2
	return q1 - q2, q1R - q2, q2B - q2
	
	
def compareAllPairs(l1,l2):
	out = []
	for i in range(len(l1)):
		for j in range(i): 
			out.append(l1[i] > l2[j])
	return sum([x > 0 for x in out]) / float(len(out))
			


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

testProcedure = differenceBetweenTwoGroups
# set this to the alternative test:
#testProcedure = differenceBetweenTwoGroups_sameFamilies

# Run tests on glottolog (gFam) and ANU (Family) families
for family_field_name in ["gFam","Family","Autotyp.area"]:
	print "RUNNING TESTS ON",family_field_name,"\n"
	data = dataX[:]# copy list
	# remove languages without family data
	data = [x for x in data if x[header.index(family_field_name)]!="NA"]


	humidity = [float(x[header.index("specH.mean")]) for x in data[1:-1]]
	family = [x[header.index(family_field_name)] for x in data[1:-1]]
	number_of_tones = [int(x[header.index("Number.of.tones")]) for x in data[1:-1]]
	
	
	
	complex = [x >=3 for x in number_of_tones]

	trueDiffs = {}
	for qx in [0.15,0.25,0.5, 0.75]:
		trueDiff = [testProcedure(humidity, complex, family, q = qx) for x in range(number_of_perms)]
		print qx,"th Test 2:", sum([x[0] > 0 for x in trueDiff]) / float(len(trueDiff))
		print qx,"th Test 3:", sum([x[0] > x[1] for x in trueDiff]) / float(len(trueDiff))
		print qx,"th Test 4:", sum([x[0] > x[2] for x in trueDiff]) / float(len(trueDiff))		
		trueDiffs[qx] = trueDiff


	print "Difference in means"

	trueDiff = [testProcedure(humidity, complex, family, returnMeasure="Mean") for x in range(number_of_perms)]
	
	print sum([x[0] > 0 for x in trueDiff]) / float(len(trueDiff))
	print sum([x[0] > x[1] for x in trueDiff]) / float(len(trueDiff))
	print sum([x[0] > x[2] for x in trueDiff]) / float(len(trueDiff))
	
	
	print "\n\n\n"