import sqlite3

from record import Record


class Data:
    def __init__(self):
        self.cursor         = None
        self.connection     = None
        self.data_file_name = "working_time.db"
        self.table_name = self.data_file_name.split(".")[0]

    def connect_sql(self):
        self.connection = sqlite3.connect(self.data_file_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        command = """CREATE TABLE """ + self.table_name + """ (
        branch_name     VARCHAR(180) PRIMARY KEY, 
        start_time      FLOAT(20,6), 
        duration        INTEGER,
        working_day     DATE);"""
        self.cursor.execute(command)
        self.connection.commit()

    def insert_record(self, record: Record):
        command = "INSERT INTO " + self.table_name + " VALUES " + record.get_string() + ";"
        self.cursor.execute(command)
        self.connection.commit()

    def insert_many_records(self, record_list: list):
        record_list = [record.get_tuple() for record in record_list]
        command = "INSERT INTO " + self.table_name + " VALUES(?,?,?,?,?);"
        self.cursor.executemany(command, record_list)
        self.connection.commit()
    
    def update_record(self, branch_name: str, property: str, new_value):
        """_summary_

        Args:
            branch_name (str): current working branch name
            property (str): "start_time"  or "duration"
            new_value (_type_): new value
        """
        command = "UPDATE " +  self.table_name + " SET \"" + property + "\" = " + str(new_value) + \
        " WHERE branch_name = \"" + branch_name + "\";"
        self.cursor.execute(command)
        self.connection.commit()

    def get_record_property(self, branch_name: str, property: str):
        """_summary_

        Args:
            branch_name (str): current working branch name
            property (str): "start_time"  or "duration"
        """
        command = "SELECT \"" + property + "\" FROM " + self.table_name + \
                  " WHERE branch_name = \"" + branch_name + "\" ;"
        self.cursor.execute(command)
        result = self.cursor.fetchone()

        return result[0]

    def is_exist_record(self, branch_name) -> bool:
        command = "SELECT EXISTS(SELECT 1 FROM " + self.table_name + \
                 " WHERE branch_name = \"" + branch_name + "\" LIMIT 1);"
        self.cursor.execute(command)
        result = self.cursor.fetchone()

        return bool(result[0])
        
    def close_connect(self):
        self.connection.close()
        
    def print_table(self):
        command = "SELECT * FROM " + self.table_name
        self.cursor.execute(command)
        ans = self.cursor.fetchall()
        log_file = open("work.txt", "w")
        for i in ans:
            log_file.write(str(i) + "\n")
        log_file.close()

    def reset_table(self):
        command = "TRUNCATE TABLE " + self.table_name + ";"
        self.cursor.execute(command)
        self.connection.commit()
    
    def drop_table(self):
        command = "DROP TABLE " + self.table_name + ";"
        self.cursor.execute(command)
