import logging # pragma: no cover
from metric_helper import metric_helper # pragma: no cover
import datetime # pragma: no cover
import math # pragma: no cover

# ---num lines of code vs num comments
# ---length of readme (longer = better)
# ---num contributors


NUM_HTTPS_MAX = 10 # pragma: no cover
README_LINES_MAX = 400 # pragma: no cover
NUM_COMMENTS_TOOMANY = 0.33 # pragma: no cover
NUM_COMMENTS_MAX = 0.20 # pragma: no cover
NUM_CONTRIBS_MAX = 100 # pragma: no cover


def bus_factor(helper):
    logging.debug("BUS FACTOR: initializing...")
    name = "bus factor"
    bus_score = calc_score(helper)
    return bus_score


def calc_score(met_help):
    logging.info("BUS FACTOR: calculating bus factor score...")

    contribs = 0
    if met_help.contribs != None: contribs = met_help.contribs.totalCount
    else: contribs = 0

    contribs_score = 0 + (contribs >= NUM_CONTRIBS_MAX)*1 + (contribs < NUM_CONTRIBS_MAX)*(contribs/NUM_CONTRIBS_MAX)
    
    if met_help.statistics == None:
        logging.error("No 'statistics' dictionary exists.")
        (code_vs_comments_score, doc_score, https_bonus) = (0,0,0)
    else:
        code = met_help.statistics['num_lines']
        comments = met_help.statistics['num_comments']
        docs = met_help.statistics['num_lines_README']
        https = met_help.statistics['num_https']
        code_vs_comments_score = 0 + (((comments/code) <= NUM_COMMENTS_TOOMANY) and ((comments/code) >= NUM_COMMENTS_MAX))*1 + (((comments/code) < NUM_COMMENTS_MAX)*(comments/code)/NUM_COMMENTS_MAX)
        doc_score = 0 + ((docs/README_LINES_MAX) > 1)*1 + ((docs/README_LINES_MAX) <= 1)*(docs/README_LINES_MAX) # if readme has > NUM_README_LINES lines, make score 100%
        https_bonus = 0 + ((https/NUM_HTTPS_MAX) > 1)*1 + ((https/NUM_HTTPS_MAX) <= 1)*(https/NUM_HTTPS_MAX) # if readme has > NUM_HTTPS links, make score 100%
    
    bus_score = (0.31*contribs_score) + (0.31*code_vs_comments_score) + (0.31*doc_score) + (0.07*https_bonus)

    return bus_score
