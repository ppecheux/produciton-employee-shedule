"In this file, we want to assign stations to activity blocks"
import pandas as pd
import numpy as np
def assign_stations(activities: list, nb_stations: int) -> dict:
	return activities

def weighted_average(df,Nb_cabs):


	tab = df.to_numpy()    #Dataframe to numpy to be able to calculate the weighted average
	nb_act = tab.shape[0]   #Number of activities
	Weig_avg = []          #Creating an empty list where we will put the weighted avg for each activity
	avg = 0                #temp variables
	Nb_cabs_tot = 0


	for i in range (len(Nb_cabs)-1):
	    Nb_cabs_tot += Nb_cabs[i]       #Number total of cabs

	for i in range (nb_act):          #Determination of the weighted avg of each activity
	    for j in range (2):
	        avg += tab[i][j] * Nb_cabs[j]
	    avg = avg/Nb_cabs_tot
	    Weig_avg.append(avg)

	df_out = pd.DataFrame(
		Weig_avg,
		index = ["act1","act2", "act3", "act4"],
		columns = ['Weighted average']
		)

	print(df_out)

Nb_cabs = [20, 14, 8]  #Number of cabs in a list

df = pd.DataFrame({
    "cabineA":[12, 15, 25,24],
    "cabineB":[26,27,19,12],
    "cabineC":[14,28,22,16]},
    index = ["act1","act2", "act3", "act4"])

weighted_average(df, Nb_cabs)