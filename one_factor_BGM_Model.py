#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 16:25:44 2019

@author: rengimcetingoz
"""
import numpy as np
import math as sqrt
import random as std

##this code can be used to estimate forward rates using LIBOR Market Model also known as BGM model
##input parameters are time step (t_(k+1)-t_(k)), maturity, zero curve vector, forward rate volatility vector and number of simulations
##for example, if I want to model forward rates for the next 10 years with one-factor model
##Assuming time step is chosen to be anually, I extract zero curve and forward rate volatility data for the next 10 years annually
##Then, input parameters will be time_step=1, maturity=10, zero curve vector of 11 elements (maturities 1 year to 11 years, we use year 11 in calculation of initial forward rates)
##and forward rate volatility vector of 10 elements

##zero_curve=np.array([0.0074,0.0074,0.0077,0.0082,0.0088,0.0094,0.0101,0.0108,0.0116,0.0123,0.0131])
##forward_rate_volatilities=np.array([0.155, 0.20636739, 0.17209861, 0.17219933, 0.1524579 ,0.14147795, 0.12977111, 0.13810532, 0.13595499, 0.13398418])

def one_factor_LIBOR_Market_Model(time_step,maturity,zero_curve,forward_rate_volatilities,N):
    steps=int(maturity/time_step)+1
    t=np.zeros(steps)
    time=0
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
                    sum1+=(Delta[i]*forward_rate[i][j]*forward_rate_volatilities[i-j-1]*forward_rate_volatilities[k-j-1])/(1+Delta[i]*forward_rate[i][j])
                e=np.random.standard_normal()
                forward_rate[k][j+1]=forward_rate[k][j]*np.exp((sum1-forward_rate_volatilities[k-j-1]**2/2)*Delta[j]+forward_rate_volatilities[k-j-1]*e*np.sqrt(Delta[j]))
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
