#!/bin/bash

export FLASK_APP=application.py
echo "Setting FLASK_APP to:" $FLASK_APP

export FLASK_ENV=development
echo "Setting FLASK_ENV to:" $FLASK_ENV

export DATABASE_URL="postgres://oydqwwvmfkwawe:3cb6a5a0d105c929fc4695244b25dfbb1458befabddb2b3c85d254549213b656@ec2-107-21-125-209.compute-1.amazonaws.com:5432/dcmoh597l9rarv"
echo "Setting DATABSE_URL to:" $DATABASE_URL


