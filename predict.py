from flask import Flask, request, jsonify
import pickle
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from feature_engineering import *

# Load the trained model
with open('xgb_final_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Create Flask app
app = Flask(__name__)

features = ['From', 'To', 'Seat Fare',  'Month','Day', 'Day of Week', 'Hour', 'Minute', 'Is Weekend', 'School_vacation', 'Wedding_Season', "Fixed_Dates_New Year's Day_Days Until_Proximity", "Fixed_Dates_New Year's Day_Days Since_Proximity", 'Fixed_Dates_Makar Sankranti/Pongal_Days Until_Proximity', 'Fixed_Dates_Makar Sankranti/Pongal_Days Since_Proximity', 'Fixed_Dates_Republic Day_Days Until_Proximity', 'Fixed_Dates_Republic Day_Days Since_Proximity', 'Fixed_Dates_Dr. Ambedkar Jayanti_Days Until_Proximity', 'Fixed_Dates_Dr. Ambedkar Jayanti_Days Since_Proximity', "Fixed_Dates_May Day/Workers' Day_Days Until_Proximity", "Fixed_Dates_May Day/Workers' Day_Days Since_Proximity", 'Fixed_Dates_Independence Day_Days Until_Proximity', 'Fixed_Dates_Independence Day_Days Since_Proximity', 'Fixed_Dates_Gandhi Jayanti_Days Until_Proximity', 'Fixed_Dates_Gandhi Jayanti_Days Since_Proximity', 'Fixed_Dates_Kannada Rajyotsava_Days Until_Proximity', 'Fixed_Dates_Kannada Rajyotsava_Days Since_Proximity', 'Fixed_Dates_Christmas_Days Until_Proximity', 'Fixed_Dates_Christmas_Days Since_Proximity', 'Fixed_Dates_Telangana Formation Day_Days Until_Proximity', 'Fixed_Dates_Telangana Formation Day_Days Since_Proximity', 'Fixed_Dates_International Yoga Festival_Days Until_Proximity', 'Fixed_Dates_International Yoga Festival_Days Since_Proximity', 'Fixed_Dates_Numaish (All India Industrial Exhibition)_Days Until_Proximity', 'Fixed_Dates_Numaish (All India Industrial Exhibition)_Days Since_Proximity', 'Moving_Dates_Guru Nanak Jayanti_Days Until_Proximity', 'Moving_Dates_Guru Nanak Jayanti_Days Since_Proximity', 'Moving_Dates_Naraka Chaturdashi_Days Until_Proximity', 'Moving_Dates_Naraka Chaturdashi_Days Since_Proximity', 'Moving_Dates_Bhai Dooj_Days Until_Proximity', 'Moving_Dates_Bhai Dooj_Days Since_Proximity', 'Moving_Dates_Maha Navami_Days Until_Proximity', 'Moving_Dates_Maha Navami_Days Since_Proximity', 'Moving_Dates_Vijayadashami (Dussehra)_Days Until_Proximity', 'Moving_Dates_Vijayadashami (Dussehra)_Days Since_Proximity', 'Moving_Dates_Karwa Chauth_Days Until_Proximity', 'Moving_Dates_Karwa Chauth_Days Since_Proximity', 'Moving_Dates_Diwali_Days Until_Proximity', 'Moving_Dates_Diwali_Days Since_Proximity', 'Moving_Dates_Krishna Janmashtami_Days Until_Proximity', 'Moving_Dates_Krishna Janmashtami_Days Since_Proximity', 'Moving_Dates_Ganesh Chaturthi_Days Until_Proximity', 'Moving_Dates_Ganesh Chaturthi_Days Since_Proximity', 'Moving_Dates_Eid-ul-Fitr_Days Until_Proximity', 'Moving_Dates_Eid-ul-Fitr_Days Since_Proximity', 'Moving_Dates_Buddha Purnima_Days Until_Proximity', 'Moving_Dates_Buddha Purnima_Days Since_Proximity', 'Moving_Dates_Bakrid (Eid-ul-Adha)_Days Until_Proximity', 'Moving_Dates_Bakrid (Eid-ul-Adha)_Days Since_Proximity', 'Moving_Dates_Muharram_Days Until_Proximity', 'Moving_Dates_Muharram_Days Since_Proximity', 'Moving_Dates_Ratha Saptami_Days Until_Proximity', 'Moving_Dates_Ratha Saptami_Days Since_Proximity', 'Moving_Dates_Maha Shivaratri_Days Until_Proximity', 'Moving_Dates_Maha Shivaratri_Days Since_Proximity', 'Moving_Dates_Holika Dahan_Days Until_Proximity', 'Moving_Dates_Holika Dahan_Days Since_Proximity', 'Moving_Dates_Holi_Days Until_Proximity', 'Moving_Dates_Holi_Days Since_Proximity', 'Moving_Dates_Ugadi_Days Until_Proximity', 'Moving_Dates_Ugadi_Days Since_Proximity', 'Moving_Dates_Ram Navami_Days Until_Proximity', 'Moving_Dates_Ram Navami_Days Since_Proximity', 'Moving_Dates_Hanuman Jayanti_Days Until_Proximity', 'Moving_Dates_Hanuman Jayanti_Days Since_Proximity', 'Moving_Dates_Good Friday_Days Until_Proximity', 'Moving_Dates_Good Friday_Days Since_Proximity', 'Moving_Dates_Tirupati Brahmotsavam_Days Until_Proximity', 'Moving_Dates_Tirupati Brahmotsavam_Days Since_Proximity', 'Moving_Dates_Visakha Utsav_Days Until_Proximity', 'Moving_Dates_Visakha Utsav_Days Since_Proximity', 'Moving_Dates_Deccan Festival_Days Until_Proximity', 'Moving_Dates_Deccan Festival_Days Since_Proximity', 'Moving_Dates_Lumbini Festival_Days Until_Proximity', 'Moving_Dates_Lumbini Festival_Days Since_Proximity', 'Moving_Dates_Art Mela_Days Until_Proximity', 'Moving_Dates_Art Mela_Days Since_Proximity', 'Moving_Dates_Bathukamma Festival_Days Until_Proximity', 'Moving_Dates_Bathukamma Festival_Days Since_Proximity', 'Moving_Dates_Bonalu Festival_Days Until_Proximity', 'Moving_Dates_Bonalu Festival_Days Since_Proximity', 'Moving_Dates_Hyderabad International Film Festival_Days Until_Proximity', 'Moving_Dates_Hyderabad International Film Festival_Days Since_Proximity', 'Moving_Dates_Hampi Utsav_Days Until_Proximity', 'Moving_Dates_Hampi Utsav_Days Since_Proximity', 'Moving_Dates_Karaga Festival_Days Until_Proximity', 'Moving_Dates_Karaga Festival_Days Since_Proximity', 'Moving_Dates_Mysore Dasara_Days Until_Proximity', 'Moving_Dates_Mysore Dasara_Days Since_Proximity', 'Moving_Dates_Bangalore Habba_Days Until_Proximity', 'Moving_Dates_Bangalore Habba_Days Since_Proximity']

@app.route('/predict', methods=['POST'])
def predict_demand():
    data = request.get_json()

    source = data.get('Source')
    destination = data.get('Destination')
    date_time = data.get('Date_time')
    Fare = data.get('Seat Fare')

    if not source or not destination or not date_time:
        return jsonify({'error': 'Missing parameters. Please provide Source, Destination, and Date_time.'}), 400

    # Create a DataFrame from the input data
    input_data = pd.DataFrame({
        'From': [source],
        'To': [destination],
        'Journey DateTime': [date_time],
        'Seat Fare': [Fare]
    })

    # Perform feature engineering
    try:
        feature_df = construct_features(input_data)

        feature_df = catagorizing_days(feature_df)

        feature_df['Journey DateTime'] = pd.to_datetime(feature_df['Journey DateTime'], errors='coerce')
        categorical_columns = ['Day of Week', 'To', 'From', 'School_vacation', 'Wedding_Season']
        label_encoders = {}

        for column in categorical_columns:
            le = LabelEncoder()
            feature_df[column] = le.fit_transform(feature_df[column])
            label_encoders[column] = le  # Save the encoder for possible inverse transformation
    
        feature_df = feature_df.drop(columns=['Journey DateTime'])
        feature_df = feature_df[features]
        feature_df = feature_df.applymap(lambda x: x.encode('ascii', 'ignore').decode('ascii') if isinstance(x, str) else x)
        print(feature_df.columns)
        
        prediction = model.predict(feature_df)

    except Exception as e:
        raise e
        return jsonify({'error': f'Feature engineering failed: {str(e)}'}), 500

    # Make a prediction using the model
    try:
        prediction = model.predict(features)[0]  # Assuming the model outputs a single prediction
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

    # Return the prediction
    return jsonify({'predicted_demand': prediction})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
