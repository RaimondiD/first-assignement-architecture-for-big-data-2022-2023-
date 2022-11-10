from helperDT import Credential,Query,Data
from typing import Tuple,Sequence,TypedDict
from pathlib import Path
from abc import abstractmethod
import threading
import time

class DbAdapter:
    def __init__(self, credentialPath, logPath, structurePath, ip, port,**kwargs):
        self.credentialPath = credentialPath
        self.logPath = logPath
        self.structurePath = structurePath
        self.serverPath = (ip,port)
        self.__init_db(**kwargs)
        self.operationDict = {"INSERT" : lambda self,query: self.__adInsert(query),
                              "UPDATE" : lambda self,query: self.__adUpdate(query),
                              "DELETE" : lambda self,query: self.__adDelete(query),
                              "SELECT" : lambda self,query: self.__adSelect(query)}
        self. serverThread = threading.Thread(target= self.__listener)
        self.serverThread.start()


    @abstractmethod
    def __init_db(self) : pass

    @abstractmethod
    def __listener(self):  
        """method that wait requests,it expose the services in self.dbExposedMethods(using rest api for example): in the CDC case they can be getChanges, executeQuery and getDbStructure and return at the dbConnection the corrispondent results"""
        pass
    
    def executeQuery(self,query:Query,credential : Credential) -> Tuple[str,Data]:
        allowed,wrongCredentialMessage = self.__checkCredential(query,credential)
        if(not allowed): return wrongCredentialMessage
        if(not self.__checkCredential(query,credential)[0]): return "wrong credential"
        error,status,result = self.__dbExecuteQuery(query,credential) #do the query on db and check if all is ok, if not we return an error to the listener
        if(not error): 
            self.operationDict[query.operation](self,query) #we use this call to do some operations after the query is done on the db. in our idea these call can be used to save operation
                                                        #logs to CDC 
        return status,result

    @abstractmethod
    def __checkCredential(self,query:Query,credential:Credential)-> Tuple[bool,str] : pass #we want to have a check credential on the adapter because this method allows us to obtain a more fine-grained control 
                                                                          #on the accesses and we can also implement an access policy that is independent from the db.
                                                                          #  If the access policy of the specific db is already fine it's always possible return true
    def __dbExecuteQuery(self,query:Query,credential : Credential) -> Tuple[bool,str] :pass

    def getChanges(self,credential,sync,tableList = None)-> Sequence[Sequence[Tuple[int,Query]]]:  #In this and in the save logs we use the idea of read/write the information according to a table structure because 
                                                                                                   #in this way is easier extend this code with the aim of apply different CDC policy at different tables.
        if(not tableList):
            tableList = self.getStructure.keys()
        allowed,wrongCredentialMessage = self.__checkReadCredential(tableList,credential)
        if(not allowed): return wrongCredentialMessage
        result= []
        for table in tableList:
            result.append(self.__getTableChanges(table,sync))
        return result
   
    @abstractmethod
    def __getTableChanges(self,table,sync) -> Sequence[int,Query] : pass  #this method use the sync information to extract the fresh query that are done on the db. The sync information can for be example the lastUpdate ts
                                                                      #so i want to return, for that table all the query that are saved in the logs with ts grater than sync (and the associated sync). Another option can be to  differentiate registry and log tables and for
                                                                      #the registry tables send in sync the hash of table (for each row hash(keyCol) and hash(valueCol) and extract the query computing the difference from the same hash calculated on
                                                                      #DB tables. 

    @abstractmethod
    def __checkReadCredendial(self,tables,credential) -> Tuple[bool,str] : pass

    @abstractmethod
    def getStructure(self) -> TypedDict[str,TypedDict[str,Sequence[str]]] : pass #return the struct of the db in form of dictionary. First key are the table names. 
                                                                                #At each table are associated another dict with some other keys (for example column names)

    def __adInsert(self,query:Query) : 
        self.__savelog(query)
    
    def __adUpdate(self,query:Query):
        self.__savelog(query)
    
    def __adDelete(self,query:Query):
        self.__savelog(query)
    
    def __adSelect(self,query:Query): pass #we don't like build 4 identical methods but the idea is that
                                    #if anyone wants to modify one of these in a concrete class he can extends only that specific
                                    #method. These methods are used to do some additional operation after that a specific
                                    #type of query is done on the db (look executeQuery and operationDict).
                                

    def __saveLog(self,query:Query):   
        savePath = Path(self.logPath / query.table / f"{time.localtime()}.log" )
        with open(savePath) as logfile:
            logfile.write(query.toString())




