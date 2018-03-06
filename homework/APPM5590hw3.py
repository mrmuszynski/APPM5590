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
from numpy import array, set_printoptions

set_printoptions(linewidth=200)
###############################################################################
#
# RABE 5.4
#
###############################################################################

asIsModel = MLR()
asIsModel.dataFile = '../data/unifiedEducationData.txt'
asIsModel.regress()

temporalModel = MLR()
temporalModel.dataFile = '../data/unifiedEducationData.txt'
temporalModel.regress(yCol=1,rowLabelCol=0,ignoreVars=[5],catVars=[4])

temporalInteractionModel = MLR()
temporalInteractionModel.dataFile = '../data/unifiedEducationData.txt'
temporalInteractionModel.regress(yCol=1,rowLabelCol=0,ignoreVars=[5],catVars=[4],intVars=[(1,4),(2,4),(3,4),(1,5),(2,5),(3,5)])

spatialModel = MLR()
spatialModel.dataFile = '../data/unifiedEducationData.txt'
spatialModel.regress(yCol=1,rowLabelCol=0,ignoreVars=[6],catVars=[4])

spatialInteractionModel = MLR()
spatialInteractionModel.dataFile = '../data/unifiedEducationData.txt'
spatialInteractionModel.regress(yCol=1,rowLabelCol=0,ignoreVars=[6],catVars=[4],
	intVars=[(1,4),(2,4),(3,4),(1,5),(2,5),(3,5),(1,6),(2,6),(3,6)])

###############################################################################
#
# RABE 5.7
#
###############################################################################

election = MLR() 
election.dataFile = '../data/P149.txt'
election.regress(yCol=1,rowLabelCol=0,intVars=[(1,4)])
election.partialRegress([2])

###############################################################################
#
# RABE 6.2
#
###############################################################################

windChill = MLR()
windChill.dataFile = '../data/P175.txt'
windChill.regress()
windChill.scatter3D()
windChill.plotMatrix()
windChill.plotResidualsVPredictors((2,1))
windChill.plotResidualsVFitted()
windChill.plotStandardizedResiduals()
windChill.plotNormalProb()

windChill.partialRegress([1])
windChill.partialRegress([2])

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


windChillPartEInteractions = MLR()
windChillPartEInteractions.dataFile = '../data/P175e.txt'
windChillPartEInteractions.regress(intVars=[(1,2),(1,3)])
windChillPartEInteractions.scatter3D()
windChillPartEInteractions.plotMatrix()
windChillPartEInteractions.plotResidualsVPredictors((3,1))
windChillPartEInteractions.plotResidualsVFitted()
windChillPartEInteractions.plotStandardizedResiduals()
windChillPartEInteractions.plotNormalProb()

from sympy import symbols, expand
V = symbols('V')
T = symbols('T')
sqrtV = symbols('sqrtV')
W = 0.0817*(3.71*sqrtV+5.81-0.25*V)*(T-91.4)+91.4
print(expand(W))
pdb.set_trace()








