import joblib
import pandas as pd
from flask import Flask, jsonify, request
import tensorflow as tf
import os

app = Flask(__name__)

num_layers = 8
nodes_per_layer = 64
latent_dim = 3
dropout_rate = 5

# Load the best model
circular_model_fin = tf.keras.models.load_model(os.path.join('DL_files', 
                                                             f'circ_lay_{str(num_layers)}_nod_{str(nodes_per_layer)}_lat_{str(latent_dim)}_dr_{str(dropout_rate)}'))
RHSSHS_model_fin = tf.keras.models.load_model(os.path.join('DL_files',
                        f'RHSSHS_lay_{str(num_layers)}_nod_{str(nodes_per_layer)}_lat_{str(latent_dim)}_dr_{str(dropout_rate)}'))
IH_model_fin = tf.keras.models.load_model(os.path.join('DL_files',
                        f'IH_lay_{str(num_layers)}_nod_{str(nodes_per_layer)}_lat_{str(latent_dim)}_dr_{str(dropout_rate)}'))

scaler_circ_x = joblib.load("DL_files/scaler_circ_x.joblib")
scaler_circ_s = joblib.load("DL_files/scaler_circ_s.joblib")
scaler_rhsshs_x = joblib.load("DL_files/scaler_rhsshs_x.joblib")
scaler_rhsshs_s = joblib.load("DL_files/scaler_rhsshs_s.joblib")
scaler_ih_x = joblib.load("DL_files/scaler_ih_x.joblib")
scaler_ih_s = joblib.load("DL_files/scaler_ih_s.joblib") 


@app.route("/", methods=["POST"])
def index():
    data = request.json
    df = pd.DataFrame(data, index=[0])
    prediction = model.predict(transformer.transform(df))
    predicted_price = expm1(prediction.flatten()[0])
    return jsonify({"price": str(predicted_price)})




# Predict on training, validation and test set
train_preds_circ = scaler_circ_s.inverse_transform(circular_model_fin.predict(x_circular_train))
train_preds_rhsshs = scaler_rhsshs_s.inverse_transform(RHSSHS_model_fin.predict(x_rhsshs_train))
train_preds_ih = scaler_ih_s.inverse_transform(IH_model_fin.predict(x_ih_train))

val_preds_circ = scaler_circ_s.inverse_transform(circular_model_fin.predict(x_circular_val))
val_preds_rhsshs = scaler_rhsshs_s.inverse_transform(RHSSHS_model_fin.predict(x_rhsshs_val))
val_preds_ih = scaler_ih_s.inverse_transform(IH_model_fin.predict(x_ih_val))

test_preds_circ = scaler_circ_s.inverse_transform(circular_model_fin.predict(x_circular_test))
test_preds_rhsshs = scaler_rhsshs_s.inverse_transform(RHSSHS_model_fin.predict(x_rhsshs_test))
test_preds_ih = scaler_ih_s.inverse_transform(IH_model_fin.predict(x_ih_test))
  
# Evaluate predictions
mae_circular_train = abs(scaler_circ_s.inverse_transform(s_circular_train)- scaler_circ_s.inverse_transform(train_preds_circ))
mae_circular_val = abs(scaler_circ_s.inverse_transform(s_circular_val)- scaler_circ_s.inverse_transform(val_preds_circ))
mae_circular_test = abs(scaler_circ_s.inverse_transform(s_circular_test)- scaler_circ_s.inverse_transform(test_preds_circ))

mae_rhsshs_train = abs(scaler_rhsshs_s.inverse_transform(s_rhsshs_train)- scaler_rhsshs_s.inverse_transform(train_preds_rhsshs))
mae_rhsshs_val = abs(scaler_rhsshs_s.inverse_transform(s_rhsshs_val)- scaler_rhsshs_s.inverse_transform(val_preds_rhsshs))
mae_rhsshs_test = abs(scaler_rhsshs_s.inverse_transform(s_rhsshs_test)- scaler_rhsshs_s.inverse_transform(test_preds_rhsshs))

mae_ih_train = abs(scaler_ih_s.inverse_transform(s_ih_train)- scaler_ih_s.inverse_transform(train_preds_ih))
mae_ih_val = abs(scaler_ih_s.inverse_transform(s_ih_val)- scaler_ih_s.inverse_transform(val_preds_ih))
mae_ih_test = abs(scaler_ih_s.inverse_transform(s_ih_test)- scaler_ih_s.inverse_transform(test_preds_ih))

