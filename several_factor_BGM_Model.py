#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 16:30:33 2019

@author: rengimcetingoz
"""

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