import yaml
from  . import config
from . import db
from . import pollers
import git
import time

class metric_parser(object):
    def __init__(self,config_path="config.yaml"):
        self.config = config.config(config_path)
        self.databaseConfig = self.config.get_component("database")
        self.db = db.getDb(self.databaseConfig)
    
    def parse_repo(self,repo_path:str,metrics_file:str):
        repo = git.Repo(repo_path)
        commits = repo.iter_commits()
        commit_group = []
        for commit in commits:
            if len(commit_group) == 20:
                self.db.add_commits(repo_path,metrics_file,commit_group)
                commit_group = []
            commit_group.append(commit)
        if len(commit_group):
            self.db.add_commits(repo_path,metrics_file,commit_group)
        commit_pollers = pollers.pollers(db_params=self.databaseConfig)
        commit_pollers.start_poller()
        while True:
            val = self.db.get_pending_counts()
            if self.db.get_pending_counts() > 0:
                time.sleep(5)
                continue
            else:
                break
    def fetch_repo_data(self,commit_id=None,count=50,direction:str="forward"):
        commits = []
        commit_details = None
        if commit_id != None:
            commit_details = self.db.get_commit_details(commit_id)
        commits = self.db.get_commits(commit_details,count,direction)            
        return commits
            