from api import * # pragma: no cover
import os # pragma: no cover
from pprint import pprint # pragma: no cover
from dotenv import load_dotenv # pragma: no cover
import logging # pragma: no cover
import datetime # pragma: no cover
import file_parser # pragma: no cover
from total_data_helper import total_data_helper # pragma: no cover
from time import time # pragma: no cover


class metric_helper:
    def __init__(self):
        self.url = ''
        self.token = ''
        self.dir = ''
        self.github_url = ''
        self.github_handle = None
        self.issues_pages = None
        self.commit_pages = None
        self.contribs = None
        self.avg_time_open = -1
        self.avg_update_time = -1
        self.statistics = None


    def get_api_stuff(self, token, url, dir):
        logging.info("METRIC HELPER: initializing...")
        self.url = url
        self.token = token
        self.dir = dir
        self.github_handle = Github_Handler()
        self.github_handle.token = self.token # set GitHub token
        self.github_handle.set_repo_format(self.url) # set owner/repo format from url
        self.issues_pages = self.issues()
        self.commit_pages = self.commits()
        self.contribs = self.contributors()
        self.avg_time_open = self.avg_time_issue_open()
        self.avg_update_time = self.update_time()
        self.statistics = self.stats(dir)

    
    def stats(self, dir):
        logging.info("METRIC HELPER: get statistics")
        # use Yitong's file parser to get stats
        stats = total_data_helper(dir)
        return stats


    def issues(self):
        logging.info("METRIC HELPER: get issues")
        return self.github_handle.get_something('issues')


    def commits(self):
        logging.info("METRIC HELPER: get commits")
        return self.github_handle.get_something('commits')


    def contributors(self):
        logging.info("METRIC HELPER: get contributors")
        return self.github_handle.get_something('contributors')


    def avg_time_issue_open(self):
        logging.info("METRIC HELPER: get avg time issues open")
        opened = 0 # list of push dates in datetime format
        closed = 0 # list of push dates in datetime format
        sum = 0
        num_issues = 0

        for iss in self.issues_pages:
            opened = iss.created_at # date issue updated
            closed = iss.closed_at # date issue updated
            diff = self.datetime_to_days(closed - opened)
            sum += diff
            num_issues += 1
        
        avg_time_open = 0 if num_issues == 0 else (sum / num_issues)
        return avg_time_open


    def update_time(self):
        logging.info("METRIC HELPER: get avg update time")
        if self.commit_pages == None: return -1
        sum = 0
        num_commits = 0

        more_recent = datetime.datetime.strptime(self.commit_pages[0].last_modified, "%a, %d %b %Y %H:%M:%S %Z")
        for i, com in enumerate(self.commit_pages):
            tmp = datetime.datetime.strptime(com.last_modified, "%a, %d %b %Y %H:%M:%S %Z")
            if i != 0:
                diff = self.datetime_to_days(more_recent - tmp)
                sum += diff
                num_commits = i
                more_recent = tmp

        if num_commits == 0: return -1
        avg_time = sum / num_commits
        return avg_time


    def datetime_to_days(self, diff):
        #logging.info("METRIC HELPER: convert datetime to number of days")
        duration_in_s = (diff).total_seconds()
        diff_tuple = divmod(duration_in_s, 86400)
        diff_fraction = diff_tuple[0] + diff_tuple[1]/86400
        return diff_fraction
