"In this file, we want to assign stations to activity blocks"
import pandas as pd
import numpy as np
def assign_stations(activities: list, products: list, nb_stations: int) -> dict:
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

def weighted_average(df_in, Nb_cabs):

	nb_act = df_in.shape[0]   #Number of activities
	Weig_avg = []          #Creating an empty list where we will put the weighted avg for each activity
	avg = 0                #temp variables
	Nb_cabs_tot = 0
	print(df_in)

	#Make sure that the df and the Nb_cabs are made of float or int or <0
	for i in range(len(Nb_cabs)):
		if type(Nb_cabs[i]) not in [int]:
			raise TypeError ("The number of cabs is not correct")
		if Nb_cabs[i] < 0:
			raise TypeError ("The number of cabs is <0")

	for i in range(1, nb_act+1):
		act = "act"
		act += str(i)
		for j in range (1, len(Nb_cabs)+1):
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
		for j in range (1, len(Nb_cabs)+1):
			cab = "cabine"
			cab += str(j)
			avg += df_in.loc[act, cab] * Nb_cabs[j-1]
		avg = avg/Nb_cabs_tot
		Weig_avg.append(avg)

	df_out = pd.DataFrame(
		Weig_avg,
		index = df_in.index,
		columns = ['Weighted average']
		)

	print(df_out)
	return(df_out)

def arrange_stations(df_in, takt_time: int, nb_stations: int):
	nb_act = df_in.shape[0]
	Station_list = []
	sum_time = 0
	time = []
	stat = 1
	for i in range (1, nb_act+1):
		act = "act"
		act += str(i)
		sum_time += df_in.loc[act, "Weighted average"]
		if sum_time <= takt_time:
			Station_list.append(stat)
			time.append(sum_time)
		else :
			stat += 1
			Station_list.append(stat)
			sum_time = df_in.loc[act, "Weighted average"]
			time.append(sum_time)

	df_out = pd.DataFrame({
		'Station' : Station_list,
		'Time total' : time},
		index = df_in.index)
	print(df_out)
	return(df_out)


Nb_cabs = [20, 14, 8]  #Number of cabs in a list

df = pd.DataFrame({
    "cabine1":[12,15,25,24,16],
    "cabine2":[26,27,19,12,18],
    "cabine3":[14,28,22,16,23],},
    index = ["act1","act2", "act3", "act4", "act5"])

df_out = weighted_average(df, Nb_cabs)
arrange_stations(df_out, 40, 28)