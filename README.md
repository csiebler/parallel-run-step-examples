# parallel-run-step-examples

A short example for training and forecasting many models on e.g., time-series data for multiple SKUs, etc. This uses `ParallelRunStep` on Azure Machine Learning.

This repo shows an example for:

* Train many models in parallel, then store packs of models in zip files on Azure Blob or ADLSg2 in a pre-defined folder, see [`example-01\train_store.ipynb`](example-01\train_store.ipynb)
* Optionally register the zip files as a model in Azure Machine Learning, see [`example-01/train_store_register.ipynb`](example-01/train_store_register.ipynb)