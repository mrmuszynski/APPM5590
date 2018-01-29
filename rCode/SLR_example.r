#! /usr/local/bin/Rscript
# Simple linear regression model on a simulated dataset

####################
# SIMULATION SET UP
# set true parameters 
b0 = 0
b1 = 3
varE = 4
stdE = sqrt(varE)

# set sample size
n = 100

# set number of repeated samples
N = 1000

# set up a matrix to capture all estimates
EstCoefs = matrix(0,2,N)

for(k in 1:N) {
##########################
# SIMULATE DATASETS

# simulate predictors:
X = rnorm(n,10,1)

# simulate the outcome
Y = b0+b1*X + rnorm(n,0,stdE)

######################3

# Fit the SLR model

SLRmodel  = lm(Y~X)
summary(SLRmodel)

# capture the estimates
EstCoefs[,k] = t(t(SLRmodel$coef))

par(new=TRUE)
plot(X,Y,cex=.1,,axes=FALSE,col='darkgrey',xaxs='i',yaxs='i')
#abline(SLRmodel$coef[1],SLRmodel$coef[2],col='black')
abline(reg=SLRmodel,col='black')
box()
}


######### POST COMMENTS

abline(v=9,lty=3,col='red',lwd=3)
axis(1, at=9, labels='x=9', tick=TRUE)



