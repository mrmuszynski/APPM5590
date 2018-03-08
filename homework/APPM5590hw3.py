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
from os import sys
sys.path.insert(0, '../../lib')
from APPM5590 import MLR
import matplotlib.pyplot as plt
from numpy import array, set_printoptions, sqrt

set_printoptions(linewidth=200)
runall = 0

###############################################################################
#
# RABE 5.4
#
###############################################################################
if 0 or runall:
	asIsModel = MLR()
	asIsModel.dataFile = '../data/unifiedEducationData.txt'
	asIsModel.regress(yCol=1,rowLabelCol=0)

	temporalModel = MLR()
	temporalModel.dataFile = '../data/unifiedEducationData.txt'
	temporalModel.regress(yCol=1,rowLabelCol=0,ignoreVars=[5])

	temporalCategoricalModel = MLR()
	temporalCategoricalModel.dataFile = '../data/unifiedEducationData.txt'
	temporalCategoricalModel.regress(yCol=1,rowLabelCol=0,catVars=[4],ignoreVars=[5])

	temporalInteractionModel = MLR()
	temporalInteractionModel.dataFile = '../data/unifiedEducationData.txt'
	temporalInteractionModel.regress(yCol=1,rowLabelCol=0,ignoreVars=[5],catVars=[4],
		intVars=[(1,4),(2,4),(3,4),(1,5),(2,5),(3,5)])

	spatialModel = MLR()
	spatialModel.dataFile = '../data/unifiedEducationData.txt'
	spatialModel.regress(yCol=1,rowLabelCol=0,ignoreVars=[6])

	spatialCategoricalModel = MLR()
	spatialCategoricalModel.dataFile = '../data/unifiedEducationData.txt'
	spatialCategoricalModel.regress(yCol=1,rowLabelCol=0,catVars=[4],ignoreVars=[6])

	spatialInteractionModel = MLR()
	spatialInteractionModel.dataFile = '../data/unifiedEducationData.txt'
	spatialInteractionModel.regress(yCol=1,rowLabelCol=0,catVars=[4],ignoreVars=[6],
		intVars=[(1,4),(2,4),(3,4),(1,5),(2,5),(3,5),(1,6),(2,6),(3,6)])

	bothInteractionModel = MLR()
	bothInteractionModel.dataFile = '../data/unifiedEducationData.txt'
	bothInteractionModel.regress(
		yCol=1,rowLabelCol=0,catVars=[4,5],
		intVars=[
			(1,4),(2,4),(3,4),
			(1,5),(2,5),(3,5),
			(1,6),(2,6),(3,6),
			(1,7),(2,7),(3,7),
			(1,8),(2,8),(3,8)
			])

	temporalModel.plotNormalProb()
	temporalCategoricalModel.plotNormalProb()
	temporalInteractionModel.plotNormalProb()
	spatialModel.plotNormalProb()
	spatialCategoricalModel.plotNormalProb()
	spatialInteractionModel.plotNormalProb()
	bothInteractionModel.plotNormalProb()


	#remove Time interaction Terms
	bothInteractionModel.partialRegress([19,20,21,22,23,24])
	
	#remove non-interaction Time Terms
	bothInteractionModel.partialRegress([8,9])

	#remove ALL Time Terms
	bothInteractionModel.partialRegress([8,9,19,20,21,22,23,24])

	#Remove Region Interaction Terms
	bothInteractionModel.partialRegress([10,11,12,13,14,15,16,17,18])

	#remove non-interaction Region Terms
	bothInteractionModel.partialRegress([10,11])

	#Remove All Region Terms
	bothInteractionModel.partialRegress([5,6,7,10,11,12,13,14,15,16,17,18])

	#Remove All Interaction Terms
	bothInteractionModel.partialRegress(
		[10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])

	#Remove All Categorical Terms
	bothInteractionModel.partialRegress([5,6,7,8,9])

	bestModelYet = MLR()
	bestModelYet.dataFile = '../data/unifiedEducationData.txt'
	bestModelYet.regress(
		yCol=1,rowLabelCol=0,catVars=[4,5],
		intVars=[
			(1,7),(2,7),(3,7),
			(1,8),(2,8),(3,8)
			])

###############################################################################
#
# RABE 5.7
#
###############################################################################

if 1 or runall:
	election = MLR() 
	election.dataFile = '../data/P149.txt'
	election.regress(yCol=1,rowLabelCol=0,intVars=[(1,4)])
	election.partialRegress([5])
	election.partialRegress([2,5])
	election.partialRegress([5,8])
	election.partialRegress([2,5,8])

	fTestResult1 = election.partialRegressions[0].runFTest(election.partialRegressions[1],saveResult=0)
	fTestResult2 = election.partialRegressions[0].runFTest(election.partialRegressions[2],saveResult=0)

	election3 = MLR() 
	election3.dataFile = '../data/P149.txt'
	election3.regress(yCol=1,rowLabelCol=0,
		intVars=[
		(1,4),(1,6),(2,6)
		])

	election3.partialRegress([2])
	election3.partialRegressions[0].partialRegress([9])
	election3.partialRegressions[0].latexTable()
	print(election3.partialRegressions[0].fTest)
	print(election3.partialRegressions[0].fDOF)
###############################################################################
#
# RABE 6.2
#
###############################################################################

if 0 or runall:

	windChill = MLR()
	windChill.dataFile = '../data/P175.txt'
	windChill.regress()
	# windChill.scatter3D()
	# windChill.plotMatrix()
	# windChill.plotResidualsVPredictors((2,1))
	# windChill.plotResidualsVFitted()
	# windChill.plotStandardizedResiduals()
	# windChill.plotNormalProb()

	windChill.partialRegress([1])
	windChill.partialRegress([2])

	from numpy import unique
	plt.figure()
	for each in	unique(windChill.X[:,2]):
		plt.title('V versus W Contours')
		plt.xlabel('V')
		plt.ylabel('W')
		ind = windChill.X[:,2] == each
		plt.plot(windChill.X[:,1][ind],windChill.Y[ind],'.')

	plt.figure()
	for each in	unique(windChill.X[:,1]):
		plt.title('T versus W Contours')
		plt.xlabel('T')
		plt.ylabel('W')
		ind = windChill.X[:,1] == each
		plt.plot(windChill.X[:,2][ind],windChill.Y[ind],'.')


	def funcW(V,T):
		return 0.0817*(3.71*sqrt(V)+5.81-0.25*V)*(T-91.4)+91.4

	Vdat = windChill.X[:,1]
	Tdat = windChill.X[:,2]

	# plt.figure()
	# plt.plot(funcW(Vdat,Tdat),windChill.Y.T[0],'.')
	# plt.figure()
	# plt.plot((funcW(Vdat,Tdat) - windChill.Y.T)[0],windChill.Yhat.T[0],'.')
	# plt.figure()
	# plt.plot((-funcW(Vdat,Tdat)+windChill.Y.T[0]),'.')
	windChillD = MLR()
	windChillD.dataFile = '../data/P175.txt'
	windChillD.regress(catVars=[1],intVars=[
		(1,10),(2,10),(3,10),(4,10),(5,10),
		(6,10),(7,10),(8,10),(9,10)
		])

	# for each in windChill.partialRegressions:
	# 	each.scatterPlot(each)
	# 	each.plotMatrix()
	# 	# each.plotResidualsVPredictors((1,1))
	# 	each.plotResidualsVFitted()
	# 	each.plotStandardizedResiduals()
	# 	each.plotNormalProb()

	windChillPartE = MLR()
	windChillPartE.dataFile = '../data/P175e.txt'
	windChillPartE.regress()
	windChillPartE.scatter3D()
	windChillPartE.plotMatrix()
	windChillPartE.plotResidualsVPredictors((3,1))
	windChillPartE.plotResidualsVFitted()
	windChillPartE.plotStandardizedResiduals()
	windChillPartE.plotNormalProb()
	windChillPartE.partialRegress([1])
	windChillPartE.partialRegress([2])
	windChillPartE.partialRegress([3])

	windChillPartEInteractions = MLR()
	windChillPartEInteractions.dataFile = '../data/P175e.txt'
	windChillPartEInteractions.regress(intVars=[(1,2),(1,3)])
	# windChillPartEInteractions.scatter3D()
	# windChillPartEInteractions.plotMatrix()
	# windChillPartEInteractions.plotResidualsVPredictors((3,1))
	windChillPartEInteractions.plotResidualsVFitted()
	windChillPartEInteractions.plotStandardizedResiduals()
	windChillPartEInteractions.plotNormalProb()
	# windChillPartEInteractions.partialRegress([1])
	# windChillPartEInteractions.partialRegress([2])
	# windChillPartEInteractions.partialRegress([3])
	# windChillPartEInteractions.partialRegress([4])
	# windChillPartEInteractions.partialRegress([5])

	# F test fails to reject null
	windChillPartEMoreInteractions = MLR()
	windChillPartEMoreInteractions.dataFile = '../data/P175e.txt'
	windChillPartEMoreInteractions.regress(intVars=[(1,2),(1,3),(2,3)])

	windChillF1 = MLR()
	windChillF1.dataFile = '../data/P175f1.txt'
	windChillF1.regress(intVars=[(1,2),(1,3),(2,3)])


	windChillF2 = MLR()
	windChillF2.dataFile = '../data/P175f2.txt'
	windChillF2.regress(intVars=[(1,2),(1,3),(2,3)])

	from sympy import symbols, expand
	V = symbols('V')
	T = symbols('T')
	sqrtV = symbols('sqrtV')
	W = 0.0817*(3.71*sqrtV+5.81-0.25*V)*(T-91.4)+91.4
	print(expand(W))

###############################################################################
#
# RABE 6.5
#
###############################################################################

if 0 or runall:
	mbPrice = MLR()
	mbPrice.dataFile = '../data/P177altered.txt'
	mbPrice.regress(yCol=3,ignoreVars=[0,1])
	mbPrice.partialRegress([1])

	mbPriceLn = MLR()
	mbPriceLn.dataFile = '../data/P177altered.txt'
	mbPriceLn.regress(yCol=3,ignoreVars=[0,1],yTransform='ln')
	mbPriceLn.partialRegress([1])

	mbPriceInteraction = MLR()
	mbPriceInteraction.dataFile = '../data/P177altered.txt'
	mbPriceInteraction.regress(
		yCol=3,ignoreVars=[0],yTransform='ln',intVars=[(1,2)])

	plt.title('Scatter Plot with Two Fits')
	plt.plot(mbPriceInteraction.X[:,2],mbPriceInteraction.X[:,2]*(mbPriceInteraction.betaHat[2]+mbPriceInteraction.betaHat[3])+mbPriceInteraction.betaHat[0]+mbPriceInteraction.betaHat[1],
		label='1988-91 fit')
	plt.plot(mbPriceInteraction.X[:,2],mbPriceInteraction.X[:,2]*(mbPriceInteraction.betaHat[2])+mbPriceInteraction.betaHat[0],
		label='1992-98 fit')
	plt.plot(mbPriceInteraction.X[:,2],mbPriceInteraction.Y,'.',label='Raw Data')
	plt.xlabel('Years Since 1988')
	plt.ylabel('Price')
	plt.legend()
pdb.set_trace()








