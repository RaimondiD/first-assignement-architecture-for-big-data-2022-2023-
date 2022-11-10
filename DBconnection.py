from abc import abstractmethod
from helperDT import DatabaseCredential,Query,Data,Credential
from typing import Tuple,Sequence, TypedDict

class DBconnection:    #class used to make transparent the fact that the db is remote. They manage all the connection stuff with the DB
    @abstractmethod
    def __init__(self,db : DatabaseCredential) -> None:
        pass
    @abstractmethod
    def execute_query(self, query:Query)->Tuple[str,Data] : pass

    @abstractmethod
    def getAllData(self,credential):
        ds = self.getDataStructure()
        data = self.__selectAllData(ds)

    @abstractmethod
    def getDataStructure(self) -> TypedDict[str,TypedDict[str,Sequence[str]]] : pass    
    @abstractmethod
    def initData(self,data:Data,dataStructure) -> None : pass  #initialize a db starting from a datastructure and some data
    @abstractmethod
    def __selectAllData(self,dataStructure : TypedDict[str,TypedDict[str,Sequence[str]]]) -> Data :pass
    
class CDCDBconnection(DBconnection):
    @abstractmethod
    def getChanges(self, sync, tableList = None) -> Sequence[Tuple[int,Query]]: pass
