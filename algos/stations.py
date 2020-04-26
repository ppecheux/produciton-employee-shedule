"In this file, we want to assign stations to activity blocks"
import pandas as pd
import numpy as np
def assign_stations(activities: list, products: list, nb_stations: int) -> dict:
	#df = pd.read_json(activities, encoding='records')
	df = pd.DataFrame.from_records(activities)
	if df.empty:
		return []
	
	df_weighted_avg = activities_weighted_avg(df, pd.DataFrame.from_records(products))

	df_weighted_avg = assign_stations_for_avg(df_weighted_avg, nb_stations)

	df = df.join(df_weighted_avg, on='activity_block_name')
	
	df = df[['product', 'activity_block_name', 'activity_block_duration', 'station_nb']]

	activities = df.to_dict('rows')
	return activities
	
def assign_stations_for_avg(df_weighted_avg: pd.DataFrame, nb_stations: int) -> pd.DataFrame:
	df_weighted_avg['station_nb'] = [np.nan] * len(df_weighted_avg)

	#compute time per station:
	rest_production_duration = df_weighted_avg['weighted_average'].sum()
	rest_nb_stations = nb_stations
	time_per_station = rest_production_duration/rest_nb_stations

	cummulated_duration = 0
	if isinstance(df_weighted_avg["weighted_average"].values[0], np.timedelta64):
		cummulated_duration = pd.Timedelta('0 days')

	station_nb = 1
	for activity in df_weighted_avg.index:

		cummulated_duration_on_middle_of_activity = cummulated_duration + df_weighted_avg.loc[activity, 'weighted_average']/2
		cummulated_duration += df_weighted_avg.loc[activity, 'weighted_average']
		while cummulated_duration_on_middle_of_activity > time_per_station:
			cummulated_duration_on_middle_of_activity = df_weighted_avg.loc[activity, 'weighted_average']/2
			cummulated_duration = df_weighted_avg.loc[activity, 'weighted_average']
			station_nb += 1
			rest_nb_stations -= 1
			time_per_station = rest_production_duration/rest_nb_stations

		df_weighted_avg.loc[activity, "station_nb"] = station_nb
		rest_production_duration -= df_weighted_avg.loc[activity, 'weighted_average']
	return df_weighted_avg	

def activities_weighted_avg(df_activities, df_products) -> pd.DataFrame:
	df_products = df_products.groupby(['product']).sum()
	total_quantity_product = df_products.quantity.sum()
	df_activities = df_activities.join(df_products['quantity'], on='product')

	df_activities['duration_times_quantity'] = df_activities['activity_block_duration'] * df_activities['quantity']
	df_activities = df_activities[['activity_block_name', 'duration_times_quantity']].groupby(['activity_block_name']).sum()
	df_activities['weighted_average'] = df_activities.duration_times_quantity/total_quantity_product

	return df_activities



def weighted_average(df_in, Nb_cabs):
	""" renvoyer une liste de temps moyenne pondéré de chaque activité """

	nb_act = df_in.shape[0]   #Number of activities
	Weig_avg = []          #Creating an empty list where we will put the weighted avg for each activity
	avg = 0                #temp variables
	Nb_cabs_tot = 0
	#print(df_in)

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

	#print(df_out)
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
	#print(df_out)
	return(df_out)

if __name__ == "__main__":
	
	Nb_cabs = [20, 14, 8]  #Number of cabs in a list

	df = pd.DataFrame({
		"cabine1":[12,15,25,24,16],
		"cabine2":[26,27,19,12,18],
		"cabine3":[14,28,22,16,23],},
		index = ["act1","act2", "act3", "act4", "act5"])

	df_out = weighted_average(df, Nb_cabs)
	arrange_stations(df_out, 40, 28)