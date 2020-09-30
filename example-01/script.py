import os
import glob
import json
import argparse
import numpy as np
import pandas as pd
import joblib

from azureml.core import Run

current_run = None

def init():
    print("Started script.py by running init()")

    parser = argparse.ArgumentParser()
    parser.add_argument('--forecast_horizon', type=str, help='Forecast horizon')
    args, _ = parser.parse_known_args()

    # Can be used to log metrics into the run
    global current_run
    current_run = Run.get_context()

    print(f'Arguments: {args}')
    print(f'Forecast horizon: {args.forecast_horizon}')

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
            #  forecast.save(...)

            print(f'Finished processing row: {row}')

            # Append to output array/dataframe for telling AML that we processed the row
            output_array.append(f'Finished processing row: {row}')
    except Exception as e:
        print(f'An error occured: {str(e)}')
    return output_array

if __name__ == "__main__":
    # Pseudocode, but good if you want to test it via:
    # python script.py --forecast_horizon 4
    some_test_mini_batch = pd.DataFrame(...)
    init()
    run(some_test_mini_batch)
    assert(...)