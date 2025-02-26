from flask import Flask, request, jsonify
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np

app = Flask(__name__)

# Load dataset
meals_df = pd.read_csv(r"C:\Users\sarth\Downloads\MealMatchingSystem\cleaned_nutrition_dataset.csv")

# Preprocess data for KNN
def preprocess_data(df):
    # Normalize numerical features
    numerical_cols = ['Calories', 'Protein', 'Fat', 'Sat.Fat', 'Fiber', 'Carbs']
    df[numerical_cols] = (df[numerical_cols] - df[numerical_cols].mean()) / df[numerical_cols].std()
    return df

meals_df = preprocess_data(meals_df)

# Train KNN model
def train_knn(df):
    features = df[['Calories', 'Protein', 'Fat', 'Sat.Fat', 'Fiber', 'Carbs']]
    knn = NearestNeighbors(n_neighbors=5, metric='cosine')
    knn.fit(features)
    return knn

knn_model = train_knn(meals_df)

# API Endpoint
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    user_preferences = data.get('user_preferences', [])

    # Ensure user_preferences has 6 values (one for each feature)
    if len(user_preferences) != 6:
        return jsonify({"error": "Please provide 6 values for user_preferences."}), 400

    # Get recommendations
    distances, indices = knn_model.kneighbors([user_preferences], n_neighbors=5)
    recommendations = meals_df.iloc[indices[0]]

    # Return results
    return jsonify(recommendations[['Food', 'Measure', 'Calories', 'Protein', 'Fat', 'Carbs']].to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)