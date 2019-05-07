#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 16:25:44 2019

@author: rengimcetingoz
"""
import numpy as np
import math as sqrt
import random as std

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