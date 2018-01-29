#! /usr/bin/env python3
###############################################################################
#
#	Title   : APPM5590.py
#	Author  : Matt Muszynski
#	Date    : 01/29/18
#	Synopsis: Functions for APPM 5990. I could probably do all this through
#		scipy and pandas, but I feel more comfortable learning it from the
#		inside out.
#
###############################################################################

from numpy import sqrt

def bar(X):
	'''!
	It's a mean, duh. Just doing this for pedagogical reasons.
	RABE 2.1
	'''
	return sum(X)/len(X)

def cov(Y,X):
	'''!
	RABE 2.2
	'''
	Ybar = bar(Y)
	Xbar = bar(X)
	n = len(Y)
	return sum((Y-Ybar)*(X-Xbar))/(n-1)

def z(Y):
	'''!
	RABE 2.3
	'''
	Ybar = bar(Y)
	sigmaY = std(Y)
	return (Y - Ybar)/sigmaY

def std(Y):
	'''!
	RABE 2.4
	'''
	Ybar = bar(Y)
	n = len(Y)
	return sqrt(sum((Y-Ybar)**2)/(n-1))

def cor(Y,X):
	'''!
	RABE 2.6. Equivalent to RABE 2.5 and 2.7.
	'''
	sigmaY = std(Y)
	sigmaX = std(X)
	covYX = cov(Y,X)
	return covYX/(sigmaY*sigmaX)

def simpleLR(Y,X):
	'''!
	A lot of stuff in here
	beta1Hat is from RABE 2.14
	beta0Hat is from RABE 2.15
	Yhat is from RABE 2.16
	e is from RABE 2.18
	'''
	Ybar = bar(Y)
	Xbar = bar(X)

	beta1Hat = sum((Y-Ybar)*(X-Xbar))/sum((X-Xbar)**2)
	beta0Hat = Ybar - beta1Hat*Xbar

	Yhat = beta0Hat + beta1Hat*X
	e = Y - Yhat
	SSE = sum(e**2)
	n = len(Y)
	sigmaHatSq = SSE/n
	sigmaHat = np.sqrt(sigmaHatSq)
	seBeta0Hat = 
	seBeta1Hat = 

	#I'll probably regret returning this as a dict some day. But today
	#I don't know enough about what I'm doing to make a better decision.
	return {
	'beta0Hat': beta0Hat,
	'beta1Hat': beta1Hat,
	'seBeta0Hat': seBeta0Hat,
	'seBeta1Hat': seBeta1Hat,	
	'Yhat': Yhat,
	'n': n,
	'e': e,
	'SSE': SSE
	}












