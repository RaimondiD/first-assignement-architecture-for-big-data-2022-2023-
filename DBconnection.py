from abc import abstractmethod
from helperDT import DatabaseCredential,Query,Data
from typing import Tuple,Sequence

class DBconnection:    #class used to make transparent the fact that the db is remote. They manage all the connection stuff with the DB
    @abstractmethod
    def __init__(self,db : DatabaseCredential) -> None:
        pass
    @abstractmethod
    def execute_query(self, query:Query)->Tuple[str,Data] : pass

class CDCDBconnection(DBconnection):
    @abstractmethod
    def getChanges(self, sync, tableList = None) -> Sequence[Tuple[int,Query]]: pass
