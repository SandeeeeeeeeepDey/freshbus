from tqdm import tqdm
from data.long_lat_data import dict_to_get_long_lat_from

# Delete Experiment
def get_long_lat(m_df, boarding:str, stoppage:str):
    print("\nfetching lats and longs...")
    for inx, row in tqdm(m_df.iterrows(), total=len(m_df)):
        blong_list = []
        blat_list = []
        for i in row[f"{boarding}_name"]:
            # print("------------------------",i, dict_to_get_long_lat_from[i])
            blong_list.append(dict_to_get_long_lat_from[i][1])
            blat_list.append(dict_to_get_long_lat_from[i][0])
        # print("blong_list",blong_list)
        # print("blat_list",blat_list)
        m_df.at[inx, f"{boarding}_long"] = blong_list
        m_df.at[inx, f"{boarding}_lat"] = blat_list

        # print(m_df.loc[inx, f"{boarding}_long"])
        slong_list = []
        slat_list = []
        for i in row[f"{stoppage}_name"]:
            slong_list.append(dict_to_get_long_lat_from[i][1])
            slat_list.append(dict_to_get_long_lat_from[i][0])
        m_df.at[inx, f"{stoppage}_long"] = slong_list
        m_df.at[inx, f"{stoppage}_lat"] = slat_list
    print("Fetching is done\n")
    # print("jjjjjjjjjjjjjjjjjjjjjj", len(dict_to_get_long_lat_from))
    return m_df