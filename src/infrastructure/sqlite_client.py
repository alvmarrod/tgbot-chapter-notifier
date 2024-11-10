import sqlite3
import threading

try:
    from src.utils import log
    from src.infrastructure.infra_exception import InfrastructureException
except ModuleNotFoundError:
    from utils import log
    from infrastructure.infra_exception import InfrastructureException


class SqliteManager:
    """Manages the connection to a SQLite database

    TODO: Beware Lock could be wrong and could need to be changed to Semaphore"""

    db_con: sqlite3.Connection
    lock:   threading.Lock

    def __init__(self, file: str):
        try:
            log("bot", "info", ["sqlite_manager", f"Connecting to {file}"])
            self.lock = threading.Lock()
            with self.lock:
                self.db_con = sqlite3.connect(file, check_same_thread=False)
        except Exception as err:
            raise InfrastructureException(err) from err

    def read_query(self, reader_query: str, *args: str) -> \
            list[tuple[str, ...]]:
        """Execute a reader query and return the result as a list of
        tuples containing strings"""
        result: list[tuple[str, ...]] = []
        try:
            with self.lock:
                result = self.db_con.execute(reader_query, args).fetchall()

        except Exception as err:
            raise InfrastructureException(err) from err

        return result

    def exc_query(self, exc_query: str, *args: str) -> None:
        """Execute a non-reader query"""
        try:
            with self.lock:
                cursor: sqlite3.Cursor = self.db_con.execute(exc_query, args)
                self.db_con.commit()
                if cursor.rowcount == 0:
                    raise InfrastructureException("No rows affected")

        except Exception as err:
            raise InfrastructureException(err) from err

    def close(self) -> None:
        try:
            with self.lock:
                self.db_con.close()

        except Exception as err:
            raise InfrastructureException(err) from err
