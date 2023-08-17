from .. import db
import multiprocessing
import time
import git
from .. import state
import json

class pollers(object):
    def __init__(self,count:int=5,db_params:dict={},repo_path:str=None):
        self.count = count
        self.db_params =db_params
        self.repo = None
        if repo_path != None:
            self.repo = git.Repo(repo_path)

    def parse_metrics(self,uid:int,repo_path:str,metrics_file:str,commit_id:str):
        print("starting metrics parsing for commit ",commit_id)
        if self.repo == None:
            self.repo = git.Repo(repo_path)
        try:
            commit = self.repo.commit(commit_id)
            tree = commit.tree
            print("tree is ========= ",tree)
            metrics_data= {}
            #if metrics_file in tree:
            try:
                file_blob = tree[metrics_file]
                file_content = file_blob.data_stream.read().decode("utf-8")
                metrics_data = json.loads(file_content)
            except Exception as e:
                pass
            print("metrics data is ",metrics_data)
            #uid:int,metrics:dict={},state=state.COMMIT_PARSE_COMPLETE
            if self.conn.update_metrics_for_commit(uid,metrics_data) == False:
                self.conn.reset_to_init(uid)
        except Exception as e:
            self.conn.reset_to_init(uid)
            print("parse_metrics error",str(e))

        return {}
    def poll(self,id):
        self.conn = db.getDb(self.db_params)
        while True:
            rows = self.conn.get_waiting_to_parse_commits(self.count)
            if len(rows) == 0:
                return 
            for row in rows:
                if self.conn.can_process_this(row,new_state=state.COMMIT_PARSE_IN_PROCESS,old_state=state.COMMIT_PARSE_INIT):
                    self.parse_metrics(row[0],row[1],row[2],row[3])

            time.sleep(1)
        return None
    def start_poller(self):
        processes =  []
        for i in range(self.count):
            process = multiprocessing.Process(target=self.poll, args=(i,))
            processes.append(process)
            process.start()
