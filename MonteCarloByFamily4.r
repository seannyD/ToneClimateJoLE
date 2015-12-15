#setwd("~/Documents/MPI/ClimateAndLanguage/JoLE/Responses/ResponseSubmission/")


d = read.csv("ANU_numTones_SpecificHumidity_GlottoFams.csv",header=TRUE, stringsAsFactors = F)
comp = d$Number.of.tones>=3
simp  = d$Number.of.tones<3

n.sample = 5000


quantile_f = function(X,q){
  # Percentile
  sort(X)[(q*length(X))]
}


samp2Fam = function(q, complexLanguages, rand =F, sampleBy='Family', measure = 'Q'){
	# sample 1 specH.mean per language family for complex langauges
  # (and where Family is not NA)
  sel = complexLanguages & !is.na(d[,sampleBy])
	complex = tapply(d[sel,]$specH.mean,d[sel,sampleBy],sample,size=1)

	# Select 1 language per language family, ignoring tone
	# (for Baseline 2)
	sel = !is.na(d[,sampleBy])
	rand = tapply(d[sel,]$specH.mean,d[sel,sampleBy],sample,size=1)

	
	#  sample 1 language per family for non-complex languages
	sel = (!complexLanguages) & (!is.na(d[,sampleBy]))
	simple = tapply(d[sel,]$specH.mean,d[sel,sampleBy],sample,size=1)
	
	# choose same number of points in each sample
	complex = complex[!is.na(complex)]
	simple = simple[!is.na(simple)]
	rand = rand[!is.na(rand)]
	
	lmin = min(c(length(complex),length(simple)))
	complex = complex[sample(1:length(complex), lmin)]
	simple = simple[sample(1:length(simple), lmin)]
	rand = rand[sample(1:length(rand), lmin)]
	
	# What measure should we return?
	# differnece in quantiles, means or medians?
	if(measure=='Q'){
	qcomplex = quantile_f(complex,q)
	qsimple = quantile_f(simple,q)
	qrand = quantile_f(rand,q)
	}
	if(measure=="Mean"){
	  qcomplex = mean(complex)
	  qsimple = mean(simple)
	  qrand = mean(rand)
	}
	if(measure=="Median"){
	  qcomplex = median(complex)
	  qsimple = median(simple)
	  qrand = median(rand)
	}
	
	# return difference in above
  return(c(test2=qcomplex - qsimple, test3=qrand - qsimple))
	}


#######



# Calculate difference between complex languages and non-complex
set.seed(15615)
m1 = replicate(n.sample,samp2Fam(0.15, comp))
m2 = replicate(n.sample,samp2Fam(0.25, comp))
m3 = replicate(n.sample,samp2Fam(0.5, comp))
m4 = replicate(n.sample,samp2Fam(0.75, comp))

test2 = c(sum(m1[1,]>0)/length(m1[1,]),
sum(m2[1,]>0)/length(m2[1,]),
sum(m3[1,]>0)/length(m3[1,]),
sum(m4[1,]>0)/length(m4[1,]))
print(test2)


test3 = c(sum(m1[1,] > m1[2,])/ length(m1[2,]),
sum(m2[1,] > m2[2,])/ length(m2[2,]),
sum(m3[1,] > m3[2,])/ length(m3[2,]),
sum(m4[1,] > m4[2,])/ length(m4[2,]))
print(test3)



############################
# Using Glottolog families #
############################

# Replace d with data frame where ther are no NAs for glottolog families
# (yes, this is bad practice to have d as a global)
d = d[!is.na(d$gFam),]

comp.g = d[!is.na(d$gFam),]$Number.of.tones>=3

set.seed(15)
set.seed(15615)
m1 = replicate(n.sample,samp2Fam(0.15, comp.g, sampleBy='gFam'))
m2 = replicate(n.sample,samp2Fam(0.25, comp.g, sampleBy='gFam'))
m3 = replicate(n.sample,samp2Fam(0.5, comp.g, sampleBy='gFam'))
m4 = replicate(n.sample,samp2Fam(0.75, comp.g, sampleBy='gFam'))

test2.g = c(sum(m1[1,]>0)/length(m1[1,]),
          sum(m2[1,]>0)/length(m2[1,]),
          sum(m3[1,]>0)/length(m3[1,]),
          sum(m4[1,]>0)/length(m4[1,]))
print(test2.g)


test3.g = c(sum(m1[1,] > m1[2,])/ length(m1[2,]),
          sum(m2[1,] > m2[2,])/ length(m2[2,]),
          sum(m3[1,] > m3[2,])/ length(m3[2,]),
          sum(m4[1,] > m4[2,])/ length(m4[2,]))
print(test3.g)


###################################
# Mean values instead of quantile

m1.g.mean = replicate(n.sample,samp2Fam(0, comp.g,  sampleBy = 'gFam', measure="Mean"))
print("Means")
print("Test2")
mean.res2 = sum(m1.g.mean[1,]>0) / length(m1.g.mean[1,])
print("Test3")
mean.res3 = sum(m1.g.mean[1,]>m1.g.mean[2,]) / length(m1.g.mean[1,])

m1.g.median = replicate(n.sample,samp2Fam(0, comp.g,  sampleBy = 'gFam', measure="Median"))
print("Means")
print("Test2")
median.res2 = sum(m1.g.median[1,]>0) / length(m1.g.median[1,])
print("Test3")
median.res3 = sum(m1.g.median[1,]>m1.g.mean[2,]) / length(m1.g.median[1,])


######

res = data.frame(name=NA,q15=NA,q25=NA,q50=NA,q75=NA)
res = rbind(res,c("Test 2",test2))
res = rbind(res,c("Test 3",test3))
res = rbind(res,c("Test 2, Glottolog",test2.g))
res = rbind(res,c("Test 3, Glottolog",test3.g))
res = rbind(res,c("Test 2 Means",mean.res2,"","",""))
res = rbind(res,c("Test 3 Means",mean.res3,"","",""))

res = rbind(res,c("Test 2 Medians",median.res2,"","",""))
res = rbind(res,c("Test 3 Medians",median.res3,"","",""))

res = res[!is.na(res$name),]
# write.csv(res,file="IndepResults.csv")






