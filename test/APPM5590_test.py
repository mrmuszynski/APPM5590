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
sys.path.insert(0,'../lib/')
from APPM5590 import simpleLR, cor, bar, cov
import pdb


def test_Parabola():
	'''!
	RABE p25
	'''
	parabolaData = csv('../data/P029a.txt',sep='\t')
	Y = parabolaData['Y']
	X = parabolaData['X']
	assert( cor(X,Y) == 0 )


def test_AnscomeQuartet():
	'''!
	RABE p25
	'''	
	anscomeData = csv('../data/P029b.txt',sep='\t')
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


def test_ComputerReparData():
	'''!
	RABE p27-42
	NOTE: the correlation test here doesn't match RABE. I believe this
	to be an error in RABE, not in my code.
	'''
	computerRepairData = csv('../data/P031.txt',sep='\t')
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
	pdb.set_trace()











