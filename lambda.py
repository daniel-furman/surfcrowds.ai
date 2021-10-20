from sklearn.externals import joblib
import pandas as pd
import json
model_gbr = joblib.load('gbr-surfai.pkl')
model_rfr = joblib.load('rfr-surfai.pkl')

def lambda_handler(event, context):
    # read in the request body as the event dict
    if "body" in event:
        event = event["body"]

        if event is not None:
            event = json.loads(event)
        else:
            event = {}
    if "Minimum Wave Height (ft)" in event:
        new_row = { "Minimum Wave Height (ft)": event["Minimum Wave Height (ft)"],
                    "Maximum Wave Height (ft)": event["Maximum Wave Height (ft)"],
                    "Day of Week (0-6 | Mon-Sun)": event["Day of Week (0-6 | Mon-Sun)"],
                    "Holiday (0/1 | No/Yes)": event["Holiday (0/1 | No/Yes)"] }

        new_x = pd.DataFrame.from_dict(new_row, orient = "index").transpose()
        prediction_gbr = model_gbr.predict(new_x)[0]
        prediction_rfr = model_rfr.predict(new_x)[0]
        prediction_final = str((prediction_gbr+prediction_rfr)/2)


        return { "body": "Prediction " + prediction_final }
    return { "body": "No parameters" }
