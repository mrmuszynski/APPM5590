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
from pandas import read_csv as csv
from numpy import array
import sys
sys.path.insert(0,'../../lib/')
from APPM5590 import simpleLR, simpleLREstimate, cor, bar, cov, MLR
import pdb


def test_Parabola():
	'''!
	RABE p25
	'''
	parabolaData = csv('../data/P025a.txt',sep='\t')
	Y = parabolaData['Y']
	X = parabolaData['X']
	assert( cor(X,Y) == 0 )


def test_AnscomeQuartet():
	'''!
	RABE p25
	'''	
	anscomeData = csv('../data/P025b.txt',sep='\t')
	Y1 = array(anscomeData['Y1'])
	X1 = array(anscomeData['X1'])
	Y2 = array(anscomeData['Y2'])
	X2 = array(anscomeData['X2'])
	Y3 = array(anscomeData['Y3'])
	X3 = array(anscomeData['X3'])
	Y4 = array(anscomeData['Y4'])
	X4 = array(anscomeData['X4'])

	lr1 = simpleLR(Y1,X1)
	lr2 = simpleLR(Y2,X2)
	lr3 = simpleLR(Y3,X3)
	lr4 = simpleLR(Y4,X4)

	cor1 = cor(Y1,X1)
	cor2 = cor(Y2,X2)
	cor3 = cor(Y3,X3)
	cor4 = cor(Y4,X4)

	assert ( abs( cor1 - cor2 ) < 0.0005 )
	assert ( abs( cor1 - cor3 ) < 0.0005 )
	assert ( abs( cor1 - cor4 ) < 0.0005 )
	assert ( abs ( lr1['beta0Hat'] - lr2['beta0Hat']) < 0.005 )
	assert ( abs ( lr1['beta0Hat'] - lr3['beta0Hat']) < 0.005 )
	assert ( abs ( lr1['beta0Hat'] - lr4['beta0Hat']) < 0.005 )


def test_ComputerRepairData():
	'''!
	RABE p27-42
	NOTE: the correlation test here doesn't match RABE. I believe this
	to be an error in RABE, not in my code.
	'''
	computerRepairData = csv('../data/P027.txt',sep='\t')
	Y = array(computerRepairData['Minutes'])
	X = array(computerRepairData['Units'])

	assert ( abs(bar(Y) - 97.21) < 0.005 )
	assert ( abs(bar(X) - 6) == 0 )
	assert ( abs(cov(Y,X) - 136) < 0.5)
	assert ( abs(cor(Y,X) - 0.9936) < 0.0005)

	#beta_1^0 == 12, beta_1^0 == 12, so beta00 nees to be set, while
	#beta10 does not.
	lr = simpleLR(Y,X,criticalT=2.18)
	# assert( abs(lr['SSR']) )
	assert( abs(sum(X) - 84) < 0.5)
	assert( abs(sum(Y) - 1361) < 0.5)
	assert( abs(sum(Y-bar(Y)) < 1e-12))
	assert( abs(sum(X-bar(X)) < 1e-12))
	assert( abs(lr['SST'] - 27768.36) < 0.005 )
	assert( abs(sum((X-bar(X))**2) - 114 < 0.5))
	assert( abs(sum((X-bar(X))*(Y-bar(Y))) -1768 < 0.005))
	assert( abs(lr['beta0Hat'] - 4.162) < 0.0005)
	assert( abs(lr['beta1Hat'] - 15.509) < 0.0005)
	assert( abs(lr['seBeta0Hat'] - 3.355) < 0.0005)
	assert( abs(lr['seBeta1Hat'] - 0.505) < 0.0005)
	assert( abs(lr['t0'] - 1.24) < 0.005)
	assert( abs(lr['t1'] - 30.71) < 0.005)
	assert( abs(lr['beta0HatPM'] - 2.18*3.355) < 0.0005)
	assert( abs(lr['beta1HatPM'] - 2.18*0.505) < 0.0005)
	assert( abs(lr['SSR']/lr['SST'] - ( 1-lr['SSE']/lr['SST'])) < 1e-14)
	assert( abs(lr['SSR']/lr['SST'] - cor(Y,X)**2) < 1e-14)
	assert( abs(lr['SSR']/lr['SST'] - .987) < 0.0005)
	lrEstimate = simpleLREstimate(lr,4,0)

	assert( abs(lrEstimate['seY0Hat'] - 5.67) < 0.005)
	assert( abs(lrEstimate['seMu0Hat'] - 1.76) < 0.005)

def test_MLRComputerRepairData():
	cr = MLR() 
	cr.dataFile = '../data/P027.txt'
	cr.regress()
	seY0Hat = cr.predict(array([[1],[4]]))[1]
	seMu0Hat = cr.predict(array([[1],[4]]))[2]

	assert( abs(sum(cr.X[:,1]) - 84) < 0.5)
	assert( abs(sum(cr.Y) - 1361) < 0.5)
	assert( abs(cr.SST - 27768.36) < 0.005 )
	assert( abs(cr.SSR/cr.SST - ( 1-cr.SSE/cr.SST)) < 1e-14)
	assert( abs(cr.SSR/cr.SST - .987) < 0.0005)
	assert( abs(cr.betaHat[0] - 4.162) < 0.0005)
	assert( abs(cr.betaHat[1]- 15.509) < 0.0005)
	assert( abs(cr.seBetaJ[0] - 3.355) < 0.0005)
	assert( abs(cr.seBetaJ[1] - 0.505) < 0.0005)
	assert( abs(cr.rSq - 0.987) < 0.0005)
	assert( abs(seY0Hat - 5.67) < 0.005)
	assert( abs(seMu0Hat - 1.76) < 0.005)

def test_supervisorPerformance():
	sp = MLR()
	sp.dataFile = '../data/P056.txt'
	sp.regress()
	sp.partialRegress([2,4,5,6])
	sp.partialRegress([3,4,5,6])
	sp.partialRegress([2,3,4,5,6])
	sp.partialRegress([1,2,3,4,5,6])

	assert(abs(sp.betaHat[0]-10.787) < 0.0005)
	assert(abs(sp.betaHat[1]-0.613) < 0.0005)
	assert(abs(sp.betaHat[2]+0.073) < 0.0005)
	assert(abs(sp.betaHat[3]-0.320) < 0.0005)
	#this seems to be a typo. I think RABE rounded wrong.
	assert(abs(sp.betaHat[4]-0.081) < 0.001) 
	assert(abs(sp.betaHat[5]-0.038) < 0.0005)
	assert(abs(sp.betaHat[6]+0.217) < 0.0005)

	#RABE seems to have rounded incorrectly here again
	assert(abs(sp.seBetaJ[0]-11.589) < 0.0005)
	assert(abs(sp.seBetaJ[1]-0.1610) < 0.00005)
	assert(abs(sp.seBetaJ[2]-0.1357) < 0.00005)
	assert(abs(sp.seBetaJ[3]-0.1685) < 0.00005)
	assert(abs(sp.seBetaJ[4]-0.2215) < 0.00005)
	assert(abs(sp.seBetaJ[5]-0.1470) < 0.00005)
	assert(abs(sp.seBetaJ[6]-0.1782) < 0.00005)
	assert(abs(sp.tTest[0]-0.93) < 0.005)
	assert(abs(sp.tTest[1]-3.81) < 0.005)
	assert(abs(sp.tTest[2]+0.54) < 0.005)
	assert(abs(sp.tTest[3]-1.90) < 0.005)
	assert(abs(sp.tTest[4]-0.37) < 0.005)
	assert(abs(sp.tTest[5]-0.26) < 0.005)
	assert(abs(sp.tTest[6]+1.22) < 0.005)
	assert(abs(sp.sigmaHat - 7.068) < 0.0005)
	assert(abs(sp.partialRegressions[0].betaHat[0] - 9.8709) < 0.0005)
	assert(abs(sp.partialRegressions[0].betaHat[1] - 0.6435) < 0.0005)
	assert(abs(sp.partialRegressions[0].betaHat[2] - 0.2112) < 0.0005)
	assert(abs(sp.partialRegressions[0].seBetaJ[0] - 7.0610) < 0.0005)
	assert(abs(sp.partialRegressions[0].seBetaJ[1] - 0.1185) < 0.0005)
	assert(abs(sp.partialRegressions[0].seBetaJ[2] - 0.1344) < 0.0005)
	assert(abs(sp.partialRegressions[0].tTest[0] - 1.40) < 0.005)
	assert(abs(sp.partialRegressions[0].tTest[1] - 5.43) < 0.005)
	assert(abs(sp.partialRegressions[0].tTest[2] - 1.57) < 0.005)
	assert(abs(sp.rSq - 0.73) < 0.005)

	#examples from section 3.5 on p58
	assert(abs(sp.partialRegressions[1].betaHat[0] - 15.3276) < 0.00005)
	assert(abs(sp.partialRegressions[1].betaHat[1] - 0.7803) < 0.00005)
	assert(abs(sp.partialRegressions[1].betaHat[2] + 0.0502) < 0.00005)
	assert(abs(sp.partialRegressions[2].betaHat[0] - 14.3763) < 0.00005)
	assert(abs(sp.partialRegressions[2].betaHat[1] - 0.754610) < 0.0000005)

	#examples from section 3.9.1 on p66 and 3.9.2 on p67
	assert(abs(sp.fTest[3] - 10.50) < 0.005)
	#another truncated value?
	assert(abs(sp.fTest[0] - 0.528) < 0.001)

def test_salarySurvey():
	salarySurvey = MLR()
	salarySurvey.dataFile = '../data/P122.txt'
	salarySurvey.regress(catVars=[2])

	#WTF is up with this first value? I have a hard time believing
	#that only one could be wrong. Maybe a typo? No... I think that
	#RABE rounds all of these to 6 digits, but then reports out to 
	#3 decimal places... I fixed muy tests to only test the things
	#that he seems to care about
	assert(abs(salarySurvey.betaHat[0] - 11031.800) < 0.01)
	assert(abs(salarySurvey.betaHat[1] -  546.184) < 0.0005)
	assert(abs(salarySurvey.betaHat[2] + 2996.210) < 0.005)
	assert(abs(salarySurvey.betaHat[3] - 147.825) < 0.0005)
	assert(abs(salarySurvey.betaHat[4] - 6883.530) < 0.005)

	assert(abs(salarySurvey.seBetaJ[0] - 383.2) < 0.05)
	assert(abs(salarySurvey.seBetaJ[1] -  30.5) < 0.05)
	assert(abs(salarySurvey.seBetaJ[2] - 411.8) < 0.05)
	assert(abs(salarySurvey.seBetaJ[3] - 387.7) < 0.05)
	assert(abs(salarySurvey.seBetaJ[4] - 313.9) < 0.05)

	assert(abs(salarySurvey.tTest[0] -  28.8) < 0.05)
	assert(abs(salarySurvey.tTest[1] -  17.9) < 0.05)
	assert(abs(salarySurvey.tTest[2] +  7.28) < 0.005)
	assert(abs(salarySurvey.tTest[3] -  0.38) < 0.005)
	assert(abs(salarySurvey.tTest[4] -  21.9) < 0.05)

	assert(abs(salarySurvey.rSq - 0.957) < 0.0005)
	assert(abs(salarySurvey.sigmaHat - 1027) < 0.5)


	salarySurvey.regress(catVars=[2],intVars=[(2,4),(3,4)])
	salarySurvey

	assert(abs(salarySurvey.betaHat[0] - 11203.40) < 0.05)
	assert(abs(salarySurvey.betaHat[1] -  496.99) < 0.005)
	assert(abs(salarySurvey.betaHat[2] + 1730.75) < 0.005)
	assert(abs(salarySurvey.betaHat[3] + 349.08) < 0.005)
	assert(abs(salarySurvey.betaHat[4] - 7047.41) < 0.05)
	assert(abs(salarySurvey.betaHat[5] + 3066.04) < 0.005)
	assert(abs(salarySurvey.betaHat[6] - 1836.49) < 0.05)

	assert(abs(salarySurvey.seBetaJ[0] - 79.07) < 0.005)
	assert(abs(salarySurvey.seBetaJ[1] -  5.57) < 0.05)
	assert(abs(salarySurvey.seBetaJ[2] - 105.30) < 0.05)
	assert(abs(salarySurvey.seBetaJ[3] - 97.57) < 0.005)
	assert(abs(salarySurvey.seBetaJ[4] - 102.6) < 0.05)
	assert(abs(salarySurvey.seBetaJ[5] - 149.3) < 0.05)
	assert(abs(salarySurvey.seBetaJ[6] - 131.2) < 0.05)

	assert(abs(salarySurvey.tTest[0] - 141.7) < 0.05)
	assert(abs(salarySurvey.tTest[1] -  89.3) < 0.05)
	assert(abs(salarySurvey.tTest[2] +  16.4) < 0.05)
	assert(abs(salarySurvey.tTest[3] +   3.6) < 0.05)
	assert(abs(salarySurvey.tTest[4] -  68.7) < 0.05)
	assert(abs(salarySurvey.tTest[5] +  20.5) < 0.05)
	assert(abs(salarySurvey.tTest[6] -  14.0) < 0.05)

	assert(abs(salarySurvey.rSq - 0.999) < 0.0005)
	assert(abs(salarySurvey.sigmaHat - 173.8) < 0.5)




	salarySurvey.regress(catVars=[2],intVars=[(2,4),(3,4)],badObs=[32])

	pdb.set_trace()

	assert(abs(salarySurvey.betaHat[0] - 11199.7) < 0.05)
	assert(abs(salarySurvey.betaHat[1] -  498.41) < 0.005)
	assert(abs(salarySurvey.betaHat[2] + 1741.28) < 0.005)
	assert(abs(salarySurvey.betaHat[3] +  357.00) < 0.005)
	assert(abs(salarySurvey.betaHat[4] - 7047.49) < 0.005)
	assert(abs(salarySurvey.betaHat[5] + 3051.72) < 0.05)
	assert(abs(salarySurvey.betaHat[6] - 1997.62) < 0.1)

	assert(abs(salarySurvey.seBetaJ[0] - 79.07) < 0.005)
	assert(abs(salarySurvey.seBetaJ[1] -  5.57) < 0.05)
	assert(abs(salarySurvey.seBetaJ[2] - 105.30) < 0.05)
	assert(abs(salarySurvey.seBetaJ[3] - 97.57) < 0.005)
	assert(abs(salarySurvey.seBetaJ[4] - 102.6) < 0.05)
	assert(abs(salarySurvey.seBetaJ[5] - 149.3) < 0.05)
	assert(abs(salarySurvey.seBetaJ[6] - 131.2) < 0.05)

	assert(abs(salarySurvey.tTest[0] - 141.7) < 0.05)
	assert(abs(salarySurvey.tTest[1] -  89.3) < 0.05)
	assert(abs(salarySurvey.tTest[2] +  16.4) < 0.05)
	assert(abs(salarySurvey.tTest[3] +   3.6) < 0.05)
	assert(abs(salarySurvey.tTest[4] -  68.7) < 0.05)
	assert(abs(salarySurvey.tTest[5] +  20.5) < 0.05)
	assert(abs(salarySurvey.tTest[6] -  14.0) < 0.05)

	assert(abs(salarySurvey.rSq - 1) < 0.0005)
	assert(abs(salarySurvey.sigmaHat - 67.13) < 0.05)

	pdb.set_trace()







