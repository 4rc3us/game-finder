#!/bin/env bash

# first check if python is installed
if ! command -v python &> /dev/null
then
    echo "Python could not be found"
    exit
fi

# check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "Pip could not be found"
    exit
fi

# check if virtualenv is installed
if ! command -v python -m venv &> /dev/null
then
    echo "Virtualenv could not be found"
    exit
fi

# check if venv exists and create it if it doesn't and install dependencies from requirements.txt
if [ ! -d "venv" ]
then
    echo "Creating virtual environment"
    python -m venv venv
fi

# activate virtualenv
source venv/bin/activate

# install dependencies but check if requirements.txt exists and dependencies aren't installed
if [ -f "requirements.txt" ]
then
    echo "Installing dependencies from requirements.txt"
    pip install -r requirements.txt
else
    echo "requirements.txt not found"
fi

# start the app (its a django app)
echo "Starting app"