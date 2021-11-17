import logging # pragma: no cover
from api import * # pragma: no cover
from metric_helper import metric_helper # pragma: no cover
import datetime # pragma: no cover

# ---avg time all closed issues were open
# ---avg time between updates
# ---how long ago was last updated (last date pushed)

# units are days
UPDATE_TIME_MAX = 100 # pragma: no cover
ISSUE_OPEN_MAX = 100 # pragma: no cover
LAST_UPDATE_MAX = 250 # pragma: no cover
NUM_RELEASE_MAX = 50 # pragma: no cover


def responsiveness(helper):
    logging.debug("RESPONSIVENESS: initializing...")
    name = "responsiveness"
    resp_score = calc_score(helper)
    return resp_score


def calc_score(met_help):
    logging.info("RESPONSIVENESS: calculating responsiveness score...")
    
    up_time = met_help.avg_update_time
    time_iss_open = met_help.avg_time_open
    last_up = last_update(met_help)

    up_time_score = 0 + (up_time != -1 and up_time <= UPDATE_TIME_MAX)*((UPDATE_TIME_MAX - up_time)/UPDATE_TIME_MAX)
    time_iss_open_score = 0 + (time_iss_open != -1 and time_iss_open <= ISSUE_OPEN_MAX)*((ISSUE_OPEN_MAX - time_iss_open)/ISSUE_OPEN_MAX)
    last_up_score = 0 + (last_up != -1 and last_up < LAST_UPDATE_MAX)*((LAST_UPDATE_MAX - last_up)/LAST_UPDATE_MAX)

    resp_score = (0.35*up_time_score) + (0.50*time_iss_open_score) + (0.15*last_up_score)

    '''
    print("\nupdate time score = ", up_time_score)
    print("time issues open score = ", time_iss_open_score)
    print("last update score = ", last_up_score)
    print("num releases score = ", releases_score)
    print("total responsiveness score = ", resp_score)
    '''

    return resp_score


# how long ago the last update was in days
def last_update(met_help):
    logging.info("RESPONSIVENESS: getting time since last update...")
    ups = met_help.commit_pages
    
    if ups == None: return -1

    datetime_last_update = datetime.datetime.strptime(ups[0].last_modified, "%a, %d %b %Y %H:%M:%S %Z")
    now = datetime.datetime.now()
    diff = now - datetime_last_update
    last_update = met_help.datetime_to_days(diff)
    return last_update