from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
import datetime

app = Flask(__name__)

model = pickle.load(open("GaussianCatBoost.pkl", "rb"))

normalCount = 0
anormalCount = 0


@app.route('/predict', methods=['POST'])
def predict():
    """
    A method that get a value as json request and time with datetime module, then response model result
    :return: model predict result
    """
    features = request.get_json(force=True)['value']
    ct = datetime.datetime.now()
    months = ct.month
    hours = ct.hour
    light = ((hours >= 7) & (hours <= 20))
    dayOfWeek = ct.weekday()
    if dayOfWeek < 5:
        weekDay = 1
    else:
        weekDay = 0
    parts = weekDay * 2 + light

    eval_value = [features, months, hours, light, dayOfWeek, weekDay, parts]

    prediction = model.predict(np.array([eval_value]).tolist()).tolist()
    response = {'prediction': prediction}

    a = -1
    for i in prediction:
        a = i

    # Set normal and anormal count for report
    if a == 0:
        global normalCount
        normalCount += 1
    else:
        global anormalCount
        anormalCount += 1

    f = open("newValue.txt", "a")
    f.write("%s, %s\n" % (ct, a))
    f.close()

    return jsonify(response)


@app.route('/report', methods=['GET'])
def report():
    """
    A method that create a report by using global variables
    :return: summary of report
    """
    read_file = pd.read_csv(r'newValue.txt')
    read_file.to_csv(r'newDataset.csv', index=None)
    string = "Number of normal values:" + str(normalCount) + "\nNumber of anormal values:" + str(anormalCount)
    return string


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# Invoke-RestMethod -Method POST -Uri http://127.0.0.1:5000/predict -Body '{"features":69.880835}'
