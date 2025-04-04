#!/bin/bash

# Enable Conda inside this script
source /opt/anaconda3/etc/profile.d/conda.sh

# Activate your environment
conda activate consus_bms

# Start the FastAPI app using Uvicorn
uvicorn main:app --reload
