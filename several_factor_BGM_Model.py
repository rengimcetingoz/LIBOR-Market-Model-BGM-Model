#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 16:30:33 2019

@author: rengimcetingoz
"""
import numpy as np
import math as sqrt
import random as std

##this code can be used to estimate forward rates using LIBOR Market Model also known as BGM model


##input parameters are time step (t_(k+1)-t_(k)), maturity, zero curve vector, forward rate volatility factors matrix and number of simulations
##note that dimension of forward rate volatility factors matrix depends on the components of volatility

##for example, if I want to model forward rates for the next 10 years with three-factor model
##Assuming time step is chosen to be anually, I extract zero curve and forward rate volatility data for the next 10 years annually
##Then, input parameters will be time_step=1, maturity=10, zero curve vector of 11 elements (maturities 1 year to 11 years, we use year 11 in calculation of initial forward rates)
##and forward rate volatility matrix of dimension 3x10

##zero_curve=np.array([0.0074,0.0074,0.0077,0.0082,0.0088,0.0094,0.0101,0.0108,0.0116,0.0123,0.0131])
##forward_rate_volatilities_three_factor=np.array([[0.1365,0.1928,0.1672,0.1698,0.1485,0.1395,0.1261,0.1290,0.1197,0.1097],
##[-0.0662,-0.0702 ,-0.0406,-0.0206,0, 0.0169, 0.0306,0.0470, 0.0581, 0.0666],[ 0.0319 , 0.0225, 0, -0.0198, -0.0347, -0.0163, 0,
##0.0151, 0.0280, 0.0384]])

def LIBOR_Market_Model(time_step,maturity,zero_curve,forward_rate_volatilities,N):
    steps=int(maturity/time_step)+1
    t=np.zeros(steps)
    time=0
    p=forward_rate_volatilities.shape[0]
    for i in range(steps):
        t[i]=time
        time+=time_step
    Delta=np.full((steps-1),time_step)  
    B_0=np.zeros(steps)
    for i in range(steps):
        B_0[i]=1/(1+zero_curve[i])**(i+1)
    forward_rate_from_zero=np.zeros((steps-1,steps-1))
    for i in range(steps-1):
        forward_rate_from_zero[i][0]=1/Delta[i]*(B_0[i]/B_0[i+1]-1)
    forward_rate_mc=0
    for n in range(N):
        forward_rate=np.zeros((steps-1,steps-1))
        for i in range(steps-1):
            forward_rate[i][0]=forward_rate_from_zero[i][0]
        for k in range(1,steps-1):
            for j in range(k):
                sum1=0
                for i in range(j+1,k+1):
                    sum2=0
                    sum3=0
                    sum4=0
                    for q in range(p):
                        e=np.random.standard_normal()
                        sum2+=(forward_rate_volatilities[q][i-j-1]*forward_rate_volatilities[q][k-j-1])
                        sum3+=forward_rate_volatilities[q][k-j-1]**2
                        sum4+=forward_rate_volatilities[q][k-j-1]*e*np.sqrt(Delta[j])
                    sum1+=(Delta[i]*forward_rate[i][j]*sum2)/(1+Delta[i]*forward_rate[i][j])
                forward_rate[k][j+1]=forward_rate[k][j]*np.exp((sum1-sum3/2)*Delta[j]+sum4)
        forward_rate_mc+=forward_rate
    forward_rate_mc=forward_rate_mc/N
    return forward_rate_mc       

##In this Monte Carlo simulation, forward rates at t_1 from those at time 0 are calculated, then
##forward rates at t_2 from those at t_1 are calculated and so on
##It is repeated many times, thus expected value of forward rates can be obtained


##what we obtain as output is a forward rate matrix composed of forward rates at time zero between
##t_1 and t_2, ...., t_k and t_k+1, at t_1 between t_2 and t_3,.....,t_k and t_k+1, at t_2 between 
##t_3 and t_4,.....,t_k and t_k+1,....., at t_k-1 between t_k and t_k+1
##we simply obtain zero curves from t_1 to t_k, from t_2 to t_k,..., and from t_k-1 to t_k
