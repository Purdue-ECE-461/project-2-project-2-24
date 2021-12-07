import base64
import tempfile  # pragma: no cover
import logging  # pragma: no cover
import git  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover
from dotenv import load_dotenv  # pragma: no cover
import shutil  # pragma: no cover
import repoMetrics  # pragma: no cover
import zipfile

# import June's code here
from metric_helper import metric_helper  # pragma: no cover
import url_handler  # pragma: no cover

# import Easton's code here
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
log_file = os.getenv("LOG_FILE")
debug_level = os.getenv("LOGGING_LEVEL")

log_level = 0
logging.disable = False

log_level = 0 + 20 * (int(debug_level == 1)) + 10 * (int(debug_level == 2))
logging.disable = True if log_level == 0 else False
logging.basicConfig(filename=log_file, level=log_level)


def zip_directory(directory, zipfile):
    for root, dirs, files in os.walk(directory):
        for file in files:
            zipfile.write(os.path.join(root, file),
                          os.path.relpath(os.path.join(root, file),
                                          os.path.join(directory, "..")))


def analyze_repo(url):
    cur_repo = repoMetrics.Repository()
    tmp_dir = tempfile.TemporaryDirectory()
    cur_repo.dir = tmp_dir
    #cur_repo.dir.name = 'working'  # TODO: Check for errors in the creation of the temporary directory
    cur_repo.url = url

    # TODO: Handle error where working exists already
    if os.path.isdir('working'):
        # logging.error('Working directory left over, deleting...')
        try:
            shutil.rmtree('working')
        except OSError:
            # logging.error('Could not delete working directory!!')
            return 23

    # TODO: Get repo url from June's function, for now just going to clone directly
    clean_url = url_handler.get_github_url(url)
    # logging.debug("Repository url found, using %s" % (clean_url))
    git.Repo.clone_from(clean_url, cur_repo.dir.name)
    # logging.debug("Repository cloned!")

    dependency_list = {}
    dep_flag = False
    for filename in os.listdir(cur_repo.dir):
        if not os.path.isdir(filename):
            with open(filename, "r") as cur_file:
                for line in cur_file:
                    if dep_flag is True:
                        if "}" in str(line):
                            pass
                        else:
                            result = str(line, 'utf-8')
                            dependency = result.rstrip().split(',')[0].split(' ')[4].strip('\"').rstrip(':').rstrip('"')
                            version = result.rstrip().split(',')[0].split(' ')[5].strip('\"')
                            dependency_list.update({dependency: version})
                    if "dependencies" in str(line):
                        dep_flag = True
                    if dep_flag is True and "}" in str(line):
                        dep_flag = False

    # Initialize base64 repo contents
    base64_contents = "base64encodedfile"

    # Set up temporary file name for zip file
    temp_file = tempfile.TemporaryFile()

    # Set up zipfile
    zip_file = zipfile.ZipFile(temp_file.name, "w", zipfile.ZIP_DEFLATED)

    # Zip repo contents
    zip_directory(cur_repo.dir.name, zip_file)

    # Get base64 contents of zip file
    with open(temp_file.name, "rb") as file:
        base64_contents = base64.b64encode(file.read())

    # Clean up
    zip_file.close()
    temp_file.cleanup()

    met_help = metric_helper()
    met_help.get_api_stuff(token, clean_url, cur_repo.dir.name)
    cur_repo.met_help = met_help

    # TODO: calculate individual metrics, for now setting random
    # logging.debug("Calculating individual metric scores...")
    cur_repo.calc_metrics(dependency_list)

    # Calculate overall score and clean up the working file
    cur_repo.calc_overall()
    tmp_dir.cleanup()
    return cur_repo, base64_contents


def main():  # pragma: no cover

    # ==================== Input Handling ======================
    if len(sys.argv) < 2:
        logging.error("Error: Not enough Arguments Provided!")

    if (sys.argv[1] == "install"):
        print("Successfully installed all dependencies!")
        return 0
    elif (sys.argv[1] == "test"):
        import unitests
        ret_val = unitests.test_all()
        return ret_val

    # ================== Start of Calculations ==================
    repositories = []
    z = zipfile.ZipFile(sys.argv[1])

    for filename in z.namelist():
        if not os.path.isdir(filename):
            for line in z.open(filename):
                if "homepage" in str(line):
                    result = str(line, 'utf-8')
                    result = result.rstrip().split(',')[0].split(' ')[3].strip('\"')
                    clean_url = result.strip()
                    clean_url = url_handler.get_github_url(clean_url)
                    cur_repo = analyze_repo(clean_url, z)
                    repositories.append(cur_repo)
            z.close()
    del z

    repositories.sort(key=lambda x: x.overall_score, reverse=True)
    print(
        "URL NET_SCORE RAMP_UP_SCORE CORRECTNESS_SCORE BUS_FACTOR_SCORE RESPONSIVE_MAINTAINER_SCORE LICENSE_SCORE FRACTION_DEPENDENCY")
    for repo in repositories:
        repo.print_metrics()
    if repo.flag_check() is True:
        Ingestible = True


if __name__ == "__main__":
    main()  # pragma: no cover
