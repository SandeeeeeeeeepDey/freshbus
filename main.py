from flask import Flask, request, jsonify
import pickle
import pandas as pd
from datetime import datetime
from utils.model_preprocess_utils import prepare_and_predict

from utils.distance_duration_utils import *
from utils.festival_utils import *
from data.festival_data import *
from utils.long_lat_utils import *
from data.feature_data import *
import os

# Define the base directory (e.g., the project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Construct the model path dynamically
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'Konkona_50_model_2.pkl')

# Load the trained model
try:
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
except FileNotFoundError:
    raise FileNotFoundError("Model file not found. Ensure 'Konkona_50_model_2.pkl' is in the correct directory.")
except pickle.UnpicklingError:
    raise ValueError("Failed to unpickle the model file. Ensure it is a valid pickle file.")
except Exception as e:
    raise RuntimeError(f"Unexpected error while loading the model: {e}")

# Create Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_demand():
    try:
        # Parse input JSON data
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid input: No JSON payload provided."}), 400
        except Exception as e:
            return jsonify({"error": f"Failed to parse input JSON: {e}"}), 400

        try:
            source = data.get('Source')
            destination = data.get('Destination')
            date_time = data.get('Date_time')
            Fare = data.get('Seat Fare')
            In_between_BP_names = data.get('In_between_BP_names')
            In_between_BP_timing = data.get('In_between_BP_timing')
            boarding_lat = None #data.get('boarding_lat')
            boarding_long = None #data.get('boarding_long')
            In_between_DP_names = data.get('In_between_DP_names')
            In_between_DP_timing = data.get('In_between_DP_timing')
            stoppage_lat = None # data.get('stoppage_lat')
            stoppage_long = None # data.get('stoppage_long')

            # Validate required fields
            # Source there or no
            if not source or len(source) < 1:
                return jsonify({"error": "Source field is required and cannot be empty"}), 400
            
            # Destination there or no
            if not destination or len(destination) < 1:
                return jsonify({"error": "Destination field is required and cannot be empty"}), 400
            
            # Datetime there or no
            if not date_time:
                date_time = datetime.now()
                date_time = date_time.replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
                date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
            
            # Seat fare there or no
            if Fare is None or not isinstance(Fare, (int, float)):
                return jsonify({"error": "Seat Fare must be a valid number"}), 400
            
            # Boarding Names, Timings there or no
            if not In_between_BP_names or not isinstance(In_between_BP_names, list):
                return jsonify({"error": "In_between_BP_names must be a non-empty list"}), 400
            if not In_between_BP_timing or not isinstance(In_between_BP_timing, list):
                return jsonify({"error": "In_between_BP_timing must be a non-empty list"}), 400
            
            # Boarding lists sizes are same or no
            if len(In_between_BP_names) != len(In_between_BP_timing):
                return jsonify({"error": "In_between_BP_timing must have same size as In_between_BP_names"}), 400

            # Stoppage Names, Timings there or no
            if not In_between_DP_names or not isinstance(In_between_DP_names, list):
                return jsonify({"error": "In_between_DP_names must be a non-empty list"}), 400
            if not In_between_DP_timing or not isinstance(In_between_DP_timing, list):
                return jsonify({"error": "In_between_DP_timing must be a non-empty list"}), 400
            
            # Stoppage lists sizes are same or no
            if len(In_between_DP_names) != len(In_between_DP_timing):
                return jsonify({"error": "In_between_DP_names must have same size as In_between_DP_timing"}), 400
            

        except Exception as e:
            return jsonify({"error": f"Input validation error: {e}"}), 400
        
         # Prepare DataFrame from input data
        try:
            input_data = pd.DataFrame({
                'source': [source],
                'destination': [destination],
                'Journey DateTime': [date_time],
                'Seat Fare': [Fare],
                'boarding_name': [In_between_BP_names],
                'boarding_lat': [boarding_lat],
                'boarding_long': [boarding_long],
                'boarding_timings': [In_between_BP_timing],
                'stoppage_name': [In_between_DP_names],
                'stoppage_timings': [In_between_DP_timing],
                'stoppage_lat': [stoppage_lat],
                'stoppage_long': [stoppage_long],
            })
        except Exception as e:
            return jsonify({"error": f"Failed to create DataFrame from input data: {e}"}), 400

 
        # Feature Engineering
        try:
            input_data = get_long_lat(input_data, "boarding", "stoppage")
            feature_df = construct_features(input_data)
            feature_df = catagorizing_days(feature_df)
            feature_df = new_get_dummy(feature_df, "boarding", "stoppage")
        except Exception as e:
            return jsonify({"error": f"Feature preparation error: {e}"}), 500

        # Final Pre-Process and Predict demand
        try:
            demand_prediction = prepare_and_predict(feature_df, model)
            return jsonify({"Demand": demand_prediction[0]})
        except Exception as e:
            return jsonify({"error": f"Prediction error: {e}"}), 500
    
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
