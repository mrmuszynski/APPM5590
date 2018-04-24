#! /usr/bin/env python3

'''This module provides Python/statsmodel solutions to all code examples in

Dobson AJ & Barnett AG: "An Introduction to Generalized Linear Models"
3rd ed
CRC Press(2008)

Points that still need to be done are marked with "tbd" below:

- [Unclear] Clarify the exact definition of "loglog" and "cloglog" in the differnent
  languages.

- [Unclear] in "senility_and_WAIS" I don't understand what the "grouped response"
  is supposed to mean

- [Missing 1] "ordinal_logistic_regression" is not yet implemented in statsmodels

- [Missing 2] Cox proportional hazards are not yet implemented in statsmodels

- [Missing 3] Repeated measures models are not yet implemented in statsmodels

Dependencies
------------
python3, numpy, pandas, patsy, statsmodels

author: thomas haslwanter
date:   March 2017
ver:    0.22

'''

# Standard libraries
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
import patsy

# The required modules from "statsmodels"
import statsmodels.api as sm
import statsmodels.stats.api as sm_stats
import statsmodels.formula.api as smf
import statsmodels.genmod.families as sm_families

# for data import
import urllib
import zipfile
import io

import pdb 

def get_data(inFile):
    '''Extract data from a zipped-archive'''

    # get the zip-archive
    url = 'http://cdn.crcpress.com/downloads/C9500/GLM_data.zip'
    GLM_archive = urllib.request.urlopen(url).read()

    # make the archive available as a byte-stream
    zipdata = io.BytesIO()
    zipdata.write(GLM_archive)

    # extract the requested file from the archive, as a pandas XLS-file
    myzipfile = zipfile.ZipFile(zipdata)
    xlsfile = myzipfile.open(inFile)

    # read the xls-file into Python, using Pandas, and return the extracted data
    xls = pd.ExcelFile(xlsfile)
    df  = xls.parse('Sheet1', skiprows=2)

    return df


def regression():
    '''Poisson regression example
    chapter 4.4, p.69'''
    
    # get the data from the web
    inFile = r'GLM_data/Table 4.3 Poisson regression.xls'
    df = get_data(inFile)
    
    # do the fit
    p = smf.glm('y~x', family=sm_families.Poisson(sm_families.links.identity), data=df)
    print(p.fit().summary())

def multiple_linear_regression():
    '''Multiple linear regression
    chapter 6.3, p. 98'''
    
    # get the data from the web
    inFile = r'GLM_data/Table 6.3 Carbohydrate diet.xls'
    df = get_data(inFile)
    
    # do the fit, for the original model ...
    model = smf.ols('carbohydrate ~ age + weight + protein', data=df).fit()
    print(model.summary())
    print(sm_stats.anova_lm(model))

    # as GLM
    glm = smf.glm('carbohydrate ~ age + weight + protein',
            family=sm_families.Gaussian(), data=df).fit()
    print('Same model, calculated with GLM')
    ''' The confidence intervals are different than those from OLS.
    The reason (from Nathaniel Smith):
    OLS uses a method that gives exact results, but only works in the special
    case where all the usual OLS criteria apply - iid Gaussian noise etc. GLM
    instead uses an approximate method which is correct asymptotically but may
    be off for small samples; the tradeoff you get in return is that this method
    works the same way for all GLM models, including those with non-Gaussian
    error terms and non-trivial link functions. So that's why they're different.
    '''

    print(glm.summary())
    
    # ... and for model 1
    model1 = smf.ols('carbohydrate ~ weight + protein', data=df).fit()
    print(model1.summary())
    print(sm_stats.anova_lm(model1))

def anova():
    '''ANOVA
    chapter 6.4, p. 108, and p. 113
    GLM does not work with anova_lm.
    '''
    
    # get the data from the web
    inFile = r'GLM_data/Table 6.6 Plant experiment.xls'
    df = get_data(inFile)
    
    # fit the model (p 109)
    glm = smf.glm('weight~group', family=sm_families.Gaussian(), data=df)
    print(glm.fit().summary())
    
    print('-'*65)
    print('OLS')
    model = smf.ols('weight~group', data=df)
    print(model.fit().summary())
    print(sm_stats.anova_lm(model.fit()))
    
    # The model corresponding to the null hypothesis of no treatment effect is
    model0 = smf.ols('weight~1', data=df)
    
    # Get the data for the two-factor ANOVA (p 113)
    inFile = r'GLM_data/Table 6.9 Two-factor data.xls' 
    df = get_data(inFile)
    
    # adjust the header names from the Excel-file
    df.columns = ['A','B', 'data']
    
    # two-factor anova, with interactions
    ols_int = smf.ols('data~A*B', data=df)
    sm_stats.anova_lm(ols_int.fit())
    
    # The python commands for the other four models are
    ols_add = smf.ols('data~A+B', data=df)
    ols_A = smf.ols('data~A', data=df)    
    ols_B = smf.ols('data~B', data=df)    
    ols_mean = smf.ols('data~1', data=df)    

def ancova():
    ''' ANCOVA
    chapter 6.5, p 117 '''
    
    # get the data from the web
    inFile = r'GLM_data/Table 6.12 Achievement scores.xls'
    df = get_data(inFile)
    
    # fit the model
    model = smf.ols('y~x+method', data=df).fit()
    print(sm_stats.anova_lm(model))
    print(model.summary())

def logistic_regression():
    '''Logistic regression example
    chapter 7.3, p 130
    [tbd]: the cloglog values are inconsistent with those mentioned in the book.
    This is probably due to the specific definitions of "loglog" and "cloglog"
    in the respective languages.
    '''
    
    inFile = r'GLM_data/Table 7.2 Beetle mortality.xls'
    df = get_data(inFile)
    
    # adjust the unusual column names in the Excel file
    colNames = [name.split(',')[1].lstrip() for name in df.columns.values]
    df.columns = colNames
    
    # fit the model
    df['tested'] = df['n']
    df['killed'] = df['y']
    df['survived'] = df['tested'] - df['killed']

    model = smf.glm('survived + killed ~ x', data=df, family=sm_families.Binomial()).fit()
    print(model.summary())
    
    print('-'*65)
    print('Equivalent solution:')
    
    model = smf.glm('I(n - y) + y ~ x', data=df, family=sm_families.Binomial()).fit()
    print(model.summary())
    
    # The fitted number of survivors can be obtained by
    fits = df['n']*(1-model.fittedvalues)
    print('Fits Logit:')
    print(fits)
    
    # The fits for other link functions are:
    model_probit = smf.glm('I(n - y) + y ~ x', data=df, family=sm_families.Binomial(sm_families.links.probit)).fit()
    print(model_probit.summary())
    
    fits_probit = df['n']*(1-model_probit.fittedvalues)
    print('Fits Probit:')
    print(fits_probit)
    
    model_cll = smf.glm('I(n - y) + y ~ x', data=df, family=sm_families.Binomial(sm_families.links.cloglog)).fit()
    print(model_cll.summary())
    fits_cll = df['n']*(1-model_cll.fittedvalues)
    print('Fits Extreme Value:')
    print(fits_cll)
    
    x = np.arange(1.65,1.91,0.01)

    y = np.exp(model.params[0]+model.params[1]*x)/(1+np.exp(model.params[0]+model.params[1]*x))
    yUp = np.exp(model.params[0]+model.bse[0]+(model.params[1]+2*model.bse[1])*x)/(1+np.exp(model.params[0]+2*model.bse[0]+(model.params[1]+2*model.bse[1])*x))
    yLo = np.exp(model.params[0]-model.bse[0]+(model.params[1]-2*model.bse[1])*x)/(1+np.exp(model.params[0]-2*model.bse[0]+(model.params[1]-2*model.bse[1])*x))
    plt.plot(df['x'],df['killed']/df['tested'],'.')
    plt.plot(x,1-y,linewidth=0.5,color='black',label='Logit Fit')
    plt.plot(x,1-yUp,'--',linewidth=0.5,color='red',label='2 Sigma Bounds')
    plt.plot(x,1-yLo,'--',linewidth=0.5,color='red')
    plt.title('Logit Fit')
    plt.xlabel('Radiation Dose')
    plt.ylabel('Probability of death from Leukemia')
    plt.legend()

    plt.figure()
    y = norm.cdf(model_probit.params[0]+model_probit.params[1]*x)
    yUp = norm.cdf(model_probit.params[0]+model_probit.bse[0]+(model_probit.params[1]+2*model_probit.bse[1])*x)
    yLo = norm.cdf(model_probit.params[0]-model_probit.bse[0]+(model_probit.params[1]-2*model_probit.bse[1])*x)
    plt.plot(df['x'],df['killed']/df['tested'],'.')
    plt.plot(x,1-y,linewidth=0.5,color='black',label='Probit Fit')
    plt.plot(x,1-yUp,'--',linewidth=0.5,color='red',label='2 Sigma Bounds')
    plt.plot(x,1-yLo,'--',linewidth=0.5,color='red')
    plt.title('Probit Fit')
    plt.xlabel('Radiation Dose')
    plt.ylabel('Probability of death from Leukemia')
    plt.legend()

    plt.figure()
    y = 1-np.exp(-(np.exp(model_cll.params[0]+model_cll.params[1]*x)))
    yUp = 1-np.exp(-(np.exp(model_cll.params[0]+model_cll.bse[0]+(model_cll.params[1]+2*model_cll.bse[1])*x)))
    yLo = 1-np.exp(-(np.exp(model_cll.params[0]-model_cll.bse[0]+(model_cll.params[1]-2*model_cll.bse[1])*x)))
    plt.plot(df['x'],df['killed']/df['tested'],'.')
    plt.plot(x,1-y,linewidth=0.5,color='black',label='CLL Fit')
    plt.plot(x,1-yUp,'--',linewidth=0.5,color='red',label='2 Sigma Bounds')
    plt.plot(x,1-yLo,'--',linewidth=0.5,color='red')
    plt.title('CLL Fit')
    plt.xlabel('Radiation Dose')
    plt.ylabel('Probability of death from Leukemia')
    plt.legend()
    pdb.set_trace()

def exercise7d1():
    '''Logistic regression example
    chapter 7.3, p 130
    [tbd]: the cloglog values are inconsistent with those mentioned in the book.
    This is probably due to the specific definitions of "loglog" and "cloglog"
    in the respective languages.
    '''
    
    inFile = r'GLM_data/Table 7.11 Hiroshima deaths.xls'
    df = get_data(inFile)

    df['radBin'] = np.array([0,1,10,50,100,200])

    # adjust the unusual column names in the Excel file
    colNames = df.columns.values
    colNames[2] = 'other'
    colNames[3] = 'total'
    df.columns = colNames
    df['n'] = df['total']
    df['y'] = df['leukemia']

    model = smf.glm('other + leukemia ~ radBin', data=df, family=sm_families.Binomial()).fit()
    print(model.summary())

    print('-'*65)
    print('Equivalent solution:')
    
    model = smf.glm('I(n - y) + y ~ radBin', data=df, family=sm_families.Binomial()).fit()
    print(model.summary())
    
    # The fitted number of survivors can be obtained by
    fits = df['n']*(1-model.fittedvalues)
    print('Fits Logit:')
    print(fits)
    
    # The fits for other link functions are:
    model_probit = smf.glm('I(n - y) + y ~ radBin', data=df, family=sm_families.Binomial(sm_families.links.probit)).fit()
    print(model_probit.summary())
    
    fits_probit = df['n']*(1-model_probit.fittedvalues)
    print('Fits Probit:')
    print(fits_probit)
    
    model_cll = smf.glm('I(n - y) + y ~ radBin', data=df, family=sm_families.Binomial(sm_families.links.cloglog)).fit()
    print(model_cll.summary())
    fits_cll = df['n']*(1-model_cll.fittedvalues)
    print('Fits Extreme Value:')
    print(fits_cll)

    x = np.arange(201)
    y = np.exp(model.params[0]+model.params[1]*x)/(1+np.exp(model.params[0]+model.params[1]*x))
    yUp = np.exp(model.params[0]+2*model.bse[0]+(model.params[1]+2*model.bse[1])*x)/(1+np.exp(model.params[0]+2*model.bse[0]+(model.params[1]+2*model.bse[1])*x))
    yLo = np.exp(model.params[0]-2*model.bse[0]+(model.params[1]-2*model.bse[1])*x)/(1+np.exp(model.params[0]-2*model.bse[0]+(model.params[1]-2*model.bse[1])*x))

    plt.plot(df['radBin'],df['leukemia']/df['total'],'.')
    plt.plot(x,1-y,linewidth=0.5,color='black',label='Logit Fit')
    plt.plot(x,1-yUp,'--',linewidth=0.5,color='red',label='2 Sigma Bounds')
    plt.plot(x,1-yLo,'--',linewidth=0.5,color='red')
    plt.title('Logit Fit')
    plt.xlabel('Radiation Dose')
    plt.ylabel('Probability of death from Leukemia')
    plt.legend()

    plt.figure()
    y = norm.cdf(model_probit.params[0]+model_probit.params[1]*x)
    yUp = norm.cdf(model_probit.params[0]+2*model_probit.bse[0]+(model_probit.params[1]+2*model_probit.bse[1])*x)
    yLo = norm.cdf(model_probit.params[0]-2*model_probit.bse[0]+(model_probit.params[1]-2*model_probit.bse[1])*x)
    plt.plot(df['radBin'],df['leukemia']/df['total'],'.')
    plt.plot(x,1-y,linewidth=0.5,color='black',label='Probit Fit')
    plt.plot(x,1-yUp,'--',linewidth=0.5,color='red',label='2 Sigma Bounds')
    plt.plot(x,1-yLo,'--',linewidth=0.5,color='red')
    plt.title('Probit Fit')
    plt.xlabel('Radiation Dose')
    plt.ylabel('Probability of death from Leukemia')
    plt.legend()

    plt.figure()
    y = 1-np.exp(-(np.exp(model_cll.params[0]+model_cll.params[1]*x)))
    yUp = 1-np.exp(-(np.exp(model_cll.params[0]+2*model_cll.bse[0]+(model_cll.params[1]+2*model_cll.bse[1])*x)))
    yLo = 1-np.exp(-(np.exp(model_cll.params[0]-2*model_cll.bse[0]+(model_cll.params[1]-2*model_cll.bse[1])*x)))
    plt.plot(df['radBin'],df['leukemia']/df['total'],'.')
    plt.plot(x,1-y,linewidth=0.5,color='black',label='CLL Fit')
    plt.plot(x,1-yUp,'--',linewidth=0.5,color='red',label='2 Sigma Bounds')
    plt.plot(x,1-yLo,'--',linewidth=0.5,color='red')
    plt.title('CLL Fit')
    plt.xlabel('Radiation Dose')
    plt.ylabel('Probability of death from Leukemia')
    plt.legend()
    pdb.set_trace()
def general_logistic_regression():
    '''Example General Logistic Recression,
    Example 7.4.1, p. 135'''
    
    # Get the data
    inFile = r'GLM_data/Table 7.5 Embryogenic anthers.xls'
    df = get_data(inFile)
    
    # Define the variables so that they match Dobson
    df['n_y'] = df['n'] - df['y']
    df['newstor'] = df['storage']-1
    df['x'] = np.log(df['centrifuge'])
    
    # Model 1
    model1 = smf.glm('n_y + y ~ newstor*x', data=df, family=sm_families.Binomial()).fit()
    print(model1.summary())
    
    # Model 2
    model2 = smf.glm('n_y + y ~ newstor+x', data=df, family=sm_families.Binomial()).fit()
    print(model2.summary())
    
    # Model 3
    model3 = smf.glm('n_y + y ~ x', data=df, family=sm_families.Binomial()).fit()
    print(model3 .summary())

def senility_and_WAIS():
    '''Another example of logistic regression.
    chapter 7.8, p 143
    [tbd]: I don't understand how the "Binomial model" (grouped response)
    is supposed to work, in either language'''

    inFile = r'GLM_data/Table 7.8 Senility and WAIS.xls'
    df = get_data(inFile)
    
    # ungrouped
    model = smf.glm('s ~ x', data=df, family=sm_families.Binomial()).fit()
    print(model.summary())
    
    # Hosmer-Lemeshow
    # grouped: Here I don't get how the grouping is supposed to be achieved, either in R or in Python
    # [tbd]

def nominal_logistic_regression():
    '''Nominal Logistic Regression
    chapter 8.3,  p. 155 
    
    At this point, nominal logistic regression cannot be done with the formula approach.
    
    Regarding the output, note that R produces log(pi2/pi1) and log(pi3/pi1), while
    statsmodels produces log(pi2/pi1) and log(pi3/pi2) 
    '''
    
    # Get the data
    inFile = r'GLM_data/Table 8.1 Car preferences.xls'
    df = get_data(inFile)

    # to make sure that "women" and "no/little" are the reference,
    # adjust them such that they come first alphabetically
    df['response'][df['response'] == 'no/little'] = '_no/little'
    df['sex'][df['sex'] == 'women'] = '_women'
    print(df)
    
    
    # Generate the design matrices using patsy
    pm = patsy.dmatrices('response~sex+age', data=df)
    
    # Generate the endog and exog matrices
    endog = np.repeat(np.array(df['response']), df['frequency'].values.astype(int), axis=0)
    exog = np.array(np.repeat(pm[1], df['frequency'].values.astype(int), axis=0))
    exog = pd.DataFrame(exog, columns=pm[1].design_info.column_names) 

    # Fit the model, and print the summary
    model = sm.MNLogit(endog, exog, method='nm').fit()
    print( model.summary())

def ordinal_logistic_regression_tbd():
    
    '''Ordinal Logistic Regression
    chapter  8.4, p161
    This function is not implemented in statsmodels yet. One solution can be found at
    http://fabianp.net/blog/2013/logistic-ordinal-regression/
    '''
    
    inFile = r'GLM_data/Table 8.1 Car preferences.xls'
    df = get_data(inFile)

def poisson_regression():
    '''Poisson Regression
    chapter 9.2, p.170 & 171 '''
    
    inFile = r"GLM_data/Table 9.1 British doctors' smoking and coronary death.xls"
    df = get_data(inFile)

    # Generate the required variables
    df['smoke'] = np.zeros(len(df))
    df['smoke'][df['smoking']=='smoker']=1

    df['agecat'] = np.array([1,2,3,4,5,1,2,3,4,5])
    df['agesq'] = df['agecat']**2

    df['smkage'] = df['agecat']
    df['smkage'][df['smoking']=='non-smoker']=0
    
    model = smf.glm('deaths~agecat+agesq+smoke+smkage',
            family=sm_families.Poisson(), data=df,
            exposure=df["person-years"]).fit()
    print(model.summary())
    plt.plot(df['agecat'],df['deaths']/df['person-years'],'.')
    
    pdb.set_trace()
def exercise9d2():
    '''Poisson Regression
    chapter 9.2, p.170 & 171 '''
    
    inFile = r"GLM_data/Table 9.13 Car insurance.xls"
    df = get_data(inFile)
    print(df)
    df['carage'] = df['car']*df['age']
    df['cardist'] = df['car']*(df['district'])
    df['agedist'] = df['age']*df['district']

    model = smf.glm('y~car+age+district+carage+cardist+agedist',
            family=sm_families.Poisson(), data=df,
            exposure=df['n']).fit()

    print(model.summary())
    pdb.set_trace()


def log_linear_models():
    '''Log-linear models
    chapter 9.7, p 180 & 182 '''

    # Malignant melanoma, p 180 --------------------------------
    inFile = r'GLM_data/Table 9.4 Malignant melanoma.xls'
    df = get_data(inFile)

    # Minimal model
    model_min = smf.glm('frequency~1', family = sm_families.Poisson(), data=df).fit()
    print('Malignant melanoma')
    print(model_min.fittedvalues[0])

    # Additive model
    model_add = smf.glm('frequency~site+type', family = sm_families.Poisson(), data=df).fit()
    print(model_add.fittedvalues[0])

    # Saturated model
    # model_sat = smf.glm('frequency~site*type', family = sm_families.Poisson(), data=df).fit()
    #
    # The saturated model gives a perfect fit, and the fitted data are equal to
    # the original data. Statsmodels indicates a "PerfectSeparationError"

    # Ulcer and aspirin, p. 182 ------------------------------------- 
    inFile = r'GLM_data/Table 9.7 Ulcer and aspirin use.xls'
    df = get_data(inFile)
    df.columns = ['GD', 'CC', 'AP', 'freq']

    model1 = smf.glm('freq~GD+CC+GD*CC', family = sm_families.Poisson(), data=df).fit()
    model2 = smf.glm('freq~GD+CC+GD*CC + AP', family = sm_families.Poisson(), data=df).fit()
    model3 = smf.glm('freq~GD+CC+GD*CC + AP + AP*CC', family = sm_families.Poisson(), data=df).fit()
    model4 = smf.glm('freq~GD+CC+GD*CC + AP + AP*CC + AP*GD', family = sm_families.Poisson(), data=df).fit()
    
    print('Ulcer and aspirin')
    print(model4.fittedvalues)


def remission_times_tbd():
    '''Survival analysis / Remission times
    chapter 10.7, p. 201
    These models, also known as "Cox proportional hazards model",
    are currently under development but not yet available in statsmodels.'''

    inFile = r'GLM_data/Table 10.1 Remission times.xls'
    df = get_data(inFile)
    print(df)

def longitudinal_data_tbd():
    '''Stroke example
    chapter 11.6, p. 222
    Clustered and Longitudinal Data are described by repeated measures models.
    These are under development, but not yet available in statsmodels.'''

    inFile = r'GLM_data/Table 11.1 Recovery from stroke.xls'
    df = get_data(inFile)
    print(df)

if __name__ == '__main__':
    runAll = 0
    if 0 or runAll: logistic_regression()
    if 0 or runAll: exercise7d1()
    if 1 or runAll: poisson_regression()
    if 0 or runAll: exercise9d2()

    # Now run all models, just to check that they don't crash
    # ancova()
    # anova()
    # general_logistic_regression()
    # logistic_regression()
    # log_linear_models()
    # multiple_linear_regression()
    # nominal_logistic_regression()
    # regression()
    # senility_and_WAIS()

