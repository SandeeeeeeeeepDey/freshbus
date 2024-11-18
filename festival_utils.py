
import pandas as pd
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder
from festival_data import *

def change_str_dicts_to_datetime(calend_dict_event_year_datetuple):
    ranges = {
        event: {
            year: (
                pd.to_datetime(start),
                pd.to_datetime(end)
            ) for year, (start, end) in years.items()
        } for event, years in calend_dict_event_year_datetuple.items()
    }

    return ranges

def calculate_since_until_days_vectorized(f_df, calend_dict_event_year_datetuple, until_since_col_prefix: str):
    event_ranges = change_str_dicts_to_datetime(calend_dict_event_year_datetuple)

    # Iterate through each row (journey) in the DataFrame
    for index, row in tqdm(f_df.iterrows(), total = len(f_df)):
        journey_date = pd.to_datetime(row["Journey DateTime"])

        for event, year_ranges in event_ranges.items():
            journey_year = journey_date.year

            # Initialize hours until/since variables
            hours_until = float('inf')
            hours_since = float('inf')

            # --o--o--o--o
            for year in [journey_year, journey_year + 1]:  # check current year
                if year in year_ranges:
                    event_date = year_ranges[year][0]  # start date of the event
                    if event_date >= journey_date:
                        # Calculate hours difference
                        hours_until = min(hours_until, (event_date - journey_date).total_seconds() / 3600)
                        break

            # Check for the nearest past date (Days Since)
            for year in [journey_year, journey_year - 1]:  # check current year and previous year
                if year in year_ranges:
                    event_date = year_ranges[year][0]  # start date of the event
                    if event_date <= journey_date:
                        # Calculate hours difference
                        hours_since = min(hours_since, (journey_date - event_date).total_seconds() / 3600)
                        break

            # Assign the calculated days (hours / 24) until and since to the DataFrame
            f_df.loc[index, f'{until_since_col_prefix}{event}_Days Until'] = round(hours_until / 24) if hours_until != float('inf') else None
            f_df.loc[index, f'{until_since_col_prefix}{event}_Days Since'] = round(hours_since / 24) if hours_since != float('inf') else None

    return f_df

# print

def check_if_in_range_vectorized(f_df, calend_dict_event_year_datetuple, name:str):

    holiday_ranges = change_str_dicts_to_datetime(calend_dict_event_year_datetuple)

    # Create a list to store holiday results
    f_df[f'{name}'] = None

    # Iterate through each journey date
    for index, row in tqdm(f_df.iterrows(), total = len(f_df)):
        journey_date = row['Journey DateTime']
        journey_year = journey_date.year
        for vacation_type, df_journey_years in holiday_ranges.items():
            for offset_year in [0, -1]:
                holiday_year = journey_year + offset_year
                if holiday_year in df_journey_years:
                    start_date, end_date = df_journey_years[holiday_year]
                    start_date -= pd.Timedelta(days=7)  # Extend range by -7 days
                    end_date += pd.Timedelta(days=7)    # Extend range by +7 days
                    if start_date <= journey_date <= end_date:
                        f_df.at[index, f'{name}'] = vacation_type
                        break
    return f_df

def categorize_proximity(days):
    if days < 1:
        return "Carolina Reaper"
    elif days == 1:
        return 'hottest'
    elif 2 <= days <= 7:
        return 'hotter'
    elif 8 <= days <= 20:
        return 'hot'
    elif 21 <= days <= 25:
        return 'cold'
    elif 26 <= days <= 31:
        return 'colder'
    else:
        return 'coldest'

def catagorizing_days(m_df):
    print("categorizing proximities function initiated...")
    days_columns = [col for col in m_df.columns if 'Days Until' in col or 'Days Since' in col]

    label_encoders = {}

    for col in tqdm(days_columns, total = len(days_columns)):
        m_df[col + '_Proximity'] = m_df[col].apply(categorize_proximity)
        le = LabelEncoder()
        m_df[col + '_Proximity'] = le.fit_transform(m_df[col + '_Proximity'])
        label_encoders[col + '_Proximity'] = le

    m_df.drop(columns=days_columns, inplace=True)
    print("Catagorizing priximity features Complete...\n")
    return m_df

def construct_features(s):
    f_df = s.copy()

    # Time Features
    with tqdm(total=6, desc="Time Features", leave=False) as pbar:
        tqdm.write("Fest Features Cunstruct Fn initiated...")
        f_df['Journey DateTime'] = pd.to_datetime(f_df['Journey DateTime'])  # Ensure the column is in datetime format
        f_df['Month'] = f_df['Journey DateTime'].dt.month
        f_df['Day'] = f_df['Journey DateTime'].dt.day
        f_df['Day of Week'] = f_df['Journey DateTime'].dt.day_name()  # Get day of the week
        f_df['Hour'] = f_df['Journey DateTime'].dt.hour
        f_df['Minute'] = f_df['Journey DateTime'].dt.minute
        f_df['Is Weekend'] = f_df['Day of Week'].isin(['Saturday', 'Sunday'])
        pbar.update(1)

        tqdm.write("Processing Fixed Festivals...")
        # Fixed Fests
        f_df = calculate_since_until_days_vectorized(f_df, fixed_fests, "Fixed_Dates_")
        pbar.update(1)

        tqdm.write("Processing Moving Festival Ranges...")
        # Moving Fest Ranges
        f_df = calculate_since_until_days_vectorized(f_df, moving_dates, "Moving_Dates_")
        pbar.update(1)

        tqdm.write("Processing Vacation Range...")
        # Vacation range
        f_df = check_if_in_range_vectorized(f_df, school_holidays, "School_vacation")
        pbar.update(1)

        tqdm.write("Processing Wedding Season Range...")
        # Wedding Range
        f_df = check_if_in_range_vectorized(f_df, wedding_seasons, "Wedding_Season")
        pbar.update(1)

        tqdm.write("Finalizing Data...")
        # In Domain or no
        f_df["School_vacation"].fillna("No Vacation", inplace=True)
        f_df["Wedding_Season"].fillna("No Wedding", inplace=True)
        pbar.update(1)

    tqdm.write("Feature construction completed.\n")

    return f_df

