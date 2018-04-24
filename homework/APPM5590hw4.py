#! /usr/bin/env python3
###############################################################################
#
#	Title   : APPM5590hw4.py
#	Author  : Matt Muszynski
#	Date    : 04/21/18
#	Synopsis: Wrapper script for explorer
#
###############################################################################

import pdb
from os import sys
sys.path.insert(0, '../../lib')
import matplotlib.pyplot as plt
from numpy import array, set_printoptions, ones, zeros, log, vstack, exp
from numpy import log, hstack
from numpy.linalg import inv
from scipy.misc import comb as choose


runAll = 0

###############################################################################
#
#	Beetle Example
#
###############################################################################

dose = array([1.6907,1.7242,1.7552,1.7842,1.8113,1.8369,1.8610,1.8839])
nBeetles = array([59,60,62,56,63,59,62,60])
nKilled = array([6,13,18,28,52,53,61,60])

def updatePI(B,X):
	Z = B.T.dot(vstack([ones(len(X)),X]))[0]
	return exp(Z)/(1+exp(Z))

def updateU(X,Y,N,PI):
	return array([[sum(Y-N*PI)],[sum(X*(Y-N*PI))]])

def updateJ(X,N,PI):
	return array([
	[sum(N*PI*(1-PI)), sum(N*X*PI*(1-PI))],
	[sum(N*X*PI*(1-PI)), sum(N*X**2*PI*(1-PI))]
	])
def updatteB(J,B,U):
	return inv(J).dot((J.dot(B)+U))

def logLiklihood(Y,B,X,N):
	Z = B.T.dot(vstack([ones(len(X)),X]))[0]
	return sum(
		Y*Z-N*log(1+exp(Z))
		)
if 0 or runAll:

	X = dose
	N = nBeetles
	Y = nKilled
	P = nKilled/nBeetles
	B = array([[0],[0]])

	for i in range(0,10):
		PI = updatePI(B,X)
		U = updateU(X,Y,N,PI)
		J = updateJ(X,N,PI)
		B = updatteB(J,B,U)
		print(B)
		print(logLiklihood(Y,B,X,N))


	# plt.plot(X,PI,'.')
	# plt.title('Beetle Mortilty')
	# plt.ylabel('Proportion Killed')
	# plt.xlabel('Dose')
	pdb.set_trace()
###############################################################################
#
#	Problem 1
#
###############################################################################

if 0 or runAll:
	radDose = array(['0','1-9','10-49','100-199','200+'])
	leukemia = array([13,5,5,3,4,18])
	other = array([378,200,151,47,31,33])
	total = array([391,205,156,50,35,51])

	succesPercent = leukemia/total

	leukemiaOdds = succesPercent/(1-succesPercent)
	leukemiaLogOdds = log(leukemiaOdds)

	plt.figure()
	plt.plot(succesPercent,'.')
	plt.title('Percentage of Cancer Deaths Due to Leukemia')
	plt.xlabel('Radiation Dose Bin')
	plt.ylabel('%')

	plt.figure()
	plt.title('Total Cancer Deaths Due to Leukemia and Other Cancers')
	plt.plot(leukemia,'.',label='Leukemia')
	plt.plot(other,'.',label='Other')
	plt.xlabel('Radiation Dose Bin')
	plt.ylabel('Deaths')
	plt.legend()


	pdb.set_trace()
	X = radDose
	N = total
	Y = leukemia
	B = array([[0],[0]])

	for i in range(0,10):
		PI = updatePI(B,X)
		U = updateU(X,Y,N,PI)
		J = updateJ(X,N,PI)
		B = updatteB(J,B,U)
		print(B)
		print(logLiklihood(Y,B,X,N))
		pdb.set_trace()

###############################################################################
#
#	Problem 1
#
###############################################################################

if 1 or runAll:

	CAR = array([1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4])
	AGE = array([1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4])
	y0 = array([65,65,52,310,98,159,175,877,41,117,137,477,11,35,39,167])
	n0 = array([317,476,486,3259,486,1004,1355,7660,223,539,697,3442,40,148,214,1019])
	y1 = array([2,5,4,36,7,10,22,102,5,7,16,63,0,6,8,33])
	n1 = array([20,33,40,316,31,81,122,724,18,39,68,344,3,16,25,114])

	DIST0Percent = sum(y0)/sum(n0)
	DIST1Percent = sum(y1)/sum(n1)
	CAR1Percent = sum(hstack([(y0)[CAR == 1],(y1)[CAR == 1]]))/sum(hstack([(n0)[CAR == 1],(n1)[CAR == 1]]))
	CAR2Percent = sum(hstack([(y0)[CAR == 2],(y1)[CAR == 2]]))/sum(hstack([(n0)[CAR == 2],(n1)[CAR == 2]]))
	CAR3Percent = sum(hstack([(y0)[CAR == 3],(y1)[CAR == 3]]))/sum(hstack([(n0)[CAR == 3],(n1)[CAR == 3]]))
	CAR4Percent = sum(hstack([(y0)[CAR == 4],(y1)[CAR == 4]]))/sum(hstack([(n0)[CAR == 4],(n1)[CAR == 4]]))

	AGE1Percent = sum(hstack([(y0)[AGE == 1],(y1)[AGE == 1]]))/sum(hstack([(n0)[AGE == 1],(n1)[AGE == 1]]))
	AGE2Percent = sum(hstack([(y0)[AGE == 2],(y1)[AGE == 2]]))/sum(hstack([(n0)[AGE == 2],(n1)[AGE == 2]]))
	AGE3Percent = sum(hstack([(y0)[AGE == 3],(y1)[AGE == 3]]))/sum(hstack([(n0)[AGE == 3],(n1)[AGE == 3]]))
	AGE4Percent = sum(hstack([(y0)[AGE == 4],(y1)[AGE == 4]]))/sum(hstack([(n0)[AGE == 4],(n1)[AGE == 4]]))

	plt.figure()
	plt.plot(zeros(len(y0)),y0/n0,'.',label='DIST=0')
	plt.plot(zeros(len(y0))+1,y1/n1,'.',label='DIST=1')
	plt.xlabel('Observation #')
	plt.ylabel('Claim Percentage')
	plt.title('Claim Percentage by Discrict')
	plt.legend()

	plt.figure()
	plt.plot(zeros(8)+1,hstack([(y0/n0)[CAR == 1],(y1/n1)[CAR == 1]]),'.',label='CAR=1')
	plt.plot(zeros(8)+2,hstack([(y0/n0)[CAR == 2],(y1/n1)[CAR == 2]]),'.',label='CAR=2')
	plt.plot(zeros(8)+3,hstack([(y0/n0)[CAR == 3],(y1/n1)[CAR == 3]]),'.',label='CAR=3')
	plt.plot(zeros(8)+4,hstack([(y0/n0)[CAR == 4],(y1/n1)[CAR == 4]]),'.',label='CAR=4')
	plt.xlabel('Observation #')
	plt.ylabel('Claim Percentage')
	plt.title('Claim Percentage by Insurance Category')
	plt.legend()

	plt.figure()
	plt.plot(zeros(8)+1,hstack([(y0/n0)[AGE == 1],(y1/n1)[AGE == 1]]),'.',label='AGE=1')
	plt.plot(zeros(8)+2,hstack([(y0/n0)[AGE == 2],(y1/n1)[AGE == 2]]),'.',label='AGE=2')
	plt.plot(zeros(8)+3,hstack([(y0/n0)[AGE == 3],(y1/n1)[AGE == 3]]),'.',label='AGE=3')
	plt.plot(zeros(8)+4,hstack([(y0/n0)[AGE == 4],(y1/n1)[AGE == 4]]),'.',label='AGE=4')
	plt.xlabel('Observation #')
	plt.ylabel('Claim Percentage')
	plt.title('Claim Percentage by Age')
	plt.legend()

pdb.set_trace()








