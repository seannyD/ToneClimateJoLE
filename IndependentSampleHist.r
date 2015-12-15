#  A method for plotting a density curve, where the height of the curve is the mean density of many independent samples.  
# One language from each family is chosen at random and the density curve is estimated for these samples (using the default kernel density estimation function in R).  This is repeated many times, then the mean curve height is taken for many points along the x axis. 


#setwd("~/Documents/MPI/ClimateAndLanguage/JoLE/Responses/ResponseSubmission/")

indepDensity = function(X, strat, from, to, n, nsample=1000, plot=F){
  
  #breaks = c(-Inf, seq(min(X),max(X),length.out=k),Inf)
  x = density(X,from=from, to=to, n=n)$x
  h = replicate(nsample, density(tapply(X,strat,sample,size=1),from=from, to=to, n=n)$y)
  h.m = rowMeans(h)
  if(plot){
    plot(NA, xlim=c(min(X),max(X)), ylim=c(0,max(h.m)))
    lines(x,h.m)
  }
  return(list(x=x,y=h.m))
  
}


d = read.csv("ANU_numTones_SpecificHumidity_GlottoFams.csv",header=TRUE, stringsAsFactors = F)
comp = d$Number.of.tones>=3
simp  = d$Number.of.tones<3

nx = 100
comp.d = indepDensity(d[comp,]$specH.mean, d[comp,]$Family, min(d$specH.mean), max(d$specH.mean), nx)
simp.d = indepDensity(d[simp,]$specH.mean, d[simp,]$Family,min(d$specH.mean), max(d$specH.mean), nx)


whole.dist = density(d$specH.mean, from=min(d$specH.mean), to=max(d$specH.mean), n=nx)

px = 0.0147
px = sort(d$specH.mean)[0.333*length(d$specH.mean)]
px = quantile(d$specH.mean,0.333,type=1)

pdf(file="IndependentDensityPlot.pdf", width=7, height=5)
plot(NA, xlim=c(min(d$specH.mean),max(d$specH.mean)), ylim=c(0,10+max(c(simp.d$y,comp.d$y))),xlab = 'Mean Specific Humidity', ylab='Density',main='')
#rect(min(d$specH.mean), 0,0.0093, 110, border=NA,col='gray')
#rect(0.0097, 0,0.0145, 110, border=NA,col='gray')
rect(min(d$specH.mean), 0,px - 0.0002, 110, border=NA,col='light gray')
rect(px + 0.0002, 0,max(d$specH.mean), 110, border=NA,col='light gray')
#lines(whole.dist$x,whole.dist$y/1.6, col='dark gray',lty=2)
lines(comp.d$x,comp.d$y,col=2)
lines(simp.d$x,simp.d$y)
legend(0.003,100, legend=c("Complex","Non-Complex"), col=2:1, lty=1, lwd=2)
dev.off()




