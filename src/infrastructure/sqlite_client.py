# Alvaro - Btc Sources

import sqlite3
import threading
from typing import List
from src.infrastructure.infra_exception import InfrastructureException

if __name__ == "__main__":
    raise InfrastructureException("Este fichero es una clase no ejecutable")

class SqliteManager:

    db_con: sqlite3.Connection
    lock:   threading.Lock

    def __init__(self, file: str):
        try:
            self.db_con = sqlite3.connect(file, check_same_thread = False)
            self.lock = threading.Lock()
        except InfrastructureException as e:
            raise e
        
    def read_query(self, reader_query: str) -> List[str]:
        """Execute a reader query and return the result as a list of strings"""
        try:
            self.lock.acquire()
            result = self.db_con.execute(reader_query).fetchall()
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise InfrastructureException(e)
        return result
    
    def exc_query(self, exc_query: str) -> None:
        """Execute a non-reader query"""
        try:
            self.lock.acquire()
            self.db_con.execute(exc_query)
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise InfrastructureException(e)

    def closeDB(self) -> None:
        try:
            self.lock.acquire()
            self.db_con.close()
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise InfrastructureException(e)