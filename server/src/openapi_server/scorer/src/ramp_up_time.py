# Learned the os.walk() method from https://www.tutorialspoint.com/python/os_walk.htm
# Learned the os.listdir() method from https://www.tutorialspoint.com/python/os_listdir.htm#:~:text=Python%20os.listdir%20%28%29%20Method%201%20Description.%20Python%20method,example%20shows%20the%20usage%20of%20listdir%20%28%29%20method.
# Learned the os.path.exists() method from https://pythontect.com/python-os-path-exists-method-tutorial/
# Learned the os.path.splitext() method from https://docs.python.org/3/library/os.path.html
# Learned the detect method of chardet from https://chardet.readthedocs.io/en/latest/usage.html#example-using-the-detect-function

from logging import log
import logging
import os
import chardet
from openapi_server.scorer.src.file_parser import file_parser


def ramp_up_time(dir_check):
    if os.path.exists(dir_check) == False:
        return -1

    logging.info('The current module directory is not None, continue to evaluate the ramp-up time score of the current module.')

    #  Evaluate the ramp up time score of moddule based on three dimensions: number_lines,Documentation, and inclusion of use case example, also set up the counters.
  
    num_codes = 0
    num_doc = 0
    num_case = 0
    num_https = 0
    usage_time = 0
    paths = os.listdir(dir_check)
    if len(paths) == 0:
        logging.info('There is no any file in current module path, returning value of -1')
        return -1
    input_dir = ''
    logging.info('Now finding the readme file directory and read the file to get info for the scoring, i.e. line_in_readme, num_https, num_case.')

    for curr_path in paths:
        if 'README' in curr_path or 'readme' in curr_path or 'ReadMe' in curr_path or "Readme" in curr_path:
            input_dir = dir_check + '/' + curr_path
    line_in_readme = 0

    if os.path.exists(input_dir):
        try:
            temp2= open(input_dir,'rb')
            temp_data2 = temp2.read()
            temp_check2 = chardet.detect(temp_data2)
            #read_data = temp_data2.decode(temp_check2['encoding'],'ignore').encode('utf-8')
            #read_readme = open(input_dir,encoding = 'utf-8')
            read_data = open(input_dir,encoding = temp_check2['encoding'])
            # read_readme = open(input_dir,encoding = 'utf-8')
            for curr_line in read_data:
                    line_in_readme += 1
                    if '```bash' in curr_line:
                        num_case += 1
                    if '```' in curr_line:
                        num_case += 1
                        usage_time += 1
                    if 'https' in curr_line:
                        num_https += 1
        except:
            logging.info('Reading error of the current readme file occurs.')
            if line_in_readme == 0:
                line_in_readme = 1
            handle_error = 1
    else:
        num_case = 0
        line_in_readme = 0

    num_case = num_case - usage_time // 2
    num_doc = line_in_readme
    logging.info('Read info of readme file done.')

   # Check how many total lines of js code in this module

    logging.info('Now getting all js files in the module and use file parser to get all info of the all files.')
    js_files_container = []

    for curr_folder, sub_folders, curr_files in os.walk(dir_check):
        for curr_file in curr_files:
            if'.js' in os.path.splitext(curr_file):
                js_files_container.append((str(curr_folder)) + '/' + curr_file)

    total_statistics = {'num_lines':0,'num_comments':0,'num_functions':0,'num_class':0,'num_bytes':0}

    for curr_js_file in js_files_container:
        curr_file_data = file_parser(curr_js_file)
        for per_data_pos in curr_file_data:
            total_statistics[per_data_pos] = curr_file_data[per_data_pos] + total_statistics[per_data_pos]

    num_codes = total_statistics['num_lines']
    num_comments = total_statistics['num_comments']

    logging.info('Getting info from all js files done')

    # Score for the documentation

    logging.info('Now calculating the score for readability of the module')
    readabilitiy_score = ((0.1)*(num_doc >= 25) +(0.1)*(num_doc>=40) + (0.2)*(num_doc>=80) + (0.1)*(num_doc>120) + 0.1 * (num_doc > 140) + 0.2 *(num_doc>180) + 0.2 *(num_doc > 220)) * 100

    # Score for comments line

    logging.info('Now calculating the score for comments lines')
    score_comments = 0.15 * (num_comments>= 0 and num_comments <200) * 100 +  (num_comments / 1000 * 100) * (num_comments >= 200 and num_comments < 500) \
    + (num_comments >= 500 and num_comments < 1500) * (num_comments / 2500 * 100) + (num_comments >= 1500 and num_comments < 5000) * 0.625 * 100 \
    + (num_comments >= 5000 and num_comments < 8000) * 0.65 * 100 + (num_comments >= 8000 and num_comments < 11000) * 0.7 * 100 \
    + (num_comments >= 11000 and num_comments) * 0.75 * 100 + (num_comments >= 19000 and num_comments < 22000) *0.78 * 100 \
    + (num_comments >= 22000 and num_comments < 25000) * 0.85 * 100 + (num_comments >= 25000 and num_comments < 29000) *0.88 * 100 \
    + (num_comments >= 29000 and num_comments < 31000) * 0.92 * 100 + (num_comments > 31000) * 100

    # Score for usage cases

    logging.info('Now calculating the usage cases score')
    case_score = 0.1 * 100 * (num_case == 0) + 0.15 * 100 * (num_case == 1) + 0.3 * 100 * (num_case == 2) + 0.4 * 100 * (num_case == 3) \
    + (num_case == 4) * 0.5 * 100 + ( num_case >= 10 and num_case < 20) * 0.75 * 100  \
    + (num_case >= 20 and num_case < 30) *0.8 * 100 + (num_case >= 30 and num_case < 70) * 0.9 * 100 + (num_case >= 70) * 100 \
    + (num_case > 4 and num_case < 10) * 0.65*100

    logging.info('Now calculating the bonus score')
    bonus_score = num_https * 0.75

    logging.info('Now calculating the total ramp-up time score')
    ramp_up_time_score = (readabilitiy_score + score_comments + case_score + bonus_score) / 3

    if ramp_up_time_score > 100:
       logging.info('The total ramp-up time score of the current module is greater than 100, it will be set to at most 100')
       ramp_up_time_score = 100


    return ramp_up_time_score /100



if __name__ == "__main__":
    print('test')
    # # print(ramp_up_time(the module dir))
    # # Below are modules samples given on the Brightspace
    # print('-----------------------------------------')
    # print(ramp_up_time('cloudinary_npm-master'))
    # print('-----------------------------------------')
    # print(ramp_up_time('express-master'))
    # print('-----------------------------------------')
    # print(ramp_up_time('nodist-master'))
    # print('-----------------------------------------')
    # print(ramp_up_time('lodash-master'))
    # print('-----------------------------------------')
    # print(ramp_up_time('browserify-master'))
    # print('-----------------------------------------')


