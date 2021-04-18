# All support functions for index preprocessing

import sys
sys.path.append(r'C:\\Python files\\Power indices\\indices')
sys.path.append(r'C:\\Python files\\Power indices\\utils')

import numpy as np
from itertools import combinations
from collections import OrderedDict
import pyexcel_xlsx as py_ex
import pandas as pd
from collections import OrderedDict
import math



def combination_all(frac):

    '''Returns all possible subsets (coalitions) for the current parliament composition of parliament'''

    indeces = range(len(frac) + 1)   
    frac = list(zip(indeces, frac))
    comb = []
    for i in indeces:
        comb += combinations(frac, i)
    return comb


def all_win(frac, q):

    '''Find all winning coalitions in parliament'''

    indeces = range(len(frac) + 1)
    all_comb = combination_all(frac)
    num_of_coal = len(all_comb)
    win_coal = []
    for i in range(num_of_coal):
        summ = 0
        for j in range(len(all_comb[i])):
            summ += all_comb[i][j][1]
        if summ >= q:
            win_coal += [all_comb[i]]
    return win_coal

def key_num_ban(frac, q):

    '''Create a dict with parties as keys and number of times they were pivotal as values'''

    all_win_coal = all_win(frac, q)
    num_of_coal = len(all_win_coal)
    k = dict()
    for i in range(len(frac)):
        k[str(i)] = 0
    for i in range(num_of_coal):
        summ = 0
        for j in range(len(all_win_coal[i])):
            summ += all_win_coal[i][j][1]
        for j in range(len(all_win_coal[i])):
            if summ - all_win_coal[i][j][1] < q:
                k[str(all_win_coal[i][j][0])] += 1   
    return k


def min_win_dig(frac, q):

    '''Minimal winning coalitions for Deegan-Packel index'''

    all_win_coal = all_win(frac, q)
    min_win_coal = []
    for coalition in all_win_coal:
        summ_votes = 0
        for party in coalition:
            summ_votes += party[1]
        indicator = 0
        for party in coalition:
            if summ_votes - party[1] >= q:
                indicator = 1
        if indicator == 0:
            min_win_coal += [coalition]
    return min_win_coal

def min_win_holl(frac, q):

    '''Minimal winning coalitions for Holler-Packel index'''

    all_win_coal = all_win(frac, q)
    min_win_coal = []
    for coalition in all_win_coal:
        summ_votes = 0
        for party in coalition:
            summ_votes += party[1]
        indicator = 0
        for party in coalition:
            if summ_votes - party[1] >= q:
                indicator = 1
        if indicator == 0:
            min_win_coal += [coalition]
    return min_win_coal

def key_num_holl(frac, q):

    '''Create a dict with parties as keys and number of times 
       they were pivotal in minimal winning coalitions as values'''

    all_win_coal = min_win_holl(frac, q)
    num_of_coal = len(all_win_coal)
    k = dict()
    for i in range(len(frac)):
        k[str(i)] = 0
    for i in range(num_of_coal):
        summ = 0
        for j in range(len(all_win_coal[i])):
            summ += all_win_coal[i][j][1]
        for j in range(len(all_win_coal[i])):
            if summ - all_win_coal[i][j][1] < q:
                k[str(all_win_coal[i][j][0])] += 1   
    return k

def win_only_parties(frac, q):

    '''Find pivotal parties in winning coalitons (for Johnston index)'''

    all_win_coal = all_win(frac, q)
    john_coal = []
    for coalition in all_win_coal:
        new_coal = []
        summ_coal = 0
        for party in coalition:
            summ_coal += party[1]
        for i in range(len(coalition)):
            if summ_coal - coalition[i][1] < q:
                new_coal += [coalition[i]]
        new_coal = tuple(new_coal)
        john_coal += [new_coal]
    return john_coal

def massive_constructor(frac, q):

    '''The massive to carry additional information for Shapley-Shubik index'''

    all_win_coal = all_win(frac, q)
    massive = []
    a = -float('inf')
    b = float('inf')
    for coalition in all_win_coal:
        length = len(coalition)
        if a < length:
            a = length
        if b > length:
            b = length
    c = range(b, a + 1)
    for i in c: 
        massive += [np.zeros(len(frac) + 1)]
    for i in range(len(massive)):
        massive[i][0] = c[i]
    return massive

def key_party(frac, q):

    '''Compute key parties for Shapley-Shubik index'''

    massive = massive_constructor(frac, q)
    all_win_coal = all_win(frac, q) 
    for size in massive:
        for coalition in all_win_coal:
            if len(coalition) == size[0]:
                summ_votes = 0
                for party in coalition:
                    summ_votes += party[1]
                for party in coalition:
                    if summ_votes - party[1] < q:
                        a = party
                        for party in coalition:
                            if party == a:
                                size[party[0] + 1] += 1
    return massive

def combination_all_colem(frac):

    '''Find all coalitions for Coleman indices'''

    indeces = range(len(frac) + 1)   
    frac = list(zip(indeces, frac))
    comb = []
    for i in indeces:
        comb += combinations(frac, i)
    return comb

def all_win_colem(frac, q):

    '''Find all winning coalitions for Coleman indices'''

    indeces = range(len(frac) + 1)
    all_comb = combination_all_colem(frac)
    num_of_coal = len(all_comb)
    win_coal = []
    for i in range(num_of_coal):
        summ = 0
        for j in range(len(all_comb[i])):
            summ += all_comb[i][j][1]
        if summ >= q:
            win_coal += [all_comb[i]]
    return win_coal

def key_num_colem(frac, q):

    '''Compute for each party the number of times it was pivotal for Coleman indices'''

    all_win_coal = all_win_colem(frac, q)
    num_of_coal = len(all_win_coal)
    k = dict()
    for i in range(len(frac)):
        k[str(i)] = 0
    for i in range(num_of_coal):
        summ = 0
        for j in range(len(all_win_coal[i])):
            summ += all_win_coal[i][j][1]
        for j in range(len(all_win_coal[i])):
            if summ - all_win_coal[i][j][1] < q:
                k[str(all_win_coal[i][j][0])] += 1   
    return k

def Num_key_index_names(frac_dict, threshold):

    '''Find all significant (at some threshold) parties in the given dictionary'''

    list_sign = []
    for party in frac_dict.keys():
        if frac_dict[party] >= threshold:
            list_sign += [party]
    return list_sign
