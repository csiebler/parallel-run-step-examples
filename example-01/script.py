import os
import glob
import json
import argparse
import numpy as np
import pandas as pd
import joblib
import tempfile
from zipfile import ZipFile
import uuid 

from azureml.core import Run

current_run = None
temp_path = None
model_path = None
forecast_horizon = None

def init():
    print("Started script.py by running init()")

    parser = argparse.ArgumentParser()
    parser.add_argument('--forecast_horizon', type=str, help='Forecast horizon')
    parser.add_argument('--model_path', type=str, help='Model directory')
    args, _ = parser.parse_known_args()

    # Can be used to log metrics into the run
    global current_run
    current_run = Run.get_context()

    print(f'Arguments: {args}')
    print(f'Forecast horizon: {args.forecast_horizon}')
    print(f'Model path: {args.model_path}')

    global model_path, forecast_horizon
    model_path = args.model_path
    forecast_horizon = args.forecast_horizon

    global temp_path
    temp_path = tempfile.mkdtemp(dir='/tmp')

def run(mini_batch):
    print(f'Input minibatch shape: {mini_batch.shape}')
    print(f'Input to script.py: \n{mini_batch}')

    output_array = []
    try:
        for index, row in mini_batch.iterrows():

            # Query required data from time-series database for the row
            # Pseudocode:
            #  df = SELECT * FROM table WHERE code=row['code'] AND company=row['company']
            #  model = forecaster.fit(df)
            #  forecast model.predict(forecast_horizon)
            #  forecast.save(/tmp/models/model1.something)

            model_filename = f'model_{row["code"]}_{row["company"]}.txt'
            with open(os.path.join(temp_path, model_filename), 'w') as f:
                f.write('This should actually be a real model\n')

            # Append to output array/dataframe for telling AML that we processed the row
            output_array.append(f'Finished processing row: {row}, saved to {model_filename}')
    except Exception as e:
        print(f'An error occured: {str(e)}')

    # Package all models from minibatch into a zip file
    model_zip_filename = os.path.join(model_path, str(uuid.uuid4()) + '.zip')
    print(f'Will create model zip under {model_zip_filename}')
    with ZipFile(model_zip_filename, 'w') as zip_file:
        for f in glob.glob(os.path.join(temp_path, "*.txt")):
            zip_file.write(f)

    return output_array

if __name__ == "__main__":
    # Pseudocode, but good if you want to test it via:
    # python script.py --forecast_horizon 4
    some_test_mini_batch = pd.DataFrame(...)
    init()
    run(some_test_mini_batch)
    assert(...)