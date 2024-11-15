from flask import Flask, request, jsonify
import pickle
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from feature_engineering_v1 import *
from feature_utils import *
import lightgbm as lgb
from feature_utils2 import *
from festival_utils import *
from festival_data import *
from long_lat_utils import *
from sklearn.metrics import mean_squared_error
import numpy as np
import xgboost as xgb
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, r2_score

# Load the trained model
with open('Konkona_50_model_2.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Create Flask app
app = Flask(__name__)

other = ['Ticket No', 'Journey DateTime', 'Route', "Service_Name", "Seat Fare"]
all_features = moving_date_features + fixed_date_features + base_features + dist_duration_features + longs_features + lats_features + between_names + between_verifier


@app.route('/predict', methods=['POST'])
def predict_demand():
    data = request.get_json()

    source = data.get('Source')
    destination = data.get('Destination')
    date_time = data.get('Date_time')
    Fare = data.get('Seat Fare')
    In_between_BP_names = data.get('In_between_BP_names')
    In_between_BP_timing = data.get('In_between_BP_timing')
    boarding_lat = data.get('boarding_lat')
    boarding_long = data.get('boarding_long')
    In_between_DP_names = data.get('In_between_DP_names')
    In_between_DP_timing = data.get('In_between_DP_timing')
    stoppage_lat = data.get('stoppage_lat')
    stoppage_long = data.get('stoppage_long')
    
    # if not source or not destination or not date_time or not In_between_BP_names or \
    #     not In_between_BP_timing or In_between_DP_names or not In_between_DP_timing:
    #     return jsonify({'error': 'Missing parameters. Please provide Source, Destination, and Date_time along with tht Boarding and Dropping points.'}), 400

    # Create a DataFrame from the input data
    input_data = pd.DataFrame({
        'source': [source],
        'destination': [destination],
        'Journey DateTime': [date_time],
        'Seat Fare': [Fare],
        'boarding_name':[In_between_BP_names],
        'boarding_lat':[boarding_lat],
        'boarding_long':[boarding_long],
        'boarding_timings':[In_between_BP_timing],
        'stoppage_name':[In_between_DP_names],
        'stoppage_timings':[In_between_DP_timing],
        'stoppage_lat':[stoppage_lat],
        'stoppage_long':[stoppage_long],
    })
    # input_data = get_long_lat(input_data, "boarding", "stoppage")

    feature_df = construct_features(input_data)
    
    feature_df = catagorizing_days(feature_df)
    # print(feature_df.columns)
    # print(feature_df.boarding_name)
    # print(feature_df.boarding_lat)
    # print(feature_df.boarding_timings)
    feature_df = new_get_dummy(feature_df, "boarding", "stoppage")

    #To have all the required columns in the df
    for col in all_features:
        if col not in feature_df.columns:
            feature_df[col] = pd.NA

    df_encoded = feature_df.copy()
    # print("between_names########", between_names)
    #Cat Cols
    categorical_columns = ['Day of Week', 'source', 'destination', 'School_vacation', 'Wedding_Season', 'boarding_Wipro Circle_name'] + between_names

    # print("categorical_columns*************", categorical_columns)
    label_encoders = {}

    for column in categorical_columns:
        le = LabelEncoder()
        # print(column)
        df_encoded[column] = le.fit_transform(df_encoded[column])
        label_encoders[column] = le  # Save the encoder for possible inverse transformation

    #Seat Fare
    df_encoded["base fare"] = df_encoded["Seat Fare"]#.apply(lambda x: x.min())

    columns_to_drop = other + between_names + lats_features + longs_features + between_verifier

    X_test = df_encoded.drop(columns=columns_to_drop)
    y_test = df_encoded['Ticket No']


    # train_split = df_encoded[df_encoded["Journey DateTime"] <= pd.to_datetime("2024-06-01")]
    # test_split = df_encoded[df_encoded["Journey DateTime"] > pd.to_datetime("2024-06-01")]

    # # Combine both lists into a single list of columns to drop
    # other = ['Ticket No', 'Journey DateTime', 'Route', "Service_Name", "Seat Fare"]
    # #columns_to_drop = base_features + moving_date_features + fixed_date_features + between_verifier + dist_duration_features + between_features + lats_features + longs_features + between_names
    # columns_to_drop = other + between_names + lats_features + longs_features

    # # Drop the specified columns from both X_train and X_test
    # X_train = train_split.drop(columns=columns_to_drop)
    # y_train = train_split['Ticket No']

    # X_test = test_split.drop(columns=columns_to_drop)
    # y_test = test_split['Ticket No']


    # Replace special characters in feature names to ensure compatibility with LightGBM
    # X_train.columns = X_train.columns.str.replace(r'[^A-Za-z0-9_]+', '_', regex=True)
    X_test.columns = X_test.columns.str.replace(r'[^A-Za-z0-9_]+', '_', regex=True)
    
    features_python = {str(feature) for feature in model.feature_names_in_}
    print("9999999999999999",len(set(X_test.columns) - set(features_python)), set(X_test.columns) - set(features_python))
    print("9999999999999999", len(set(features_python) - set(X_test.columns)), set(features_python) - set(X_test.columns))

    print("\n++++++++++",set(X_test.columns))
    print("\n++++++++++",set(features_python))
    y_pred = model.predict(X_test)
    
    print(type(y_pred))
    # print(feature_df, "HHHHHHHHHHHHHHHHk")
    #jsonify(feature_df.shape)
    return jsonify(y_pred[0])  
    
    # Perform feature engineering

    #     feature_df['Journey DateTime'] = pd.to_datetime(feature_df['Journey DateTime'], errors='coerce')
    #     categorical_columns = ['Day of Week', 'To', 'From', 'School_vacation', 'Wedding_Season']
    #     label_encoders = {}

    #     for column in categorical_columns:
    #         le = LabelEncoder()
    #         feature_df[column] = le.fit_transform(feature_df[column])
    #         label_encoders[column] = le  # Save the encoder for possible inverse transformation
    
    #     feature_df = feature_df.drop(columns=['Journey DateTime'])
    #     feature_df = feature_df[all_features]
    #     feature_df = feature_df.applymap(lambda x: x.encode('ascii', 'ignore').decode('ascii') if isinstance(x, str) else x)
    #     print(feature_df.columns)
        
    #     prediction = model.predict(feature_df)

    # except Exception as e:
    #     raise e
    #     return jsonify({'error': f'Feature engineering failed: {str(e)}'}), 500

    # # Make a prediction using the model
    # try:
    #     prediction = model.predict(all_features)[0]  # Assuming the model outputs a single prediction
    # except Exception as e:
    #     return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

    # # Return the prediction
    # return jsonify({'predicted_demand': prediction})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
