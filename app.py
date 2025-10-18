import os 
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import pandas as pd 
from src.Car.loggers import logger
from src.Car.pipelines.prediction_pipeline import PredictionPipeline

load_dotenv()

app=Flask(__name__)
app.secret_key= os.getenv("Seceret_key","Super-seceret-key")

# instantiate prediction pipeline (loads preprocessor and model)
predictor=PredictionPipeline(config_path="config/config.yml")

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
   # global predictor 
    try:
        # lazy load prediction pipeline
        ''' if predictor is None:
            print("Loading Prediction pipeline....")
            predictor=PredictionPipeline(config_path="config/config.yml")
            print("prediction pipeline loaded")'''

        # gather form data
        data={
            "name":request.form.get("name"),
            "year":int(request.form.get("year")),
            "km_driven":float(request.form.get("km_driven")),
            "fuel":request.form.get("Fuel"),
            "transmission":request.form.get("transmission"),
            "owner":request.form.get("owner")
        }
        df=pd.DataFrame([data])
        preds=predictor.predict(df)
        price=round(float(preds[0]),2)

        return render_template("prediction.html",predicted_price=price)
    
    except Exception as e:
        logger.exception("Prediction Error")
        flash("An Error Occured during prediction. Ensure model is trained and artifacts exist."," Danger")
        return redirect(url_for("index"))
    

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)