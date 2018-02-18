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
from os import sys
sys.path.insert(0, '../../lib')
from APPM5590 import simpleLR, simpleLREstimate

def problem2d2a():
	plt.figure()
	f = open('../data/P025a.txt', 'r')
	split = f.read().split()
	Y = np.array([float(i) for i in split[1:][1::2]])
	X = np.array([float(i) for i in split[1:][2::2]])
	plt.plot(X,Y,'.')
	plt.title('Scatter Plot of RABE Table 2.3 Data')
	plt.xlabel('X')
	plt.ylabel('Y')

def problem2d2b():
	plt.figure()
	f = open('../data/P027.txt', 'r')
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
	f = open('../data/P027.txt', 'r')
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
	dataFile = "../data/P050.txt"
	df = pd.read_csv(dataFile,sep='\t')
	Y = array(df['Sunday'])
	X = array(df['Daily'])

	lr = simpleLR(Y,X,criticalT=2.04)
	n = len(Y)
	Yhat = lr['beta0Hat'] + lr['beta1Hat']*X
	plt.figure()
	plt.plot(X,Y,'.',markersize=10,color='blue')
	plt.xlabel('Daily')
	plt.ylabel('Sunday')
	plt.title('Scatter Plot of Sunday versus Daily Newspaper Circulation' + \
		'\n (in Thousands)')
	plt.figure()
	plt.plot(X,Y,'.',markersize=10,color='blue')
	plt.xlabel('Daily')
	plt.ylabel('Sunday')
	plt.title('Scatter Plot of Sunday versus Daily Newspaper Circulation' + \
		'\n (in Thousands) with Least Squares Regression Line')

	plt.plot(X, Yhat,color='red')
	print('n: ' + str(lr['n']))
	print('seBeta0hat: ' + str(lr['seBeta0Hat']))
	print('seBeta1Hat: ' + str(lr['seBeta1Hat']))
	print('beta0Hat: ' + str(lr['beta0Hat']))
	print('beta1Hat: ' + str(lr['beta1Hat']))
	print('beta0HatPM: ' + str(lr['beta0HatPM']))
	print('beta1HatPM: ' + str(lr['beta1HatPM']))

	lrEstimate = simpleLREstimate(lr,500,2.04)
	yHat0 = lrEstimate['yHat0']
	muHat0 = lrEstimate['muHat0']
	seY0Hat = lrEstimate['seY0Hat']
	seMu0Hat = lrEstimate['seMu0Hat']
	print("Paper 1")
	print("yHat0: " + str(yHat0))
	print("muHat0: " + str(muHat0))
	print("seY0Hat: " + str(seY0Hat))
	print("seMu0Hat: " + str(seMu0Hat))	
	lrEstimate = simpleLREstimate(lr,2000,2.04)
	yHat0 = lrEstimate['yHat0']
	muHat0 = lrEstimate['muHat0']
	seY0Hat = lrEstimate['seY0Hat']
	seMu0Hat = lrEstimate['seMu0Hat']
	print("Paper 2")
	print("yHat0: " + str(yHat0))
	print("muHat0: " + str(muHat0))
	print("seY0Hat: " + str(seY0Hat))
	print("seMu0Hat: " + str(seMu0Hat))	

	
runAll = 1
if 0 or runAll: problem2d2a()
if 0 or runAll: problem2d2b()
if 0 or runAll: problem2d3()
if 1 or runAll: problem2d12() 

pdb.set_trace()








