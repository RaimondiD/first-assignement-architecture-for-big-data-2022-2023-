from abc import abstractmethod
from helperDT import DatabaseCredential, Query, Data,QueryError,BulkCopyException
import threading
import time
from DBconnection import DBconnection
from typing import Tuple,Sequence



class BatchSqlExtractor:

    def __init__(self, sourceDB: DatabaseCredential,
                 histDb: DatabaseCredential,checkUpdateCond = 24*60*60*1000) -> None:  
        self.sourceDBconnection = self.__connect(sourceDB)  #
        self.histDBConnection = self.__connect(histDb)
        self.lastUpdate = 0  # get the fresh changes
        self.checkUpdateCond = checkUpdateCond
        self.__fullUpdate()
        x = threading.Thread(target=self.__synchronizer)
        x.start()

    def __synchronizer(self):
        while (True):
            time.sleep(self.checkUpdateCond)   
            while (self.__updateCondtion()):
                self.update()

    """ get the log that goes from the last ts
    listOfQueries -  [[timestamp1,query1], [timestamp2,query2]]
    getChanges - retrieve executed query """
    def update(self):
        listOfQueries = self.sourceDBconnection.getChanges(self, self.lastUpdate)
        for queryWithTime in listOfQueries:
            try:
                # execute every new query (insert, update and delete)
                self.histDBConnection.execute_query(queryWithTime[1])
                self.lastUpdate = queryWithTime[0]
            except:
                print("db exception occurred.")
                break

    @abstractmethod
    def __updateCondition(
            self) -> bool:  # implement the update policy, can be implemented in differents way
        pass

    def __fullUpdate(
            self) -> None: 
        try:
            data,structure = self.sourceDBconnection.getAllData()
            self.histDBConnection.initData(data,structure)
        except:
            print("error in initial copy of data")
            raise BulkCopyException
        self.lastUpdate = time.time()

    def read(self, query:Query) -> Data:
        if(query.checkSqlInjection() or query.operation != "SELECT"):
            raise QueryError
        return self.histDBConnection.execute_query(query)
        
    @abstractmethod
    def __connect(self, database: DatabaseCredential) -> DBconnection:
        pass
