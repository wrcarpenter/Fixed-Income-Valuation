"""
Interest Rate Models 

Author : William Carpenter
Date   : Feb 19 2024

Objective: Create a binomial tree interest rate model that takes as arguments
todays forward curve and volatilities. Use the tree to price various bonds and 
other fixed income derivatives (caps, floors, swaps, etc.).

"""
import sys
import os
import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
# Every agrument takes in a row,col,rate, notional argument but doesn't necessarily use it

# Multiplying the coupon x delta is a simplified assumption for interest rate accrual 
# zero pay-delay assumption

floor_cf = lambda rate, strike, delta, notion, cpn : exp(-1*rate*delta)*delta*notion*max(strike-rate,0)
swap_cf  = lambda rate, strike, delta, notion, cpn : exp(-1*rate*delta)*delta*notion*(rate - strike)
bond_cf  = lambda rate, strike, delta, notion, cpn : notion*delta*cpn
zcb_cf   = lambda rate, strike, delta, notion, cpn : 0 




# Print helper function 
def display(arr):
  for i in arr:
    for j in i:
        print("{:8.4f}".format(j), end="  ")
    print() 
  print("\n")

# Defining tree probabilities 
def probTree(length):

    prob = np.zeros((length, length))
    prob[np.triu_indices(length, 0)] = 0.5
    return(prob)


def cfTree(rates, strike, delta, notion, cpn, cf_type):
    
    '''
    Cash Flow Tree Function
    
    Returns periodic cash flow given a certain type of asset.
    
    
    '''
    
    cf = np.zeros([len(rates), len(rates)])
    cf[np.triu_indices(len(cf),0)] = cf_type(rates, strike, delta, notion, cpn)
    
    return cf             
                  

                  
    
def priceTree(rates, prob, cf, delta, payoff, notion):
    
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
            # cf_d = cashflow(rate, )
            # cf_u = cashflow(rate, strike, delta, notional, cpn)
            pu = pd = prob[row, col] # always equal to 1/2 from prob tree
            
            tree[row, col] = np.exp(-1*rate*delta)* \
                             (pu*(tree[row, col+1]+cf[row,col+1]) + pd*(tree[row+1, col+1]+cf[row+1, col+1]))      
    # Results / debugging                          
    display(tree)
    print(tree[0,0])  
        

#%%

# Test cases

# Slide 5 
prob  = probTree(4)
pu = prob[1,1]
cf    = 0 
delta = 1/2

price = priceTree(one_period_tree, prob, delta, bond, 1)

#%%

# Slide 7
prob  = probTree(5) 
delta = 1/2

price = priceTree(two_period_tree, prob, delta, bond, 1)

#%%

# Large tree
len(rateTree)

prob  = probTree(len(rateTree))
cf = cfTree(rateTree, 0, 1/2, 100, 0.02, bond_cf)
delta = 1/2

price = priceTree(rateTree, prob, cf, delta, bond, 100) 

#%%

cf = cfTree(rateTree, 0, 1/2, 100, 0.02, bond_cf)  


  
  
  