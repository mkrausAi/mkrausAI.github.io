import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request
import tensorflow as tf
import os

app = Flask(__name__)

# Load the best model
circular_model_fin = tf.keras.models.load_model("DL_files/circular_model_fin.h5")
RHSSHS_model_fin = tf.keras.models.load_model("DL_files/RHSSHS_model_fin.h5")
IH_model_fin = tf.keras.models.load_model("DL_files/IH_model_fin.h5")

scaler_circ_x = joblib.load("DL_files/scaler_circ_x.joblib")
scaler_circ_s = joblib.load("DL_files/scaler_circ_s.joblib")
scaler_rhsshs_x = joblib.load("DL_files/scaler_rhsshs_x.joblib")
scaler_rhsshs_s = joblib.load("DL_files/scaler_rhsshs_s.joblib")
scaler_ih_x = joblib.load("DL_files/scaler_ih_x.joblib")
scaler_ih_s = joblib.load("DL_files/scaler_ih_s.joblib") 


def predict_s(X_html,keras_model,X_scaler,s_scaler):
    """
    Predicts the overstrength of a profil using the trained NN model.

    Args:
    X_html (pandas DataFrame): The (unscaled) input data from the Flask app form as a pandas DataFrame.
    keras_model (keras.models.Sequential): The Keras model to use for making predictions.
    X_scaler (sklearn.preprocessing.StandardScaler): The scaler used to preprocess the input data.
    s_scaler (sklearn.preprocessing.StandardScaler): The scaler used to preprocess the output data.

    Returns:
    postprocessed_prediction (numpy.ndarray): The predicted overstrength (corrctly scaled) as a numpy array.
    """

    # Preprocess the input data
    X_scaled = X_scaler.transform(X_html)
    
    # Use the model to make a prediction
    prediction_unscaled = keras_model.predict(X_scaled)
    
    # Postprocess the prediction
    postprocessed_prediction = s_scaler.inverse_transform(prediction_unscaled)

    return postprocessed_prediction


@app.route('/predict_circ', methods=['POST'])
def predict_circ():
    error = None  # initialize error message to None

    try:
        data = request.json
        df = pd.DataFrame(data, index=[0])
    
        # Pass the input values to the trained model to get the predicted values
        s_circ_pred = predict_s(df.values, circular_model_fin, scaler_circ_x, scaler_circ_s)
            
    except:
        error = "DL model execution error. Correct your inputs."

    # Render the response HTML
    return render_template('input.html', s_circ_pred=s_circ_pred, error=error,)

@app.route('/predict_RHSSHS', methods=['POST'])
def predict_rhsshs():
    error = None  # initialize error message to None

    try:
        data_rhsshs = request.json
        df_rhsshs = pd.DataFrame(data_rhsshs, index=[0])
    
        # Pass the input values to the trained model to get the predicted values
        s_rhsshs_pred = predict_s(df_rhsshs.values, RHSSHS_model_fin, scaler_rhsshs_x, scaler_rhsshs_s)
    
    except:
        error = "DL model execution error. Correct your inputs."

    # Render the response HTML
    return render_template('input.html', s_rhsshs_pred=s_rhsshs_pred, error=error,)

@app.route('/predict_ih', methods=['POST'])
def predict_ih():
    error = None  # initialize error message to None

    try:
        data_ih = request.json
        df_ih = pd.DataFrame(data_ih, index=[0])
    
        # Pass the input values to the trained model to get the predicted values
        s_ih_pred = predict_s(df_ih.values, IH_model_fin, scaler_ih_x, scaler_ih_s)
            
    except:
        error = "DL model execution error. Correct your inputs."

    # Render the response HTML
    return render_template('input.html', s_ih_pred=s_ih_pred, error=error,)


