#Import required libraries
import requests
import json
import pandas as pd
import numpy as np
from pulp import *

#Retrieve the fpl player data from the hard-coded url
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

response = requests.get(url)

#Create initial dataset by parsing json file 
responseStr = response.text
data = json.loads(responseStr)

#Build dataframes from the raw data
json = response.json()

elements_df = pd.DataFrame(data['elements'])
elements_types_df = pd.DataFrame(data['element_types'])
teams_df = pd.DataFrame(data['teams'])

#Look at columns in elements_df
elements_df.columns

elements_df.head()

#Reformat some fields
elements_df["full_name"] = elements_df["first_name"] + " " + elements_df["second_name"]

elements_df["cost"] = elements_df["now_cost"]/10

elements_df['xPoints'] = elements_df.ep_this.astype(float)

slim_elements_df = elements_df[['full_name','id','team','element_type','cost','total_points','xPoints','points_per_game','value_season','ep_this','ep_next','chance_of_playing_this_round','selected_by_percent','minutes','transfers_in','goals_scored','assists','clean_sheets','bps','influence','creativity','threat','ict_index','expected_goals','expected_assists','expected_goal_involvements','expected_goals_conceded','corners_and_indirect_freekicks_order','direct_freekicks_order','penalties_order','expected_goals_per_90','expected_assists_per_90','saves_per_90','expected_goals_conceded_per_90','form_rank']]


slim_elements_df.head()

