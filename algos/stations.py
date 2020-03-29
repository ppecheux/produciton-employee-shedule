"In this file, we want to assign stations to activity blocks"
import pandas as pd
import numpy as np
def assign_stations(activities: list, nb_stations: int) -> dict:
	#df = pd.read_json(activities, encoding='records')
	df = pd.DataFrame.from_records(activities)
	if df.empty:
		return []
	
	#begin algo
	df['station_nb'] = df.fixed_station_nb
	df.loc[df.fixed_station_nb == '', 'station_nb'] = np.nan
	#end algo
	
	df = df[['product', 'activity_block_name', 'activity_block_duration', 'station_nb']]

	activities = df.to_dict('rows')
	return activities

def weighted_average(df_in,Nb_cabs):

	nb_act = df.shape[0]   #Number of activities
	Weig_avg = []          #Creating an empty list where we will put the weighted avg for each activity
	avg = 0                #temp variables
	Nb_cabs_tot = 0
	print(df_in)

	#Make sure that the df and the Nb_cabs are made of float or int
	for i in range(len(Nb_cabs)):
		if type(Nb_cabs[i]) not in [int]:
			raise TypeError ("The number of cabs is not correct")

	for i in range(1, nb_act+1):
		act = "act"
		act += str(i)
		for j in range (1, nb_act):
			cab = "cabine"
			cab += str(j)
			if type(df_in.loc[act, cab]) not in [np.int64, np.float64]:
				raise TypeError ("There is a type error in the time of the activites")
			if df_in.loc[act, cab] < 0:
				raise TypeError("There is a time<0 in the activities")




	for i in range (len(Nb_cabs)):
	    Nb_cabs_tot += Nb_cabs[i]       #Number total of cabs
	
	for i in range(1, nb_act+1):
		act = "act"
		act += str(i)
		avg = 0
		for j in range (1, nb_act):
			cab = "cabine"
			cab += str(j)
			avg += df_in.loc[act, cab] * Nb_cabs[j-1]
		avg = avg/Nb_cabs_tot
		Weig_avg.append(avg)

	df_out = pd.DataFrame(
		Weig_avg,
		index = ["act1","act2", "act3", "act4"],
		columns = ['Weighted average']
		)

	print(df_out)
	return(df_out)

Nb_cabs = [20, 14, 8]  #Number of cabs in a list

df = pd.DataFrame({
    "cabine1":[12, 15, 25,24],
    "cabine2":[26,27,19,12],
    "cabine3":[14,28,22,16]},
    index = ["act1","act2", "act3", "act4"])

weighted_average(df, Nb_cabs)