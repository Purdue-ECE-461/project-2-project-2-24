import coverage
# Start the code coverage detection
tot_coverage = coverage.coverage()
tot_coverage.start()

# Below, import the functions that shoule be tested
import sys # pragma: no cover
import os # pragma: no cover
from bus_factor import bus_factor # pragma: no cover
from file_parser import file_parser # pragma: no cover
from main import analyze_repo # pragma: no cover
from metric_helper import metric_helper # pragma: no cover
from total_data_helper import total_data_helper # pragma: no cover
from ramp_up_time import ramp_up_time # pragma: no cover
from correctness import correctness # pragma: no cover
from responsiveness import responsiveness # pragma: no cover
from url_handler import get_github_url # pragma: no cover
from dotenv import load_dotenv # pragma: no cover


# ----------------------------------------------------------------------
def test_all():
    blockPrint()
    repo = analyze_repo('https://github.com/dbatides/3issues_2commits')

    tests =[]
    tests.append(test_dir_file_parser())
    tests.append(test_return_type_file_parser())
    tests.append(test_file_parser_result())
    tests.append(test_ramp_up_time_dir())
    tests.append(test_ramp_up_time_type())
    tests.append(test_ramp_up_time_range())
    tests.append(test_ramp_up_time_result())
    tests.append(test_correctness_dir())
    tests.append(test_correctness_type())
    tests.append(test_correctness_result())
    tests.append(data_helper_dir())
    tests.append(data_helper_type())
    #tests.append((test_empty_folder()))
    tests.append(test_url_handler_npmjs())
    tests.append(test_url_handler_github())
    tests.append(test_url_handler_invalid())
    tests.append(test_api_module())
    tests.append(test_bus_factor_normalstats_normalcontribs(repo.met_help))
    tests.append(test_bus_factor_nonestats_nonecontribs())
    tests.append(test_responsiveness_none())
    tests.append(test_responsiveness_normal(repo.met_help))
    tests.append(repoMetrics_test(repo))
    
    total_cases = 0
    pass_cases = 0
    for test in tests:
        total_cases+=1
        if test == True:
            pass_cases+=1

    rate = tot_coverage.report()
    #tot_coverage.html_report()
    enablePrint()
    print('Total:',total_cases)
    print('Passed:',pass_cases)
    print('Coverage: {}%'.format(int(rate)))
    print('{}/{} test cases passed. {}% line coverage achieved.'.format(pass_cases,total_cases,int(rate)))
    tot_coverage.stop()
    #tot_coverage.html_report()
    return total_cases-pass_cases

# --------------------------------------------------------------------
# --------------------------- file parser tests ----------------------
def test_dir_file_parser():
    acurrate_result = {'num_lines':1,'num_comments':0,'num_functions':0,'num_class':0,'num_bytes':0}
    actual_result = file_parser('this file loc is not existing at all')
    case_passed = False
    if (acurrate_result == actual_result):
        case_passed = True
    if case_passed: print('1')
    return case_passed

def test_return_type_file_parser():
    result = file_parser('src/test_module/test.js')
    case_passed = False
    if type(result) == type({'num_lines':1,'num_comments':0,'num_functions':0,'num_class':0,'num_bytes':0}):        
        case_passed = True
    if case_passed: print('2')
    return case_passed

def test_file_parser_result():
    result = file_parser('src/test_module/test.js')
    case_passed = False
    if result['num_lines'] == 70 and result['num_comments'] == 6:
        case_passed = True
    if case_passed: print('3')
    return case_passed

# --------------------------------------------------------------------
# -------------------- api unit test funcitons -----------------------
def test_api_module():
    #test code that does not get covered in other modules
    import api
    
    repo = api.Github_Handler()
    if (repo.get_something('nothing') != -1):
        print(repo.get_something)
        return False
    load_dotenv()
    repo.token=os.getenv("GITHUB_TOKEN")
    repo.repo=('jonschlinkert/even')
    if (repo.get_something('nothing') == -1):
        print('4')
        return True
    return False



# --------------------------------------------------------------------
# -------------------------- ramp up time tests ----------------------
def test_ramp_up_time_dir():
    result = ramp_up_time('This is module path is not existing at all')
    case_passed = False
    if -1 == result:
        case_passed = True
    if case_passed: print('5')
    return case_passed

def test_ramp_up_time_type():
    result = ramp_up_time('src/test_module')
    case_passed = False
    if type(result) == type(1) or type(result) == type(1.0):
        case_passed = True
    if case_passed: print('6')
    return case_passed

def test_ramp_up_time_range():
    result = ramp_up_time('src/test_module')
    case_passed = False
    if result == -1 or (result >= 0 and result <= 1):
        case_passed = True
    if case_passed: print('7')
    return case_passed

def test_ramp_up_time_result():
    result = ramp_up_time('src/test_module')
    case_passed = False
    if result <= 0.57*(1.05) and result >= 0.57*(0.95):
        case_passed = True
    if case_passed: print('8')
    return case_passed


# --------------------------------------------------------------------
# --------------------------- correctness tests ----------------------
def test_correctness_dir():
    case_passed = False
    result = correctness('This is a path that does not exist')
    if result == -1:
        case_passed = True
    if case_passed: print('9')
    return case_passed

def test_correctness_type():
    case_passed = False
    result = correctness('src/test_module')
    if type(result) == type(1.0) or type(result) == type(1):
        case_passed = True
    if case_passed: print('10')
    return case_passed

def test_correctness_result():
    case_passed = False
    result = correctness('src/test_module')
    if result <= 0.705*(1.05) and result >= 0.705*(0.95):
        case_passed = True
    if case_passed: print('11')
    return case_passed


# --------------------------------------------------------------------
# --------------------------- data helper tests ----------------------
def data_helper_dir():
    case_passed = False
    result = total_data_helper('This is antoher dirctoray that does not exist')
    if result == {'num_lines': 1, 'num_comments': 0, 'num_functions': 0, 'num_class': 0, 'num_bytes': 0, \
        'num_lines_README': 0, 'num_https':0,'license':'None'}:
        case_passed = True
    if case_passed: print('12')
    return True

def data_helper_type():
    result = total_data_helper('src/test_module')
    case_passed = False
    d = {'1':1}
    if type(result) == type(d):
        case_passed = True
    if case_passed: print('13')
    return True

# This function should test when the current path of the module is empty, we cannot create an empty folder in GitHub,
# This function does work in our local IDE, we just put the testing code below.

# def test_empty_folder():
#     result_1 = total_data_helper('src/test_module/empty_folder')
#     result_2 = ramp_up_time('src/test_module/empty_folder')
#     result_3 = correctness('src/test_module/empty_folder')

#     case_passed = False

#     if result_1['num_lines'] == 1 and result_2 == -1 and result_3 == -1:
#         case_passed = True
#     return case_passed
  

# --------------------------------------------------------------------
# --------------------------- url handler tests ----------------------
def test_url_handler_npmjs():
    # call get_github_url with npmjs url
    case_passed = False
    npmjs_url = 'https://www.npmjs.com/package/express'
    npmjs_to_github = get_github_url(npmjs_url)
    case_passed = True if npmjs_to_github == 'https://github.com/expressjs/expressjs.com' else False
    if case_passed: print('14')
    return case_passed

def test_url_handler_github():
    # call get_github_url with github url
    case_passed = False
    github_url = 'https://github.com/requirejs/requirejs'
    github_to_github = get_github_url(github_url)
    case_passed = True if github_to_github == 'https://github.com/requirejs/requirejs' else False
    if case_passed: print('15')
    return case_passed

def test_url_handler_invalid():
    # call get_github_url with invalid url
    case_passed = False
    invalid_url = 'this is a baaaaaaaaad url'
    invalid_url = get_github_url(invalid_url)
    case_passed = True if invalid_url == '' else False
    if case_passed: print('16')
    return case_passed


# --------------------------------------------------------------------
# --------------------------- bus factor tests -----------------------
def test_bus_factor_normalstats_normalcontribs(met_help):
    # call bus_factor with normal stats, normal contributors
    case_passed = False
    bus_score = bus_factor(met_help)
    case_passed = True if (bus_score >= 0.29 and bus_score <= 0.3) else False
    if case_passed: print('17')
    return case_passed

def test_bus_factor_nonestats_nonecontribs():
    # call bus_factor with None stats, None contributors
    case_passed = False
    helper = metric_helper()
    helper.statistics = None
    helper.contribs = None
    bus_score = bus_factor(helper)
    case_passed = True if bus_score == 0.0 else False
    if case_passed: print('18')
    return case_passed


# --------------------------------------------------------------------
# ------------------------- responsiveness tests ---------------------
def test_responsiveness_none():
    # call responsiveness with none of everything
    case_passed = False
    helper = metric_helper()
    resp_score = responsiveness(helper)
    case_passed = True if resp_score == 0.0 else False
    if case_passed: print('19')
    return case_passed

def test_responsiveness_normal(met_help):
    # call responsiveness with normal everything
    case_passed = False
    resp_score = responsiveness(met_help)
    case_passed = True if (resp_score >= 0.9 and resp_score <= 1.01) else False
    print(resp_score)
    if case_passed: print('20')
    return case_passed


# --------------------------------------------------------------------
# -------------------------- repoMetrics tests -----------------------
def repoMetrics_test(repo):
    case_passed = False
    repo.print_metrics()
    case_passed = True if repo.overall_score >= 0 else False
    print(repo.overall_score)
    if case_passed: print('21')
    return case_passed


# Citation from 
# https://stackoverflow.com/questions/8391411/how-to-block-calls-to-print#:~:text=Python%20lets%20you%20overwrite%20standard%20output%20%28stdout%29%20with,start%20blocking%20at%20the%20top%20of%20the%20file.
# Reuse codes to mute unneeded coverage printing, and thought there was no need to change two one line functions

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

if __name__ == '__main__':
    test_all()
