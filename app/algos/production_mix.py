
from numpy import mean, array_split, random, cumsum
import numpy as np
from math import log2
from matplotlib import pyplot as plt

def mix_distribute_uniformly(arr : iter):
    """shuffles the array based on the mean of the value of the item
    
    Arguments:
        arr {iter} -- the array could be array of itegers or array of array of integer
    
    Returns:
        array -- mixed array
    """
    if len(arr) and isinstance(arr[0], list):
        arr = sorted(arr, key=mean)
    else:
        arr = sorted(arr)
    mix_arr = []
    while len(arr) >= 2:
        mix_arr.extend([arr.pop(0), arr.pop(-1)])
    if arr:
        mix_arr.extend(arr)
    return mix_arr


def merge_mix(arr: list) -> list:
    """mix the array item by item and groups by groups to give a uniform distribution
    
    Arguments:
        arr {list} -- [description]
    
    Returns:
        list -- mixed_array
    """
    level = len(arr)
    while level>=4:
        arr = array_split(arr, level)
        arr = list(map(list, arr))
        arr = mix_distribute_uniformly(arr)
        arr = [item for split in arr for item in split]        
        level /= 2
    return arr

if __name__ == "__main__":

    arr = [12, 11, 13, 5, 6, 7]
    arr = random.randint(0,high=1000, size=20)
    arr_verif = arr.copy()
    n = len(arr) 
    print ("Given array is")
    print(arr)

    print ("\n\nmixed array is")
    mix_arr = merge_mix(arr)
    print(mix_arr)

    plt.plot(arr, label='random distribution of trucks')
    plt.plot(mix_arr, label='mixed distribution of trucks')
    plt.plot( [mean(arr)]*len(arr), label='mean time for a truck')
    plt.plot(cumsum(arr)/(np.arange(len(arr)) + np.ones(len(arr))), label='cumulated mean time for the random distribution')
    plt.plot(cumsum(mix_arr)/(np.arange(len(arr)) + np.ones(len(arr))), label='cumulated mean time for the mixed distribution')
    plt.legend()
    plt.xlabel("sequence of trucks")
    plt.ylabel("time to produce a truck")
    plt.show()