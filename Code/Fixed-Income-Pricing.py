"""
Fixed Income Pricing
W.Carpenter
"""
import sys
import os
import math 
import pandas as pd
import numpy as np
import time
import datetime 
import calendar 
from pandas.tseries.offsets import DateOffset
from scipy.optimize import fsolve
from scipy.optimize import newton
from scipy import optimize
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#%%
# Reading in interest rate tree data for testing 

one_period_tree = np.array([[0.0168, 0.0433, np.nan], 
                            [np.nan, 0.0120, np.nan], 
                            [np.nan, np.nan, np.nan]]) 

two_period_tree = np.array([[0.0168, 0.0433, 0.0638, np.nan], 
                            [np.nan, 0.0120, 0.0361, np.nan], 
                            [np.nan, np.nan, 0.0083, np.nan], 
                            [np.nan, np.nan, np.nan, np.nan]])

rateTree = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Fixed-Income-Valuation/main/Data/testTree.csv", header=0).values

len(rateTree)
display(rateTree)

# capVols  = np.genfromtxt(path + "libor_1m_atm_cap_vol.csv", dtype=float, delimiter=',', names=True) 

#%%

# Asset Payoff Functions 
call    = lambda x: max(x-100, 0)
put     = lambda x: max(100-x, 0)
forward = lambda x: x - 100
cap     = lambda x: 0 
floor   = lambda x: 0
swap    = lambda x: 0
collar  = lambda x: 0
bond    = lambda x: x

# Asset Cash Flow Functions

# Every agrument takes in a row,col,rate, notional argument but doesn't necessarily use it lol
cap_cf   = lambda (rate, strike, delta, notion, cpn): exp(-1*rate*delta)*delta*notion*max(rate-strike,0)
floor_cf = lambda (rate, strike, delta, notion, cpn): exp(-1*rate*delta)*delta*notion*max(strike-rate,0)
swap_cf  = lambda (rate, strike, delta, notion, cpn): exp(-1*rate)delta)*delta*notion(rate - strike)
bond_cf  = lambda (rate, strike, delta, notion, cpn): notional*delta*coupon
zcb_ cf  = lambda (rate, strike, delta, notion, cpn): 0 

# cap, floor, collar
# swap 
 
# Print Helper function 
def display(arr):
  for i in arr:
    for j in i:
        print("{:8.4f}".format(j), end="  ")
    print() 
  print("\n")

def probTree(length):
    prob = np.zeros((length, length))
    prob[np.triu_indices(length, 0)] = 1/2
    return(prob)

def cfTree(length, rates, cf_type):
    cf = np.zeros((length, length))
    
def priceTree(rates, prob, delta, payoff, notion, coupon, strike, cashflow):
    
    '''
    General Tree Pricing Function 
    
    Returns final asset price and tree of price evolution
    
    rates    : N+1 x N+1 tree of interest rates 
    prob     : N+1 x N+1 tree of up/down probabilities
    delta    : time delta, with a value of 1 being annual 
    payoff   : payoff funtion 
    notion   : notional value of the security being priced
    coupon   : coupon of the security being priced, if relevant 
    strike   : strike rate of the security being priced if relevant
    cashflow : cashflow function
    
    '''
            
    tree = np.zeros([len(rates), len(rates)])
    
    tree[:,len(tree)-1] = payoff(notion)
        
    for col in reversed(range(0,len(tree)-1)):  
        
        for row in range(0, col+1):
            
            rate = rates[row,col]
            cf_d = cashflow(rate, )
            cf_u = cashflow(rate, strike, delta, notional, cpn)
            pu, pd = prob[row, col] # always equal to 1/2 from prob tree
            
            tree[row, col] = np.exp(-1*rate*delta)* \
                             (pu*tree[row, col+1] + pd*tree[row+1, col+1])      
    # Results / debugging                          
    display(tree)
    print(tree[0,0])  
        

#%%

# Test cases 

prob  = probTree(4)
cf    = 0 
delta = 1/2

price = priceTree(two_period_tree, prob, cf, delta, bond, 1)
print(price)

len(rateTree)

prob  = probTree(21)
cf    = 0 
delta = 1/2

price = priceTree(rateTree, prob, cf, delta, bond, 1)


_#%%

  
  
  
  