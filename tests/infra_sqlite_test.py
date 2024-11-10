import os
import stat
import random
import string
import unittest
from typing import List

try:
    from src.infrastructure import sqlite_client as sq
except ModuleNotFoundError:
    from infrastructure import sqlite_client as sq


class TestInfraSQLite(unittest.TestCase):
    """Tests for the SQLite infrastructure"""

    querys_db_name: str = "querys_db.db"
    querys_db: sq.SqliteManager

    querys_db_table: str = "table_name"
    querys_db_table_fields: List[str] = ["field1", "field2"]

    def test_init_new_file(self):
        """Validates that a new database can be created from scratch"""
        db_filename: str = "".join(random.choices(string.ascii_letters, k=5)) + ".db"

        try:
            manager = sq.SqliteManager(f"./{db_filename}")
            manager.close()

        except sq.InfrastructureException as err:
            raise err

        finally:
            if os.path.isfile(f"./{db_filename}"):
                os.remove(f"./{db_filename}")

    def test_query_ok_read_ok(self):
        """Validates that a query can be executed and the result can be read"""
        db_filename: str = "".join(random.choices(string.ascii_letters, k=5)) + ".db"

        try:
            manager = sq.SqliteManager(f"./{db_filename}")
            manager.exc_query("".join([
                f"CREATE TABLE {self.querys_db_table} ",
                f"({self.querys_db_table_fields[0]} ",
                f"TEXT, {self.querys_db_table_fields[1]} TEXT)"
            ]))

            manager.exc_query("".join([
                f"INSERT INTO {self.querys_db_table} ",
                "VALUES ('value1', 'value2')"
            ]))

            result = manager.read_query("".join([
                f"SELECT * FROM {self.querys_db_table}"
            ]))

            manager.close()

            self.assertEqual(result, [("value1", "value2")])
        except sq.InfrastructureException as err:
            raise err

        finally:
            if os.path.isfile(f"./{db_filename}"):
                os.remove(f"./{db_filename}")

    def test_query_ok_read_nok(self):
        """Validates that a query goes ok but read fails per invalid field"""
        db_filename: str = \
            "".join(random.choices(string.ascii_letters, k=5)) + ".db"

        try:
            manager = sq.SqliteManager(f"./{db_filename}")
            manager.exc_query("".join([
                f"CREATE TABLE {self.querys_db_table} ",
                f"({self.querys_db_table_fields[0]} ",
                f"TEXT, {self.querys_db_table_fields[1]} TEXT)"
            ]))

            manager.exc_query("".join([
                f"INSERT INTO {self.querys_db_table} ",
                "VALUES ('value1', 'value2')"
            ]))

            with self.assertRaises(sq.InfrastructureException):
                manager.read_query("".join([
                    f"SELECT * FROM {self.querys_db_table} ",
                    "WHERE field3 = 'value3'"
                ]))

            manager.close()
        except sq.InfrastructureException as err:
            raise err

        finally:
            if os.path.isfile(f"./{db_filename}"):
                os.remove(f"./{db_filename}")

    def test_query_nok_read_ok(self):
        """Validates that a query goes nok but read goes ok"""
        db_filename: str = \
            "".join(random.choices(string.ascii_letters, k=5)) + ".db"

        try:
            manager = sq.SqliteManager(f"./{db_filename}")
            manager.exc_query("".join([
                f"CREATE TABLE {self.querys_db_table} ",
                f"({self.querys_db_table_fields[0]} ",
                f"TEXT, {self.querys_db_table_fields[1]} TEXT)"
            ]))

            with self.assertRaises(sq.InfrastructureException):
                manager.exc_query("".join([
                    f"INSERT INTO {self.querys_db_table} ",
                    "VALUES ('value1', 'value2', 'value3')"
                ]))

            result: list[tuple[str, ...]] = manager.read_query("".join([
                f"SELECT * FROM {self.querys_db_table}"
            ]))

            self.assertListEqual(result, [])

            manager.close()
        except sq.InfrastructureException as err:
            raise err

        finally:
            if os.path.isfile(f"./{db_filename}"):
                os.remove(f"./{db_filename}")

    def test_query_nok_read_nok(self):
        """Validates that a query goes nok and read goes nok"""
        db_filename: str = \
            "".join(random.choices(string.ascii_letters, k=5)) + ".db"

        try:
            manager = sq.SqliteManager(f"./{db_filename}")
            manager.exc_query("".join([
                f"CREATE TABLE {self.querys_db_table} ",
                f"({self.querys_db_table_fields[0]} ",
                f"TEXT, {self.querys_db_table_fields[1]} TEXT)"
            ]))

            with self.assertRaises(sq.InfrastructureException):
                manager.exc_query("".join([
                    f"INSERT INTO {self.querys_db_table} ",
                    "VALUES ('value1', 'value2', 'value3')"
                ]))

            with self.assertRaises(sq.InfrastructureException):
                manager.read_query("".join([
                    f"SELECT * FROM {self.querys_db_table} ",
                    "WHERE field3 = 'value3'"
                ]))

            manager.close()
        except sq.InfrastructureException as err:
            raise err

        finally:
            if os.path.isfile(f"./{db_filename}"):
                os.remove(f"./{db_filename}")
