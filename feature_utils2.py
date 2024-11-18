from datetime import datetime, timedelta
from tqdm import tqdm
import requests
from googlemaps import Client
import pandas as pd
from secret import secret_key

api_key = secret_key  # Replace with your actual API key
gmaps = Client(key=api_key)


def get_distance_and_duration(origin_lat, origin_lng, dest_lat, dest_lng, departure_time):
    """Gets distance and duration between two points using Google Maps API"""

    origin = (origin_lat, origin_lng)
    destination = (dest_lat, dest_lng)
    result = gmaps.distance_matrix(origin, destination, mode="driving", departure_time=departure_time)

    distance = result['rows'][0]['elements'][0]['distance']['value']/1000
    duration = result['rows'][0]['elements'][0]['duration']['value']/3600
    origin_addresses = result["origin_addresses"]
    destination_addresses = result["destination_addresses"]
    return distance, duration, origin_addresses, destination_addresses


# 1: for each in-between places, we create lat and long and fill them instead of just creating dummies
def new_get_dummy(m_df, boarding:str, stoppage: str):
    print("Now calculating the distanceses and durations...")
    for inx, row in tqdm(m_df.iterrows(), total = len(m_df)):
        # 2: Calculate - Distancece and - Duration too
        distance = 0
        duration = 0
        source_temp_lat = row[f"{boarding}_lat"][0]
        source_temp_long = row[f"{boarding}_long"][0]
        # source_temp = row[f"{boarding}_name"][0]

        destination_temp_lat = row[f"{stoppage}_lat"][0]
        destination_temp_long = row[f"{stoppage}_long"][0]
        # destination_temp = row[f"{stoppage}_name"][0]

        distances_list_boardings = []
        durations_list_boardings = []
        distances_list_stoppages = []
        durations_list_stoppages = []

        distances_list = []
        durations_list = []
        # pd.set_option('display.max_columns', None)
        adrses = []
        # d_adrses = []
        # print(row)
        for bna, bla, blo, btime in zip(row[f"{boarding}_name"], row[f"{boarding}_lat"], row[f"{boarding}_long"], row[f"{boarding}_timings"]):
            # print(bna, bla, blo, btime)
            btime = datetime.strptime(btime, '%Y-%m-%d %H:%M:%S')
            today = datetime.now()

            # Update btime's date based on the day of the week from data
            btime_weekday = btime.weekday()
            if btime < today:
                if btime_weekday == 6:
                    btime = today
                else:
                    days_to_next_weekday = (btime_weekday - today.weekday() + 7) % 7
                    days_to_next_weekday = days_to_next_weekday if days_to_next_weekday != 0 else 7
                    btime = today + timedelta(days=days_to_next_weekday)
                btime = btime.replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
                btime = datetime.strptime(btime, '%Y-%m-%d %H:%M:%S')
            distance_temp, duration_temp, o_adrs, d_adrs = get_distance_and_duration(source_temp_lat, source_temp_long, bla, blo, btime)
            distance += distance_temp
            duration += duration_temp
            distances_list.append(distance_temp)
            durations_list.append(duration_temp)
            distances_list_boardings.append(distance_temp)
            durations_list_boardings.append(duration_temp)

            adrses.append(o_adrs)

            m_df.at[inx, f"{boarding}_{bna}_name"] = bna
            m_df.at[inx, f"{boarding}_{bna}_lat"] = bla
            m_df.at[inx, f"{boarding}_{bna}_long"] = blo

            # source_temp = bna
            source_temp_lat = bla
            source_temp_long = blo

        destination_temp_lat = row[f"{boarding}_lat"][-1]
        destination_temp_long = row[f"{boarding}_long"][-1]
        # destination_temp = row[f"{boarding}_name"][-1]

        for sna, sla, slo, stime in zip(row[f"{stoppage}_name"], row[f"{stoppage}_lat"], row[f"{stoppage}_long"], row[f"{stoppage}_timings"]):

            stime = datetime.strptime(stime, '%Y-%m-%d %H:%M:%S')

            today = datetime.now()

            stime_weekday = stime.weekday()

            if stime_weekday == 6:
                stime = today
            else:
                days_to_next_weekday = (stime_weekday - today.weekday() + 7) % 7
                days_to_next_weekday = days_to_next_weekday if days_to_next_weekday != 0 else 7
                stime = today + timedelta(days=days_to_next_weekday)

            distance_temp, duration_temp, o_adrs, d_adrs = get_distance_and_duration(destination_temp_lat, destination_temp_long, sla, slo, stime)
            distance += distance_temp
            duration += duration_temp

            distances_list.append(distance_temp)
            durations_list.append(duration_temp)
            distances_list_stoppages.append(distance_temp)
            durations_list_stoppages.append(duration_temp)

            adrses.append(o_adrs)

            m_df.at[inx, f"{stoppage}_{sna}_name"] = sna
            m_df.at[inx, f"{stoppage}_{sna}_lat"] = sla
            m_df.at[inx, f"{stoppage}_{sna}_long"] = slo


            # destination_temp = sna
            destination_temp_lat = sla
            destination_temp_long = slo

        # featurize last distance of boarding to first stoppage
        m_df.at[inx, f"main_distance"] = f"{distance_temp}"
        m_df.at[inx, f"main_duration"] = f"{duration_temp}"
        m_df.at[inx, f"main_o_adrses"] = f"{o_adrs}"
        m_df.at[inx, f"main_d_adrses"] = f"{d_adrs}"

        # Distance Duration lists for each row
        m_df.at[inx, f"list_distances"] = f"{distances_list}"
        m_df.at[inx, f"list_durations"] = f"{durations_list}"

        # Total Distance Duration lists for each row
        m_df.at[inx, f"total_distance"] = distance
        m_df.at[inx, f"total_duration"] = duration

        m_df.at[inx, "o_adrses"] = f"{adrses}"
    print("Distance and Duration calculated...\n")
    return m_df