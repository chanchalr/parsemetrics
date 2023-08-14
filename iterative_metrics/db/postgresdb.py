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

    def add_metrics(self,commit_id,metrics):
        """
        adds a metrics to a commit id .

        :return: bool
        """
    def get_pending_counts(self):
        """
        get pending tasks.

        :return: bool
        """
        cursor = self.conn.cursor()
        select_query= "SELECT uid, repo_path, metrics_file FROM commmit_metrics WHERE state = '"+state+"' order by created_at asc"
        try:
            cursor.execute(select_query)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except (Exception, psycopg2.Error) as error:
            print("Error:", error)
            return []

    def get_pending_commits(self,count,state=state.COMMIT_PARSE_INIT):
        cursor = self.conn.cursor()
        select_query= "SELECT uid, repo_path, metrics_file FROM commmit_metrics WHERE state = '"+state+"' order by created_at asc"
        try:
            cursor.execute(select_query)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except (Exception, psycopg2.Error) as error:
            print("Error:", error)
            return []

