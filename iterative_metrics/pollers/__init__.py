from .. import db
import multiprocessing
import time

class pollers(object):
    def __init__(self,count:int=5,db_params:dict={}):
        self.count = count
        self.db_params =db_params
    def poll(self,id):
        self.conn = db.getDb(self.db_params)
        while True:
            rows = self.conn.get_waiting_to_parse_commits(self.count)
            print(rows)
            time.sleep(1)
        return None
    def start_poller(self):
        processes =  []
        for i in range(self.count):
            process = multiprocessing.Process(target=self.poll, args=(i,))
            processes.append(process)
            process.start()
        for p in processes:
            p.join()

