import pandas as pd
from sklearn.preprocessing import LabelEncoder
from data.feature_data import *

all_features = moving_date_features + fixed_date_features + base_features + dist_duration_features + longs_features + lats_features + between_names + between_verifier


def prepare_and_predict(input_data, model):
    try:
        # Ensure all required columns are present
        for col in all_features:
            if col not in input_data.columns:
                input_data[col] = pd.NA

        # Encode categorical columns
        df_encoded = input_data.copy()
        categorical_columns = ['Day of Week', 'source', 'destination', 'School_vacation', 'Wedding_Season', 'boarding_Wipro Circle_name'] + between_names

        label_encoders = {}
        for column in categorical_columns:
            le = LabelEncoder()
            df_encoded[column] = le.fit_transform(df_encoded[column])
            label_encoders[column] = le  # Save the encoder for possible inverse transformation

        # Prepare numeric features
        df_encoded["base fare"] = df_encoded["Seat Fare"]

        # Drop unnecessary columns
        columns_to_drop = other + between_names + lats_features + longs_features + between_verifier
        X_test = df_encoded.drop(columns=columns_to_drop)

        # Sanitize column names for LightGBM
        X_test.columns = X_test.columns.str.replace(r'[^A-Za-z0-9_]+', '_', regex=True)

        # Make predictions
        y_pred = model.predict(X_test)

        return y_pred
    except Exception as e:
        raise ValueError(f"Error during prediction preparation: {e}")