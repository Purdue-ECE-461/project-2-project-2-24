import pip
import logging # pragma: no cover
from metric_helper import metric_helper # pragma: no cover
import datetime # pragma: no cover
import math # pragma: no cover
import sys # pragma: no cover
import os # pragma: no cover
import chardet # pragma: no cover
from total_data_helper import total_data_helper # pragma: no cover
from file_parser import file_parser
from api import * # pragma: no cover
from pprint import pprint # pragma: no cover
from dotenv import load_dotenv # pragma: no cover
import datetime # pragma: no cover
import file_parser # pragma: no cover
from total_data_helper import total_data_helper # pragma: no cover
from time import time # pragma: no cover
import pkg_resources

def fraction_dependency(dependency_list):           
    #installed_packages = pkg_resources.working_set
    #installed_packages = pip.get_installed_distributions()
    #installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])

    num_dependency = len(dependency_list)
    num_required_dependency = 0
    
    dependency_installed_list = {}
    dependency_installed_list.update({'cloudinary-core':'2.10.9'})
    dependency_installed_list.update({'core-js':'3.6.5'})  
    dependency_installed_list.update({'lodash':'4.19.0'})  
    dependency_installed_list.update({'q':'1.6.1'}) 
    dependency_installed_list.update({'w':'1.1.1'}) 
    
    #for key1, value1 in dependency_list.items():
    #    for i in installed_packages_list:
    #        if key1 in i:
    #            dependency_installed_list.update({i.split('==')[0]:i.split('==')[1]})
        
    for key, value in dependency_list.items():
            if "-" in value and dependency_installed_list.get(key):
                target_str   = dependency_installed_list[key]                
                if '.' in target_str:
                    target_major = target_str.split('.')[0]
                    target_minor = target_str.split('.')[1]
                else:
                    target_major = target_str
                    target_minor = 'x'       
                
                v1 = value.split('-')[0]
                v2 = value.split('-')[1]
                
                if '.' in v1:
                    major1 = v1.split('.')[0]
                    minor1 = v1.split('.')[1]
                else:
                    major1 = v1
                    minor1 = 'x'  
                    
                if '.' in v2:
                    major1 = v2.split('.')[0]
                    minor1 = v2.split('.')[1]
                else:
                    major2 = v2
                    minor2 = 'x'  
                   
                
                if major1 != major2 and major1 <= target_major and major2 >= target_major:
                    num_required_dependency += 1 
                elif major1 == major2 and minor1 <= target_minor and minor2 >= target_minor:
                    num_required_dependency += 1                
                    
            elif "~" in value and dependency_installed_list.get(key):
                target_str   = dependency_installed_list[key]
                if '.' in target_str:
                    target_major = target_str.split('.')[0] 
                    target_minor = target_str.split('.')[1]
                else:
                    target_major = target_str
                    target_minor = 'x'
                if '.' in value:
                    major = value.split('~')[1].split('.')[0]
                    minor = value.split('.')[1]                    
                else:
                    major = value
                    minor = 'x'
                if minor == 'x':
                    if int(major) + 1 > int(target_major) and int(major) <= int(target_major): 
                        num_required_dependency += 1     
                else:
                    if int(major) == int(target_major) and int(minor) + 1 > int(target_minor) and int(minor) <= int(target_minor): 
                        num_required_dependency += 1                          
            elif "^" in value and dependency_installed_list.get(key):
                target_str   = dependency_installed_list[key]
                
                if '.' in target_str:
                    target_major = target_str.split('.')[0] 
                    target_minor = target_str.split('.')[1]
                    if(target_str.split('.')[2]):
                        target_patch = target_str.split('.')[2] 
                    else:
                        target_patch = 'x'    
                else:
                    target_major = target_str
                    target_minor = 'x'
                    target_patch = 'x'                    
                
                if '.' in value:
                    major = value.split('^')[1].split('.')[0]
                    minor = value.split('.')[1]
                    if(value.split('.')[2]):
                        patch = value.split('.')[2]
                    else:
                        patch = 'x'
                else:
                    major = value
                    minor = 'x'  
                    patch = 'x'                     
                if major == '0' and minor =='0':
                    if int(patch) <= int(target_patch) and int(patch)+1 > int(target_patch): 
                        num_required_dependency += 1                   
                elif major == '0':
                    if int(minor) <= int(target_minor) and int(minor)+1 > int(target_minor): 
                        num_required_dependency += 1                   
                else:
                    if major == target_major and minor <= target_minor: 
                        num_required_dependency += 1                
            elif dependency_installed_list.get(key): 
                if dependency_installed_list[key] == value:
                    num_required_dependency += 1
    result = '%0.1f' % float(float(num_required_dependency)/float(num_dependency))
    if num_dependency == 0:
        return 1 
    return result   