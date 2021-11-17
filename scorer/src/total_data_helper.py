# Use following as guides: 
# License:  http://www.gnu.org/licenses/gpl-faq.html#AllCompatibility
# License:  https://www.whitesourcesoftware.com/resources/blog/license-compatibility/
# Learned the os.walk() method from https://www.tutorialspoint.com/python/os_walk.htm
# Learned the .lower() method from https://www.tutorialspoint.com/python/string_lower.htm#:~:text=Python%20String%20lower%20%28%29%20Method%201%20Description.%20Python,example%20shows%20the%20usage%20of%20lower%20%28%29%20method.
# Learned the os.path.exists() method from https://pythontect.com/python-os-path-exists-method-tutorial/
# Learned the os.path.splitext() method from https://docs.python.org/3/library/os.path.html
# learned the sys.getsizeof() method from https://docs.python.org/3/library/sys.html
# Also learned info and use of UnicodeEncodeError from https://wiki.python.org/moin/UnicodeDecodeError
# Learned the detect method of chardet from https://chardet.readthedocs.io/en/latest/usage.html#example-using-the-detect-function

# This is a helper function to help to give the total statistics of all files in the current module that is being evaluated
# To use the helper, please input the current directory name of the current module, the output will give you a dictionary
# with 7 features.
# The return value is like:
# {'num_lines': 181359, 'num_comments': 27727, 'num_functions': 9514, 'num_class': 385, 'num_bytes': 250221, 'num_lines_README': 44,'license_score': 1} (from the testing example)
# Please include: from total_data_helper import total_data_helper     in your metric function.
# And directly call total_data_helper (curr_module_dir) in your metric function
#
from logging import log # pragma: no cover
import os # pragma: no cover
import logging # pragma: no cover
from file_parser import file_parser # pragma: no cover
import chardet # pragma: no cover


def get_license_helper(curr_line):
    license_type = ''


     
    if "MIT" in curr_line or "Creative Commons" in curr_line or "X11" in curr_line or "Expat" in curr_line: license_type = 'MIT'
    elif "BSD-new" in curr_line: license_type = 'BSD-new'
    elif "Apache 2.0" in curr_line: license_type = 'Apache 2.0'
    elif "LGPLv2.1" in curr_line: license_type = 'LGPLv2.1'
    elif "GPLv2" in curr_line: license_type = 'GPLv2'
    elif "GPLv2+" in curr_line: license_type = 'GPLv2+'
    elif "GPLv3" in curr_line: license_type = 'GPLv3'
    elif "LGPLv2.1+" in curr_line: license_type = 'LGPLv2.1+'
    elif "LGPLv3" in curr_line: license_type = 'LGPLv3'
    else: license_type = 'NA'
    return license_type


def total_data_helper(curr_module_dir):
    # Please include: from total_data_helper import total_data_helper     in your metric function.

    if os.path.exists(curr_module_dir) == False:
        return {'num_lines': 1, 'num_comments': 0, 'num_functions': 0, 'num_class': 0, 'num_bytes': 0, 'num_lines_README': 0, 'num_https':0,'license':'None'}

    num_doc = 0
    line_in_readme = 0
    num_codes = 0
    num_doc = 0
    num_case = 0
    num_https = 0
    usage_time = 0
    license_type = 'NA'
    paths = os.listdir(curr_module_dir)

    license_file_container = []
    try:
        for file in paths:
            if 'license'.upper() in file or 'LICENSE'.lower() in file:
                license_file_container.append(file)

        for license_file in license_file_container:

            license_dir = curr_module_dir + '/' + license_file
            temp = open(license_dir, 'rb')
            temp_data = temp.read()
            temp_check = chardet.detect(temp_data)
            license_data = open(license_dir, encoding=temp_check['encoding'])

            for curr_line in license_data:
                if 'https' in curr_line: num_https += 1
                if (license_type == 'NA'): license_type = get_license_helper(curr_line)
  
    except:license_type = 'NA'

            

    input_dir = ''
    for curr_path in paths:
        if 'README' in curr_path or 'readme' in curr_path or 'ReadMe' in curr_path or "Readme" in curr_path:
            input_dir = curr_module_dir + '/' + curr_path
    line_in_readme = 0


    if os.path.exists(input_dir):
        try:  
            temp2= open(input_dir,'rb')
            temp_data2 = temp2.read()
            temp_check2 = chardet.detect(temp_data2)
            read_readme = open(input_dir,encoding = temp_check2['encoding'])

            for curr_line in read_readme:

                line_in_readme += 1
                if '```bash' in curr_line:
                    num_case += 1
                if '```' in curr_line:
                    num_case += 1
                    usage_time += 1

                if 'https' in curr_line:
                    num_https += 1

                if (license_type == 'NA'):
                    license_type = get_license_helper(curr_line)  
        except:  
            logging.info('There is no readme file or the decoding could not be handled.')

    else:
        num_case = 0
        line_in_readme = 0
    num_case = num_case - usage_time // 2
    num_doc = line_in_readme
    
    logging.info('The analysis for Readme done.')
    # Check how many total lines of js code in this module

    js_files_container = []

    for curr_folder, sub_folders, curr_files in os.walk(curr_module_dir):
        for curr_file in curr_files:
            if '.js' in os.path.splitext(curr_file):
                js_files_container.append((str(curr_folder)) + '/' + curr_file)
    
    logging.info('js files are stored.')

    total_statistics = {'num_lines': 0, 'num_comments': 0, 'num_functions': 0, 'num_class': 0, 'num_bytes': 0,
                        'num_lines_README': num_doc, 'num_https': num_https,'license':license_type}

    for curr_js_file in js_files_container:
        curr_file_data = file_parser(curr_js_file)
        for per_data_pos in curr_file_data:
            total_statistics[per_data_pos] = curr_file_data[per_data_pos] + total_statistics[per_data_pos]
    logging.info('js files read and anlysis done the total statistic is calculated.')

    return total_statistics
