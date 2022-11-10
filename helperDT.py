from abc import abstractmethod
from typing import Tuple,Sequence


class Query:
    def __init__(self, string) -> None:
        self.operation, self.table, self.listColumns, self.listCondition = self.ParseString(string)
    @abstractmethod
    def checkSqlInjection(self) -> bool:
        pass
    @abstractmethod
    def parseString(self, string)-> Tuple[str,str,Sequence[str],Sequence[str]] :pass
    @abstractmethod
    def toString(self) -> str :pass 

class Data:  #class used to interpret and represent data read from operationalDB and to write on the hist databases
    pass

class Credential:pass #data type used to represent db credential

class DatabaseCredential: #data type used to represent all the stuff necessary to connect on a remote db
    def __init__(self,address,port,credential : Credential) -> None:
        self.address=address
        self.port=port
        self.credential = credential

class QueryError(Exception): pass
class BulkCopyException(Exception): pass