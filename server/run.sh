#!/bin/sh

# Check for correct number of arguments
if [ "$#" -ne 1 ]; then
    echo "You must enter exactly 1 command line argument."
    echo "Use the '-help' option to see options!"
    exit 1
fi

if [ $1 == "-help" ]; then
    echo "Use 'install' to install, 'test' to run tests, or 'clean' to clean install"
elif [ $1 == "install" ]; then
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -e ./openapi_server
    deactivate
elif [[ $1 == "test" ]]; then
    source venv/bin/activate
    > test_output.txt
    coverage run -m pytest test.py >> test_output.txt
    coverage report -m >> test_output.txt
    python3 print_tests.py test_output.txt
    deactivate
elif [[ $1 == "clean" ]]; then
    echo "Cleaning install..."
    rm -r __pycache__
    rm -r .pytest_cache
    rm -r bin
    rm -r include
    rm -r lib
    rm -r share
    rm pyvenv.cfg
else
    echo "Invalid command line argument"
    echo "Use the '-help' option to see options!"
    exit 1
fi

exit 0