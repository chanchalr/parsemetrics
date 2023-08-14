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
    def add_metrics(self,commit_id,metrics):
        """
        adds a metrics to a commit id .

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
    def get_waiting_to_parse_commits(self,count=0):
        """
        get pending tasks.

        :return: bool
        """
        raise NotImplementedError