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
from numpy import array
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
print('Model 1 Prediction:')
x0model1 = array([1,78]).reshape(-1,1)
exams.partialRegressions[0].predict(x0model1)
print('Model 2 Prediction:')
x0model2 = array([1,85]).reshape(-1,1)
exams.partialRegressions[1].predict(x0model2)
print('Model 3 Prediction:')
x0model3 = array([1,78,85]).reshape(-1,1)
exams.predict(x0model3)


pdb.set_trace()


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
cig.partialRegress([5],rowLabelCol=0,yCol=7)
cig.partialRegress([2,5],rowLabelCol=0,yCol=7)
cig.partialRegress([3],rowLabelCol=0,yCol=7)
cig.partialRegress([2,4,5],rowLabelCol=0,yCol=7)
cig.partialRegress([1,2,3,4,5],rowLabelCol=0,yCol=7)

noFemalePR = cig.partialRegressions[0]
noFemaleNoHSind = cig.partialRegressions[1]
print('Problem 3.14')
print('Part A')
print('SSEFM: ' + str(cig.SSE))
print('SSERM: ' + str(noFemalePR.SSE))
print('n: ' + str(cig.Y.shape[0]))
print('p: ' + str(cig.X.shape[1]))
print('k: ' + str(noFemalePR.X.shape[1]))
print('F: ' + str(cig.fTest[0]))
print('Part B')
print('SSERM: ' + str(noFemaleNoHSind.SSE))
print('SSEFM: ' + str(cig.SSE))
print('n: ' + str(cig.Y.shape[0]))
print('p: ' + str(cig.X.shape[1]))
print('k: ' + str(noFemaleNoHSind.X.shape[1]))
print('F: ' + str(cig.fTest[1]))
print('Part C')
print('beta1Hat' + str(noFemaleNoHSind.betaHat[1]))
print('seBeta1Hat' + str(noFemaleNoHSind.seBetaJ[1]))
print('Part d')
print('rSq, no Income: ' + str(cig.partialRegressions[2].rSq))
print('rSq, only ' +str(cig.partialRegressions[3].dataNames) + ': ' + str(cig.partialRegressions[3].rSq))
print('rSq, only ' +str(cig.partialRegressions[4].dataNames) + ': ' + str(cig.partialRegressions[4].rSq))

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
cows.plotNormalProb()
# cows.plotMatrix()
plt.show()
pdb.set_trace()








