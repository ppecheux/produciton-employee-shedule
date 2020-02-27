from numpy import mean, array_split, random
from math import log2
from statistics import mean

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

numberchoice=[10,15,20]
i=0
arr=[]
while i<20 :
    arr.append(random.choice(numberchoice))
    i+=1
arr_verif = arr.copy()
n = len(arr)
medianne=mean(arr)

#Par doublettes
j=0
retard=0
while j<20:
    retard+=(medianne-(arr[j]+arr[j+1])/2)
    print(arr[j],":", arr[j+1], "Accumulated time lost or gained compared to the average value :",retard)
    j+=2
print()
#Par triplettes
j=0
retard=0
while j<17:
    retard+=(medianne-(arr[j]+arr[j+1]+arr[j+2])/3)
    print(arr[j],":", arr[j+1],":",arr[j+2], "Accumulated time l/g compared to the avg value :",retard)
    j+=3
retard+=(medianne-(arr[j]+arr[j+1])/2)
print(arr[j],":", arr[j+1], "Accumulated time l/g compared to the avg value :",retard)
print()
#Par quadrupellettes
j=0
retard=0
while j<20:
    retard+=(medianne-(arr[j]+arr[j+1]+arr[j+2]+arr[j+3])/4)
    print(arr[j],":", arr[j+1],":",arr[j+2],":",arr[j+3], "Accumulated time l/g compared to the avg value :",retard)
    j+=4
print()
#Par quintuplettes
j=0
retard=0
while j<20:
    retard+=(medianne-(arr[j]+arr[j+1]+arr[j+2]+arr[j+3]+arr[j+4])/5)
    print(arr[j],":", arr[j+1],":",arr[j+2],":",arr[j+3],":",arr[j+4],"Accumulated time l/g compared to the avg value :",retard)
    j+=5
print()
print ("Given array is")
print(arr)



print ("\n\nSorted array is")
print(merge_mix(arr))
