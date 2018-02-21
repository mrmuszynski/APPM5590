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
	pdb.set_trace()
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

def test_supervisorPerformance():
	sp = MLR()
	sp.dataFile = '../data/P056.txt'
	sp.regress()
	sp.partialRegress([1,3])
	pdb.set_trace()

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






