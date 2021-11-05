import tempfile # pragma: no cover
import logging # pragma: no cover
import git # pragma: no cover
import os # pragma: no cover
import sys # pragma: no cover
from dotenv import load_dotenv # pragma: no cover
import shutil # pragma: no cover
import repoMetrics # pragma: no cover
import coverage # pragma: no cover

#import June's code here
from metric_helper import metric_helper # pragma: no cover
import url_handler # pragma: no cover

#import Easton's code here
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
log_file = os.getenv("LOG_FILE")
debug_level = os.getenv("LOGGING_LEVEL")

log_level = 0
logging.disable = False

log_level = 0 + 20 * (int(debug_level == 1)) + 10*(int(debug_level == 2))
logging.disable = True if log_level == 0 else False
logging.basicConfig(filename=log_file,level=log_level)

def analyze_repo(url):
        # Configure current current Repository Object
        cur_repo = repoMetrics.Repository()
        tmp_dir = tempfile.TemporaryDirectory()
        cur_repo.dir = tmp_dir
        
        #
        cur_repo.dir.name = 'working' #TODO: Check for errors in the creation of the temporary directory
        cur_repo.url = url

        # TODO: Handle error where working exists already
        if os.path.isdir('working'):
            logging.error('Working directory left over, deleting...')
            try: shutil.rmtree('working')
            except OSError: 
                logging.error('Could not delete working directory!!')
                return 23

        # TODO: Get repo url from June's function, for now just going to clone directly
        clean_url = url_handler.get_github_url(url)
        logging.debug("Repository url found, using %s" % (clean_url))
        git.Repo.clone_from(clean_url, cur_repo.dir.name)
        logging.debug("Repository cloned!")

        met_help = metric_helper()
        met_help.get_api_stuff(token, clean_url, cur_repo.dir.name)
        cur_repo.met_help = met_help

        # TODO: calculate individual metrics, for now setting random
        logging.debug("Calculating individual metric scores...")
        cur_repo.calc_metrics()
        
        # Calculate overall score and clean up the working file
        cur_repo.calc_overall()
        tmp_dir.cleanup()
        return cur_repo

def main(): # pragma: no cover

    # ==================== Input Handling ======================
    if len(sys.argv)<2:
        logging.error("Error: Not enough Arguments Provided!")

    if (sys.argv[1] == "install"):
        print("Successfully installed all dependencies!")
        return 0
    elif(sys.argv[1] == "test"):
        import unitests
        ret_val = unitests.test_all()
        return ret_val


    # ================== Start of Calculations ==================
    repositories = []
    url_file = open(sys.argv[1],'r')
    for url in url_file:
        clean_url = url.strip() #NEEDED OR ELSE CLONE BREAKS!
        logging.info("Working on %s url..." % (clean_url))
        clean_url = url_handler.get_github_url(clean_url)

        # Perform analysis
        cur_repo = analyze_repo(clean_url)
        
        #Log changes and append repo to scores
        logging.info("Calculated overall score for %s: %.2f" % (clean_url, cur_repo.overall_score))
        repositories.append(cur_repo)
    # ================== End of Calculations ===================


    # ================= PRINT FORMATTED OUTPUT =================
    repositories.sort(key=lambda x: x.overall_score, reverse=True)
    print("URL NET_SCORE RAMP_UP_SCORE CORRECTNESS_SCORE BUS_FACTOR_SCORE RESPONSIVE_MAINTAINER_SCORE LICENSE_SCORE")
    for repo in repositories:
        repo.print_metrics()
        #repo.validate_scores()

if __name__ == "__main__":
    main() # pragma: no cover
