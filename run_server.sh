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
    python3 -m venv server/venv
    source server/venv/bin/activate
    pip3 install --upgrade pip
    pip3 install -e server
    pip3 install pytest
    pip3 install coverage
    deactivate
elif [[ $1 == "test" ]]; then
    source server/venv/bin/activate
    > server/test_output.txt
    source server/src/openapi_server/.env
    PYTHONPATH=server/src coverage run -m pytest server/tests >> server/test_output.txt
    coverage report -m >> server/test_output.txt
    deactivate
elif [[ $1 == "clean" ]]; then
    echo "Cleaning install..."
    rm -r server/src/openapi_server/__pycache__
    rm -r server/.pytest_cache
    rm -r server/venv
else
    echo "Invalid command line argument"
    echo "Use the '-help' option to see options!"
    exit 1
fi

exit 0
