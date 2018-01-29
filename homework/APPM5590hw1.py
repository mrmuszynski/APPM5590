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
import pandas as pd
from scipy.stats import linregress, sem
from numpy import array, sqrt, mean
def problem2d2a():
	plt.figure()
	f = open('../data/P029a.txt', 'r')
	split = f.read().split()
	Y = np.array([float(i) for i in split[1:][1::2]])
	X = np.array([float(i) for i in split[1:][2::2]])
	plt.plot(X,Y,'.')
	plt.title('Scatter Plot of RABE Table 2.3 Data')
	plt.xlabel('X')
	plt.ylabel('Y')

def problem2d2b():
	plt.figure()
	f = open('../data/P031.txt', 'r')
	split = f.read().split()
	minutes = np.array([float(i) for i in split[1:][1::2]])
	units = np.array([float(i) for i in split[1:][2::2]])
	plt.plot(minutes,units,'.')
	plt.title('Scatter Plot of RABE Table 2.3 Data')
	plt.xlabel('Minutes')
	plt.ylabel('Units')

def problem2d3():
	criticalT = 2.18
	beta0hat = 4.162
	beta1hat = 15.509
	f = open('../data/P031.txt', 'r')
	split = f.read().split()
	minutes = np.array([float(i) for i in split[1:][1::2]])
	units = np.array([float(i) for i in split[1:][2::2]])

	plt.figure()
	plt.plot(minutes,units,'.')
	plt.plot(beta0hat + beta1hat*units,units)
	plt.title('Scatter Plot of RABE Table 2.3 Data with Fit')
	plt.xlabel('Minutes')
	plt.ylabel('Units')

	seBeta0hat = 3.355
	seBeta1hat = 0.505
	beta0hatPM = criticalT*seBeta0hat
	beta1hatPM = criticalT*seBeta1hat

	plt.figure()
	plt.plot(minutes,units,'.')
	plt.plot(beta0hat + beta0hatPM + (beta1hat + beta1hatPM)*units,
		units,color='orange')
	plt.plot(beta0hat - beta0hatPM + (beta1hat - beta1hatPM)*units,
		units,color='orange')
	plt.title('Scatter Plot of RABE Table 2.3 Data with 99% Confidence Bounds')
	plt.xlabel('Minutes')
	plt.ylabel('Units')

def problem2d12():
	dataFile = "../data/P054.txt"
	df = pd.read_csv(dataFile,sep='\t')
	X = array(df['Sunday'])
	Y = array(df['Daily'])
	lr = linregress(X,Y)
	Yhat = lr.intercept + lr.slope*X
	sigmaHatSq = sum((Y - Yhat)**2)/(len(Y)-2)
	sigmaHat = sqrt(sigmaHatSq)
	Xbar = mean(X)
	seBeta0hat = sigmaHat*sqrt(len(Y)**-1 + Xbar**2/sum((X-Xbar)**2))
	seBeta1hat = sigmaHat/sqrt(sum((X-Xbar)**2))
	# seBeta0hat = sem()
	# seBeta1hat = sem()
	df.plot.scatter('Sunday','Daily')
	plt.title('Scatter Plot of Sunday versus Daily Newspaper Circulation' + \
		'\n (in Thousands)')

	df.plot.scatter('Sunday','Daily')
	plt.title('Scatter Plot of Sunday versus Daily Newspaper Circulation' + \
		'\n (in Thousands) with Least Squares Regression Line')


	plt.plot(X, Yhat,color='red')
	pdb.set_trace()
	
runAll = 0
if 0 or runAll: problem2d2a()
if 0 or runAll: problem2d2b()
if 0 or runAll: problem2d3()
if 1 or runAll: problem2d12() 

pdb.set_trace()








