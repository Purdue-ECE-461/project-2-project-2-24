#!/bin/bash

# Check for correct number of arguments
if [ "$#" -ne 1 ]; then
    echo "You must enter exactly 1 command line argument."
    echo "Use the '-help' option to see options!"
    exit 1
fi

if [ $1 == "-help" ]; then
    echo "Use 'install' to install server, 'test' to run server tests, or 'clean' to clean install"
elif [ $1 == "install" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    pip3 install -e .
    deactivate
elif [ $1 == "start" ]; then
    source venv/bin/activate
    export $(grep -v '^#' .env | xargs -d '\n')
    python3 -m uvicorn openapi_server.main:app --host localhost --port $PORT
    deactivate
elif [ $1 == "gae_install_and_run" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    pip3 install .
    python3 -m uvicorn openapi_server.main:app --host localhost --port $PORT
    deactivate
elif [[ $1 == "test" ]]; then
    source venv/bin/activate
    > test_output.txt
    export $(grep -v '^#' .env | xargs -d '\n')
    coverage run -m pytest tests >> test_output.txt
    coverage report -m >> test_output.txt
    deactivate
elif [[ $1 == "clean" ]]; then
    echo "Cleaning install..."
    rm -r src/openapi_server/__pycache__
    rm -r .pytest_cache
    rm -r venv
    rm -r src/openapi_server.egg-info
else
    echo "Invalid command line argument"
    echo "Use the '-help' option to see options!"
    exit 1
fi

exit 0