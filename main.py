from abc import abstractmethod
from dataclasses import dataclass
from turtle import update
from sql_conn import Sql_conn



class Data:
    pass

class BatchSqlExtractor:

    def __init__(self,updateTime,adress,port,credential,query) -> None: #add paramse for the secondo db, create second database in attribute
        self.database_connection = self.connect(adress,port,credential) #control update time
        self.update = updateTime
        self.queryParams = query
        self.__first_update()

    
    def __first_update(self) -> None:
        check_update() #creare update per capire
        query = f"SELECT * from TABLENAME when timestamp >= {self.update}" #wrote a good query
        data = self.__readFromOneStream(query)
        self.__update_copy_dataset(data)
        #drop da hist data
        
    @abstractmethod
    def __readFromOneStream(self,query)-> Data:
        pass
    
    @abstractmethod
    def __update_copy_dataset(self,data) -> None:
        pass

    @abstractmethod
    def connect(self,address,port,credential) ->Sql_conn :
        pass

pippo = BatchSqlExtractor()
pippo.readFromOneStream()

