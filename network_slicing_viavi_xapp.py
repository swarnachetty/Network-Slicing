import json
import requests
import sys
import pandas as pd
import time
from get_last_simulation_id_non_stand_alone import get_largest_simulation_id


check_db_status = 1
# check for status
def connect_to_endpoint(url_address):
    res = requests.get(url_address)
    print("==================")
    print("response ok 200 = ",res.status_code)
    print("==================")
    # print(response.url)
    # print(response.headers['x-rate-limit-remaining'])
    return res.json()

if check_db_status==1:
    #querry_address = 'http://127.0.0.1/sba/influx/query?q=SELECT%20*%20FROM%20UEReports%20group%20by%20%22report%22%20order%20%20by%20time%20DESC%20LIMIT%201'
    querry_address = 'http://144.32.33.150/sba/influx/query?q=SELECT%20*%20FROM%20UEReports%20group%20by%20%22report%22%20order%20%20by%20time%20DESC%20LIMIT%201'
    response = connect_to_endpoint(querry_address)
    #print("respone type", type(response))
    #print("response length", len(response))
    print("================================")

# function to change from json to pandas df and add 'Viavi.UE.Name' as a DataFrame column
def jsonbody_to_df(json_data):
    df = pd.DataFrame()

    # Iterate over the series in the JSON response
    for series in json_data['results'][0]['series']:
        # Extract the columns and values
        columns = series['columns']
        values = series['values']
        
        # Create a temporary DataFrame
        df_temp = pd.DataFrame(values, columns=columns)
        
        # Add 'Viavi.UE.Name' from the 'tags' section as a new column
        df_temp['Viavi.UE.Name'] = series['tags']['Viavi.UE.Name']
        
        # Append to the main DataFrame
        df = pd.concat([df, df_temp], ignore_index=True)

    return df


def processing_ue_reports(endurl="http://144.32.33.150/influx/query?db=1222-simulation&q=SELECT%20*%20FROM%20%22UEReports%22%20GROUP%20BY%20%22Viavi.UE.Name%22%20LIMIT%201"):
    """
    Parameters:
    num_of_reported_nbs : integer, Number of neighbor cells present in UE Measurement reports.
    endurl : str, RESTapi URL to request UEReports.

    Returns: Processed pandas dataframe.
    """
    jsonbody = connect_to_endpoint(endurl)
    #print (jsonbody)
    #num_of_UEs = len(jsonbody['results'][0]['series'])
    #print("Number of UEs in the network:", num_of_UEs)
    
    df = jsonbody_to_df(jsonbody)
    df.to_csv("ue_kpm.txt", sep='\t')


    # get the KPMs of interest and store them in a new data frame
    cols_kpm = ['time','Viavi.UE.Name', 'Viavi.UE.Slice','DRB.UEThpDl', 'DRB.UEThpUl',
                'Viavi.UE.targetThroughputDl', 'Viavi.Cell.Name']

    df_kpms = df.loc[:, cols_kpm]

    return df_kpms


# Define the URL and starting ID
#url_ip = "10.122.14.52"
url_ip = "144.32.33.150"
check_db_status = 1
url_to_stop = f"http://{url_ip}/sba/tests/status/20-simulation"
url = f"http://{url_ip}/sba/influx/query?q=SHOW%20DATABASES"
largest_simulation_id = get_largest_simulation_id(url)
url_small = f"http://{url_ip}/influx/query?db="
print("simulation id = ", largest_simulation_id)

# turn off idle cells
# Define the URL for the reports
url = "http://144.32.33.150/sba/influx/query?q=SELECT%20*%20FROM%20CellReports%20GROUP%20BY%20%22Viavi.Cell.Name%22%20ORDER%20BY%20time%20DESC%20LIMIT%201"
# url_UE = "http://144.32.33.150/sba/influx/query?q=SELECT%20*%20FROM%20UEReports%20GROUP%20BY%20%22Viavi.Cell.Name%22%20ORDER%20BY%20time%20DESC%20LIMIT%201"
url_UE = f"{url_small}{largest_simulation_id}-simulation&q=SELECT%20*%20FROM%20%22UEReports%22%20GROUP%20BY%20%22Viavi.UE.Name%22%20ORDER%20BY%20time%20DESC%20LIMIT%201"

kpsm = processing_ue_reports(url_UE)
# df1 = df[['a', 'b']]

# what is the paln? for each of the slices, check user is unique and add
# the throughput to a total. 
"""
do this for n amounts of slices

ie: 3, 6, 2; T= 11 
4, 8, 0.1; T=12.1
2, 8, 4; T=14

So what we do is create a ratio like 3:6:2, all timesed by 1.3, then divide by
total. So 3:6:2 (times 1.3)-> 3.9:7.8:2.6
 
As ratios, we add totals: 14.3, then hold off 5% for emergencies, divide by total
14.3 + 5% = 15 -- /15*100 to get the percentages for network slices'

26:52:17.3 - round nearest !! Then send this off to the api
"""

def sum_of_throughputs(df_kpms):
    # sums the throughput downlink for the users, per slices
    # df_kpms.assign(Entity_ID_perc = df_kpms.groupby('Viavi.UE.Slice')['DRB.UEThpUl'].sum())
    return df_kpms.groupby('Viavi.UE.Slice')['DRB.UEThpUl'].sum()
    
def calculate_slicing_percentage(df_thp_per_slice):
    # first sum them all, then add 5%
    total_thp_utilised = df_thp_per_slice['DRB.UEThpUl'].sum() * 1.05
    # now i am finding the percentages, by dividing by the total
    dive = df_thp_per_slice['DRB.UEThpUl'].div(total_thp_utilised*0.01).round(1)
    return dive
    # df_thp_per_slice.to_csv("yooo.txt", sep='\t')
    
df_kpms_ue = sum_of_throughputs(kpsm).reset_index()
# print(pd.DataFrame(df_kpms_ue))
calculate_slicing_percentage(df_kpms_ue)

# ee.to_csv("holaaa.txt", sep='\t')
"""
 df.assign(Entity_ID_perc = df.groupby('Entity ID')['% Ownership'].sum() / 100)
    Entity ID   % Ownership Entity_ID_perc
0   12345       100.00      1.0000
1   45643       49.56       0.4956
2   00000       100.00      2.0000
3   00000       100.00      2.0000

for cell_id in viavi_cell_names_with_zero_connmean:
    send_to_endpoint(cell_id)
    print(cell_id)
    # Pause the simulation for 3 seconds based on VIAVI recommendation
    time.sleep(3)
"""


            
    
    
    
    

