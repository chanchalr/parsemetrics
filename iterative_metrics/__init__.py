import yaml
from  . import config
from . import db
from . import pollers
import git

class metric_parser(object):
    def __init__(self,config_path="config.yaml"):
        self.config = config.config(config_path)
        databaseConfig = self.config.get_component("database")
        self.db = db.getDb(databaseConfig)
        commit_pollers = pollers.pollers(db_params=databaseConfig)
        commit_pollers.start_poller()
    
    def parse_repo(self,repo_path:str,metrics_file:str):
        repo = git.Repo(repo_path)
        commits = repo.iter_commits()
        commit_group = []
        for commit in commits:
            if len(commit_group) == 20:
                self.db.add_commits(commit_group)
                commit_group = []
            commit_group.append(commit)
        if len(commit_group):
            self.db.add_commits(repo_path,metrics_file,commit_group)
            