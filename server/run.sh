#!/bin/bash

# Check for correct number of arguments
if [ "$#" -ne 1 ]; then
    echo "You must enter exactly 1 command line argument."
    echo "Use the '-help' option to see options!"
    exit 1
fi

if [ $1 == "-help" ]; then
    echo "Use 'install' to install, 'test' to run tests, or 'clean' to clean install"
elif [ $1 == "install" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip3 install --upgrade pip
    pip3 install -e ./openapi_server
    deactivate
elif [[ $1 == "test" ]]; then
    source venv/bin/activate
    > test_output.txt
    source openapi_server/.env
    coverage run -m pytest openapi_server/test/test_database.py >> test_output.txt
    coverage report -m >> test_output.txt
    # python3 print_tests.py test_output.txt
    deactivate
elif [[ $1 == "clean" ]]; then
    echo "Cleaning install..."
    rm -r openapi_server/__pycache__
    rm -r openapi_server/.pytest_cache
    rm -r venv
else
    echo "Invalid command line argument"
    echo "Use the '-help' option to see options!"
    exit 1
fi

exit 0
