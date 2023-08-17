from . import database
import psycopg2
import json
from .. import state
from git.objects.commit import Commit
from typing import List
import datetime


class postgres_db(database.database):
    def __init__(self,name,type_name,conn_params):
        self.name = name
        self.type = type_name
        self.conn_params = conn_params
        db_params = {
            'dbname': conn_params["dbname"],
            'user': conn_params["user"],
            'password': conn_params["password"],
            'host': conn_params["host"],
            'port': conn_params["port"]
        }
        self.conn = psycopg2.connect(**db_params)
    def __get_formatted_datetime__(self,input_datetime:datetime.datetime):
        return input_datetime.strftime('%Y-%m-%d %H:%M:%S')


    def add_commits(self,repo: str,metrics_path:str,commits: List[Commit],commit_state: str=state.COMMIT_PARSE_INIT):
        '''
            uid          bigint PRIMARY KEY          NOT NULL,
            repo_path    varchar(1000)               NOT NULL,
            commit_id    varchar(1000)               NOT NULL,
            metrics_file varchar(1000)               NOT NULL,
            metrics      jsonb                       DEFAULT '{}',
            author       varchar(1000)               DEFAULT '',
            committer    varchar(1000)               DEFAULT '',
            committed_time  timestamp without time zone NOT NULL,
            authored_date timestamp without time zone NULL,
            co_authors   varchar(1000)               DEFAULT '',
            state        varchar(100)                NOT NULL,
            created_at   timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
            parsed_at    timestamp without time zone NULL
        '''
        table_data = []
        for commit in commits:
            table_data.append((repo,commit.hexsha,metrics_path,str(commit.author),str(commit.committer),self.__get_formatted_datetime__(commit.committed_datetime),self.__get_formatted_datetime__(commit.authored_datetime),','.join([str(i) for i in commit.co_authors]),commit_state))
        sql_insert = """
        INSERT INTO commmit_metrics (repo_path,commit_id,metrics_file,author,committer,committed_time,authored_date,co_authors,state) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        try:
            cursor = self.conn.cursor()
            print(sql_insert,table_data)
            cursor.executemany(sql_insert, table_data)
            self.conn.commit()
            cursor.close()
        except Exception as e:
            print(str(e))
            raise e

    def get_pending_counts(self):
        """
        get pending tasks.

        :return: bool
        """
        cursor = self.conn.cursor()
        select_query= "SELECT count(*) FROM commmit_metrics WHERE state = '"+state.COMMIT_PARSE_IN_PROCESS+"' OR state='"+state.COMMIT_PARSE_INIT+"'"
        try:
            cursor.execute(select_query)
            rows = cursor.fetchall()
            cursor.close()
            return rows[0][0]
        except (Exception, psycopg2.Error) as error:
            print("error in get_pending_counts commits:", error)
            return 0

    def get_waiting_to_parse_commits(self,count,state=state.COMMIT_PARSE_INIT):
        cursor = self.conn.cursor()
        select_query= "SELECT uid, repo_path, metrics_file,commit_id FROM commmit_metrics WHERE state = '"+state+"' order by created_at asc"
        try:
            cursor.execute(select_query)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except (Exception, psycopg2.Error) as error:
            print("error in getting waiting to parse commits:", error)
            return []
    def get_commit_details(self,commit_id:str):
        select_query = "SELECT uid FROM commmit_metrics WHERE commit_id=%s"
        cursor = self.conn.cursor()
        try:
            cursor.execute(select_query,[commit_id])
            rows = cursor.fetchall()
            return rows
        except (Exception, psycopg2.Error) as error:
            print("Error while updating new process state:", error)
            self.conn.rollback()
            return False
    def get_commits(self,commmit_row:List,count=50,direction="forward"):
        print("in get commits")
        uid = None
        res = []
        if commmit_row!=None and len(commmit_row)>0:
            uid=commmit_row[0][0]
        select_query = "SELECT commit_id,author,co_authors,committed_time,authored_date,metrics,uid FROM commmit_metrics WHERE state=%s"
        if uid!= None:
            if direction == "forward":
                select_query += " AND uid > "+str(uid)
            else:
                select_query += " AND uid < "+str(uid)
        if direction == "forward":
            select_query += " ORDER BY uid ASC LIMIT %s"
        else:
            select_query += " ORDER BY uid DESC LIMIT %s"
        print("========================="+select_query)
        cursor = self.conn.cursor()
        try:
            cursor.execute(select_query,[state.COMMIT_PARSE_COMPLETE,count])
            print("Executing query ",select_query)
            rows = cursor.fetchall()
            res = []
            for row in rows:
                print(len(row),row,row[0],row[1],row[2],row[3],row[4],row[5])
                res.append({
                    "commit_id":row[0],
                    "author": row[1],
                    "co_authors":row[2],
                    "committed_time": row[3],
                    "authored_date":row[4],
                    "metrics":row[5]
                })
            return res
        except (Exception, psycopg2.Error) as error:
            print("Error while selecting metrics",str(error))
            return []


    def can_process_this(self,row,new_state=state.COMMIT_PARSE_IN_PROCESS,old_state=state.COMMIT_PARSE_INIT):
        """
        get pending tasks.

        :return: bool
        """
        update_query = "UPDATE commmit_metrics SET state=%s WHERE state=%s AND uid=%s"
        cursor = self.conn.cursor()
        try:
            cursor.execute(update_query, (new_state, old_state,row[0]))
            self.conn.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except (Exception, psycopg2.Error) as error:
            print("Error while updating new process state:", error)
            self.conn.rollback()
            return False
        
    def reset_to_init(self,uid:int,state=state.COMMIT_PARSE_INIT):
        try:
            cursor = self.conn.cursor()
            # Construct the SQL INSERT statement with the JSON data
            update_query = "UPDATE commmit_metrics SET state=%s where uid= %s"
            # Execute the SQL statement with the JSON data
            cursor.execute(update_query, [state,uid])
            self.conn.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            print("Error while resetting to init state:"+str(e))
            return False


    def update_metrics_for_commit(self,uid:int,metrics:dict={},state=state.COMMIT_PARSE_COMPLETE):
        try:
            print("update metrics for uid",uid,"metrics",metrics,"state",state)
            cursor = self.conn.cursor()
            # Construct the SQL INSERT statement with the JSON data
            update_query = "UPDATE commmit_metrics SET metrics=%s,state=%s where uid=%s"
            # Execute the SQL statement with the JSON data
            cursor.execute(update_query, [json.dumps(metrics),state,uid])
            self.conn.commit()
            if cursor.rowcount > 0:
                return True
            else:
                print("Failed to update any data")
                return False
        except Exception as e:
            print("Error while updating the metrics: "+str(e))
            return False
