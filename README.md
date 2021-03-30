# Rescale-Tutorial
This repo contains the python program for submitting automated simulation jobs to Rescale cloud platform using REST API. The parallelization of sequential Monte Carlo [code](https://github.com/karthikncsu/Sampling-from-high-dimensional-space) is [benchmarked](https://github.com/karthikncsu/Rescale-Tutorial/blob/main/rescale_rest_api.pdf) using automated job submissions.

### Required python packages to run the code

* numpy
* matplotlib
* tqdm
* scipy
* seaborn
* mpi4py

### Input files

Python code for [sampling from high dimensional space with complex, non-linear constraints](https://github.com/karthikncsu/Sampling-from-high-dimensional-space).

### Files
rescale_restapi.py : Contains BatchJobSubmit class for methods for uploading input files, setting and submitting jobs using REST API.

runjob_sampling_multijob.py: Code to benchmark the parallelization of sequential Monte Carlo [code](https://github.com/karthikncsu/Sampling-from-high-dimensional-space) by automating the job submissions with multiple processors using the BatchJobSubmit objects.

download_file.py, downloading_files.py: Tutorial for downloading files using REST API.
