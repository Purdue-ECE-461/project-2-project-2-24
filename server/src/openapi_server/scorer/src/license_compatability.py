# Overview
# ACME uses GNU LGPLv2.1
# Use following as guides: 
#   http://www.gnu.org/licenses/gpl-faq.html#AllCompatibility
#   https://www.whitesourcesoftware.com/resources/blog/license-compatibility/
from openapi_server.scorer.src.total_data_helper import total_data_helper # pragma: no cover
import logging # pragma: no cover

def license_compatability(repo_dir):
    '''
        Calculates a License Compatability Score. Assumes ACME Corporation still uses LGPLv2.1!
    '''
    # Configuration values
    cpy_weight = 0.5
    lib_weight = 0.5

    # ========= License Calculations ============
    cpy_score = 0 #final score between 0 and 1
    lib_score = 0 #final score between 0 and 1

    dir_stats = total_data_helper(repo_dir)
    license_type = dir_stats['license']
    #print(license_type)

    if not ((license_type == "MIT") or (license_type == "BSD-new") or (license_type == "Apache 2.0") or (license_type == "GPLv2") or (license_type == "GPLv2+") or (license_type == "GPLv3") or (license_type == "LGPLv2.1") or (license_type == "LGPLv2.1+") or (license_type == "LGPLv3")): return 0

    cpy_score = 0 + 1*((license_type == "MIT") or (license_type == "BSD-new") or (license_type == "Apache 2.0") or (license_type == "LGPLv2.1")) + 0.8*((license_type == "LGPLv2.1+") or (license_type == "LGPLv3")) + 0.6*(license_type == "GPLv2") + 0.5*(license_type == "GPLv2+") + 0.4*(license_type == "GPLv3")
    lib_score = 0 + 1*((license_type == "MIT") or (license_type == "BSD-new") or (license_type == "Apache 2.0") or (license_type == "LGPLv2.1") or (license_type == "LGPLv2.1+") or (license_type == "LGPLv3")) + 0.7*((license_type == "GPLv2") or (license_type == "GPLv2+")) + 0.6*(license_type == "GPLv3")

    '''if (license_type == "MIT") or (license_type == "BSD-new") or (license_type == "Apache 2.0"):
        # Permissive licenses are completely compatible 
        cpy_score = 1
        lib_score = 1
    elif (license_type == "GPLv2"): 
        cpy_score = .6 # COPY: GPLv2 only (OK, combination is under gplv2)
        lib_score = .7 # LIBS: GPLv2 only (OK, combination is under gplv2 only)
    elif(license_type == "GPLv2+"): 
        cpy_score = .5 # COPY: GPLv2 or later (OK, combination is under gplv2 or later)
        lib_score = .7 # LIBS: GPLv2 or later (OK, combination is under gplv2 or later)
    elif(license_type == "GPLv3"): 
        cpy_score = .4 # COPY: GPLv3 (OK, combination is under gplv3)
        lib_score = .6 # LIBS: GPLv3 (OK, combination is under gplv3)
    elif(license_type == "LGPLv2.1"): 
        cpy_score = 1  # COPY: LGPLv2.1 (OK)
        lib_score = 1  # LIBS: LGPLv2.1 (OK)
    elif(license_type == "LGPLv2.1+"): 
        cpy_score = .8 # COPY: LGPLv2.1+ (OK under GPLv3 terms)
        lib_score = 1  # LIBS: LGPLv2.1+ (OK)
    elif(license_type == "LGPLv3"):
        cpy_score = .8  # COPY: LGPLv3 (OK under GPLv3 combination)
        lib_score = 1  # LIBS: LGPLv3 (OK)
    else:
        logging.info("Invalid or no license found!")
        return -1'''
        
    return ((cpy_weight*cpy_score)+(lib_weight*lib_score))

'''
if __name__=="__main__":
    # Check handled calculated values (compare with sample output + intuition)
    license = "GPLv2"
    print("Calculated Value for %s: %0.2f" % (license,license_compatability(license)))
    license = "GPLv2+"
    print("Calculated Value for %s: %0.2f" % (license,license_compatability(license)))
    license = "GPLv3"
    print("Calculated Value for %s: %0.2f" % (license,license_compatability(license)))
    license = "LGPLv2.1"
    print("Calculated Value for %s: %0.2f" % (license,license_compatability(license)))
    license = "LGPLv2.1+"
    print("Calculated Value for %s: %0.2f" % (license,license_compatability(license)))
    license = "LGPLv3"
    print("Calculated Value for %s: %0.2f" % (license,license_compatability(license)))
    license = "MIT"
    print("Calculated Value for %s: %0.2f" % (license,license_compatability(license)))

    # Attempt to break function
    license = 32
    print("Calculated Value for %s: %0.2f" % (str(license),license_compatability(license)))
    license = []
    print("Calculated Value for %s: %0.2f" % (license,license_compatability(license)))
    '''