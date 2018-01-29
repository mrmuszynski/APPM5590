#! /usr/bin/env python3
###############################################################################
#
#	Title   : APPM5590hw1.py
#	Author  : Matt Muszynski
#	Date    : 01/21/18
#	Synopsis: Wrapper script for explorer
#
###############################################################################

import pdb
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import normal
from scipy.stats import linregress as lr

b0 = 0
b1 = 3
varE = 4
stdE = np.sqrt(varE)
# set sample size
n = 100

# set number of repeated samples
N = 1000

# set up a matrix to capture all estimates
samplePoints = np.empty(shape=(0,n))

allX = np.empty(shape=(0,n))
allY = np.empty(shape=(0,n))
allYHat = np.empty(shape=(0,n))
allCoeffs = np.empty(shape=(0,2))

for k in range(0,N):
	X = normal(10,1,n)
	Y = b0 + b1*X + normal(0,stdE,n)
	allX = np.vstack([allX,X])
	allY = np.vstack([allY,Y])
	linReg = lr(X,Y)
	coeffs = np.array([linReg.intercept,linReg.slope])
	allCoeffs = np.vstack([allCoeffs,coeffs])
	yHat = coeffs[0] + \
		coeffs[1]*X
	allYHat = np.vstack([allYHat,yHat])
plt.plot(allX,allY,'.',color='grey',markersize=1)
for i in range(0,N): plt.plot(allX[i],allYHat[i],color='b')

pdb.set_trace()

# for k in range(0,N+1):
# 	##########################
# 	# SIMULATE DATASETS

# 	# simulate predictors:
# 	X = normal(10,1,n)

# 	# simulate the outcome
# 	Y = b0+b1*X + normal(0,stdE,100)

# 	######################3

# 	# Fit the SLR model

# 	SLRmodel  = lm(Y~X)
# 	summary(SLRmodel)

# 	# capture the estimates
# 	EstCoefs[,k] = t(t(SLRmodel$coef))

# 	par(new=TRUE)
# 	plot(X,Y,cex=.1,,axes=FALSE,col='darkgrey',xaxs='i',yaxs='i')
# 	#abline(SLRmodel$coef[1],SLRmodel$coef[2],col='black')
# 	abline(reg=SLRmodel,col='black')
# 	box()

# ######### POST COMMENTS

# abline(v=9,lty=3,col='red',lwd=3)
# axis(1, at=9, labels='x=9', tick=TRUE)
pdb.set_trace()

