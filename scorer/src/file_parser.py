def file_parser(js_file):
    
    # New update: now it is the most great version that can decode any file encoded by different standards.
    # Learned the os.walk() method from https://www.tutorialspoint.com/python/os_walk.htm
    # Learned the .lower() method from https://www.tutorialspoint.com/python/string_lower.htm#:~:text=Python%20String%20lower%20%28%29%20Method%201%20Description.%20Python,example%20shows%20the%20usage%20of%20lower%20%28%29%20method.
    # Learned the os.path.exists() method from https://pythontect.com/python-os-path-exists-method-tutorial/
    # Learned the os.path.splitext() method from https://docs.python.org/3/library/os.path.html
    # learned the sys.getsizeof() method from https://docs.python.org/3/library/sys.html
    # Also learned info and use of UnicodeEncodeError from https://wiki.python.org/moin/UnicodeDecodeError
    # Learned the detect method of chardet from https://chardet.readthedocs.io/en/latest/usage.html#example-using-the-detect-function
   
    import chardet
    import sys
    import logging
    import os
    

    if  os.path.exists(js_file) != True:
        logging.debug('The current file that is being read is not a valid directory.')
        return {'num_lines':1,'num_comments':0,'num_functions':0,'num_class':0,'num_bytes':0}
    
    if  os.path.isfile(js_file) != True:
        logging.debug('The current file that is being read is not a valid directory.')
        return {'num_lines':1,'num_comments':0,'num_functions':0,'num_class':0,'num_bytes':0}

    # Read the js file

    temp_js = open(js_file,'rb')
    temp_data = temp_js.read()
    temp_check = chardet.detect(temp_data)
    js = open(js_file,encoding = temp_check['encoding'])
    

    # Set up the logging setting

    
    read_file_bytes = sys.getsizeof(js_file)
    logging.debug('The size of the current file %s is %d bytes.'% (js_file, read_file_bytes))


    # Set a counter for counting how many lines of code are there, and set the the counter for counting
    # how many comments of lines are there in the JAVASCRIPT file, also should set the flag for indicating
    # if the current line is still inside the comments, also set the counter for counting how many classes
    # are crated

    line_counter = 0
    comment_counter = 0
    function_counter = 0
    comment_done_flag = 1
    class_counter = 0

    # Read the js file line-by-line, if the current line is empty line without any characters,
    # Then ignore the current line, only count the lines where codes are written
    # The counter for lines of comments should also work
    try:
        for curr_line in js:           
            if curr_line != '\n':
                line_counter += 1
                if '//' in curr_line:
                    comment_counter += 1
                if comment_done_flag == 1 and 'class' in curr_line:
                    class_counter += 1
                    continue
                if comment_done_flag == 0:
                    comment_counter+= 1
                if comment_done_flag == 1 and 'function' in curr_line or 'static' in curr_line or'async' in curr_line or'restricted' in curr_line or 'public' in curr_line or 'exec' in curr_line:
                    function_counter +=1
                    continue
                if '/*' in curr_line:
                    comment_done_flag = 0
                    comment_counter += 1
                if '*/' in curr_line:
                    comment_done_flag = 1
                    comment_counter += 1
    except:
        line_counter = line_counter + 1 * (line_counter == 0)
        comment_counter = comment_counter + 1 * (comment_counter == 0)
        logging.debug('There is character that can not be decoded in current line of current file')

    statistics = {'num_lines':line_counter,'num_comments':comment_counter,'num_functions':function_counter,'num_class':class_counter,'num_bytes':read_file_bytes}
    logging.debug('The statistics of the current file %s are %s.' % (js_file, statistics))

    return statistics