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
###############################################################################
#
# RABE 3.3
#
###############################################################################


exams = MLR()
exams.dataFile = '../data/P076.txt'
exams.regress()
exams.partialRegress([1])
exams.partialRegress([2])
pdb.set_trace()
#Part A. 
#Make all the plots we want to have to show we did the job
exams.scatterAllPartials()
exams.scatter3D()
exams.plotMatrix()
#print beta values so they can be put in latex
print('')
print('Model 1 Betas: ' + str(exams.partialRegressions[0].betaHat.T[0]))
print('Model 2 Betas: ' + str(exams.partialRegressions[1].betaHat.T[0]))
print('Model 3 Betas: ' + str(exams.betaHat.T[0]))
#Part B
#print beta values so they can be put in latex
print('')
print('Model 1 seBetas: ' + str(exams.partialRegressions[0].seBetaJ.T[0]))
print('Model 2 seBetas: ' + str(exams.partialRegressions[1].seBetaJ.T[0]))
print('Model 3 seBetas: ' + str(exams.seBetaJ.T[0]))
print('Model 1 tTests: ' + str(exams.partialRegressions[0].tTest.T[0]))
print('Model 2 tTests: ' + str(exams.partialRegressions[1].tTest.T[0]))
print('Model 3 tTests: ' + str(exams.tTest.T[0]))
print('Model 1 rSq: ' + str(exams.partialRegressions[0].rSq))
print('Model 2 rSq: ' + str(exams.partialRegressions[1].rSq))
print('Model 3 rSq: ' + str(exams.rSq))
print('Model 1 SSE: ' + str(exams.partialRegressions[0].SSE))
print('Model 2 SSE: ' + str(exams.partialRegressions[1].SSE))
print('Model 3 SSE: ' + str(exams.SSE))


###############################################################################
#
# RABE 3.14
#
###############################################################################
cig = MLR()
cig.dataFile = '../data/P081.txt'
#regress full model
cig.regress(rowLabelCol=0,yCol=7)
#regress without female
# cig.partialRegress([5],rowLabelCol=0,yCol=7)
# cig.partialRegress([2,5],rowLabelCol=0,yCol=7)
# cig.partialRegress([3],rowLabelCol=0,yCol=7)
# cig.partialRegress([2,4,5],rowLabelCol=0,yCol=7)
# cig.partialRegress([1,2,4,5,6],rowLabelCol=0,yCol=7)
cig.partialRegress([2,3,4,5,6],rowLabelCol=0,yCol=7)
cig.partialRegress([1,3,4,5,6],rowLabelCol=0,yCol=7)
cig.partialRegress([1,2,4,5,6],rowLabelCol=0,yCol=7)
cig.partialRegress([1,2,3,5,6],rowLabelCol=0,yCol=7)
cig.partialRegress([1,2,3,4,6],rowLabelCol=0,yCol=7)
cig.partialRegress([1,2,3,4,5],rowLabelCol=0,yCol=7)

cig.plotMatrix()
pdb.set_trace()


###############################################################################
#
# RABE 4.1a
#
###############################################################################

cows = MLR()
cows.dataFile = '../data/P004.txt'
cows.regress()
cows.plotResidualsVPredictors((3,2))
cows.plotResidualsVFitted()
# cows.plotMatrix()
plt.show()
pdb.set_trace()








