# Overview

## Dependencies
In order to properly build/run this project, you will need Python 3.6 or newer! To install all relevant modules for the project, simply run:
```
$chmod +rwx run
$./run install
```
If all packages are properly installed, you shall get an output stating "Successfully installed all dependencies!" In addition to the module installation, the user will also need to provide an .env file in the project directory.

### Configuring the .env
Your .env file should include the following enviornmental variables:

```
GITHUB_TOKEN=______ 
LOGGING_LEVEL=______
LOG_FILE=________
```
$GITHUB_TOKEN is the developer token generated on your github, $LOGGING_LEVEL 0 results in no output, 1 results in info, 2 results in verbose debugging output. Finally, $LOG_FILE is the file in which the logging information is outputted to (NOTE: $LOGGING_LEVEL=2 may generate a very large file!)

# Usage
In order to run the program you first must setup the dependencies (see "Dependencies"). After the modules are successfully installed, use the following command:
```
$./run URL_FILE
```
Where URL_FILE is the name of a file containing URL's to npm modules (either npmjs.com or github.com urls are accepted). The program will output a list of ranked npm modules based on various metric calculations to stdout and return 0 if the program terminates successfully. 

In addition to running the program normally, the test suite can be activated by running the following script:
```
$./run test
```
which will allow the user to get a test coverage of the system.
