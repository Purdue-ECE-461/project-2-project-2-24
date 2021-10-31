# Learned the os.walk() method from https://www.tutorialspoint.com/python/os_walk.htm
# Learned the .lower() method from https://www.tutorialspoint.com/python/string_lower.htm#:~:text=Python%20String%20lower%20%28%29%20Method%201%20Description.%20Python,example%20shows%20the%20usage%20of%20lower%20%28%29%20method.
# Learned the os.path.exists() method from https://pythontect.com/python-os-path-exists-method-tutorial/
# Learned the os.path.splitext() method from https://docs.python.org/3/library/os.path.html
# learned the sys.getsizeof() method from https://docs.python.org/3/library/sys.html
# Also learned info and use of UnicodeEncodeError from https://wiki.python.org/moin/UnicodeDecodeError
# Learned the detect method of chardet from https://chardet.readthedocs.io/en/latest/usage.html#example-using-the-detect-function

import sys # pragma: no cover
import os # pragma: no cover
import logging # pragma: no cover
import chardet # pragma: no cover

def correctness(module_loc):
    logging.info("CORRECTNESS: starting calculations...")

    if os.path.exists(module_loc) == False:
        return -1

    if len(os.listdir(module_loc)) == 0:
        #print('1')
        return -1


    # Set up the counters for counting the info that are needed in calculating the total correctness score
    num_bugs_corrected = 0
    num_lines_log = 0
    num_test_files = 0
    test_size = 0

    # Getting any logging related files to the logging_file_container and examine the the files to extract needed info
    loggings_files_container = []

    for curr_folder, sub_folders, curr_files in os.walk(module_loc):
        for curr_file in curr_files:
            if ('.log' in (os.path.splitext(curr_file))[1].lower()) \
                    or ('log' in curr_file.lower()) or ('history' in curr_file.lower())\
                    or('security' in curr_file.lower()) or('readme' in curr_file.lower()):
                loggings_files_container.append((str(curr_folder)) + '/' + curr_file)
            if 'test' in curr_folder.lower():
                for file in sub_folders:
                    test_size = test_size + sys.getsizeof(file)

    logging.debug ('The test files size is calculated and the logging files are contained in the container')

    test_size_score = (0.1 * (test_size > 100) + 0.3* (test_size > 300) + 0.4 * (test_size>1000) + 0.2 * (test_size > 5000) ) * 25 # total 25 possible

    logging.debug('The test size score is calculated, now examining the logging files to get any info needed')

    # Extract info needed from the logging files, the file must be readable by decoding of utf-8 while parsing it, otherwise skipping it

    for logging_file in loggings_files_container:
        if '.png' in logging_file or '.jpg' in logging_file:
            logging.debug('The current that will be read is a png or jpg file, pass')
            continue
        try:
            temp2= open(logging_file,'rb')
            temp_data2 = temp2.read()
            temp_check2 = chardet.detect(temp_data2)
            curr_data = open(logging_file,encoding = temp_check2['encoding'])
            #curr_data = open(logging_file, encoding='UTF-8')
            for per_line in curr_data:
                if per_line != '\n':
                    num_lines_log += 1
                    if 'fix' in per_line or 'Fix' in per_line or 'FIX' in per_line:
                        num_bugs_corrected += 1
            logging.debug('The number of bugs corrected are calculated')
        except UnicodeDecodeError:
            print("Attempted to decode non UTF-8 file, skipping...")
            logging.debug('Attempted to decode non UTF-8 file, skipping...')

    # Now calculating the log_score
    # total 50 possible

    log_score = (num_lines_log < 10) * 0.25 * 50 + (num_lines_log >= 10 and num_lines_log < 20) * 0.3 * 50 + (num_lines_log >= 20 and num_lines_log < 40) \
    * 0.35 * 50 + (num_lines_log >= 40 and num_lines_log < 50) * 0.45 * 50 + (num_lines_log >= 50 and num_lines_log < 100) * 0.55 * 50 \
    + (num_lines_log >= 100 and num_lines_log < 150) * 0.65 * 50 * (num_lines_log >= 150 and num_lines_log < 175) * 0.75 * 50 \
    + (num_lines_log >= 175 and num_lines_log < 220) * 0.85 * 50 + (num_lines_log >= 220 and num_lines_log < 350) * 0.90 * 50 \
    + (num_lines_log >= 350) * 50

    logging.debug('log_score calculation done')

    # Now calculating the bugs_corrected_score, total 25 possible

    bugs_corrected_score = (num_bugs_corrected <= 10) * 25 * 0.4 + (num_bugs_corrected <= 100 and num_bugs_corrected > 40) * 25 * 0.6 \
    + (num_bugs_corrected >= 100 and num_bugs_corrected < 200) * 25 * 0.65 + (num_bugs_corrected >= 200 and num_bugs_corrected < 300) * 25 * 0.70 \
    + (num_bugs_corrected >= 300 and num_bugs_corrected < 400) * 25 * 0.72 + (num_bugs_corrected >= 400 and num_bugs_corrected < 600) * 25 * 0.73 \
    + (num_bugs_corrected >= 600 and num_bugs_corrected < 800) * 25 * 0.74 + (num_bugs_corrected >= 800 and num_bugs_corrected < 1000) * 25 * 0.75 \
    + (num_bugs_corrected >= 1000 and num_bugs_corrected < 1200) * 25 * 0.80 + (num_bugs_corrected >= 1200 and num_bugs_corrected < 1400) * 25 * 0.85 \
    + (num_bugs_corrected >= 1400 and num_bugs_corrected < 1800) * 25 * 0.9 + (num_bugs_corrected >= 1800 and num_bugs_corrected < 2100) *  25 * 0.95 \
    + (num_bugs_corrected >= 2100) * 25

    logging.debug('bug_corrected_score calculation done')

    # Calculating the balancer, if possible
    balancer = 0
    if test_size == 0 and num_lines_log > 50: balancer = 0.15
    logging.debug('balancer calculated')

    #Calculating the total correctness score, if the score is over 1, reset it to 1

    total_correctness_score = bugs_corrected_score + log_score + test_size_score
    result_score = total_correctness_score / 100 + balancer

    if result_score > 1: result_score = 1

    logging.debug('final total correctness calculated')

    return result_score


if __name__ == "__main__":
    print('test')
    # print('Now testing the samples of modules......')
    # print('The percent of the correctness metric score that the module should have is:', correctness('cloudinary_npm-master'))
    # print('The percent of the correctness metric score that the module should have is:', correctness('express-master'))
    # print('The percent of the correctness metric score that the module should have is:', correctness('nodist-master'))
    # print('The percent of the correctness metric score that the module should have is:', correctness('lodash-master'))
    # print('The percent of the correctness metric score that the module should have is:', correctness('browserify-master'))


