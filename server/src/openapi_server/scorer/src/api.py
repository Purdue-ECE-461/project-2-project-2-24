from github import Github # pragma: no cover
import logging # pragma: no cover

class Github_Handler:
    '''
    Used for all Github API requests. Performs very quickly and provides a lot of base functionality to prevent rewriting code.
    '''

    def __init__(self,token='',repo='') -> None:
        self.token=token
        self.repo=repo

    def get_something(self, something):
        # Configure api object
        if(self.token == '') or self.repo == '':
            logging.error("Must set Github_Handler.token and .repo to use!")
            return -1
	
        git_helper = Github(self.token)
        repo_obj = git_helper.get_repo(self.repo)

        if something == 'issues':
            return self.get_issues(repo_obj)
        elif something == 'contributors':
            return self.get_contributors(repo_obj)
        elif something == 'commits':
            return self.get_commits(repo_obj)
        else:
            logging.error("Not a valid request!")
            return -1


    # returns paginated list
    def get_issues(self, repo_obj):
        issues = repo_obj.get_issues(state="closed")
        return issues


    def get_contributors(self, repo_obj):
        contributors = repo_obj.get_contributors()
        return contributors


    def get_commits(self, repo_obj):
        commits = repo_obj.get_commits()
        return commits


    # helper functions
    def set_repo_format(self, url):
        parts = url.split("/")
        self.repo = str(parts[len(parts) - 2] + "/" + parts[len(parts) - 1])
