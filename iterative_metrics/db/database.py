from abc import ABCMeta, abstractmethod
import json
import os
import hashlib
from git.objects.commit import Commit

class database(object):
    
    @abstractmethod
    def validate(self):
        """
        validate whether init data is fine .

        Returns True if everything is fine, False and reasons otherwise.

        :return: bool
        """
        raise NotImplementedError
    @abstractmethod
    def add_commits(self,repo,metrics_path,Commits,state):
        """
        adds a commit to database .

        :return: bool
        """
        raise NotImplementedError
    @abstractmethod
    def get_pending_counts(self):
        """
        get pending tasks.

        :return: bool
        """
        raise NotImplementedError
    
    @abstractmethod
    def can_process_this(self,row,new_state,old_state):
        """
        get pending tasks.

        :return: bool
        """
        raise NotImplementedError
    @abstractmethod
    def reset_to_init(self,uid,state):
        """
        reset to init state.

        :return: bool
        """
        raise NotImplementedError



    @abstractmethod
    def get_commit_details(self,commit_id):
        """
        get details of a commit
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_waiting_to_parse_commits(self,count=0):
        """
        get pending tasks.

        :return: bool
        """
        raise NotImplementedError
    @abstractmethod
    def update_metrics_for_commit(self,uid:int,metrics:dict,state:str):
        """
        update metrics data from a commit.

        :return: bool
        """
        raise NotImplementedError
    @abstractmethod
    def get_commits(self,commit_row,count,direction):
        """
        get commits above or below a commit
        """
        raise NotImplementedError

