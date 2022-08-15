class Record:
    def __init__(self, 
                 branch_name: str,
                 start_time : float,
                 date       : str,
                 duration   : float=0) -> None: 
        """_summary_

        Args:
            branch_name (str): name of branch
            start_time (float): result of time.time()
            end_time (float): result of time.time()
            date (str): working day - Format: YYYY-MM-DD: 2022-6-4 
        """
        self.__branch_name = branch_name
        self.__start_time  = start_time
        self.__date        = date
        self.__duration    = int(duration)

    def get_string(self) -> str:

        return str(self.get_tuple())

    def get_tuple(self) -> tuple:
        record_tuple = tuple([self.branch_name, self.start_time, self.duration, self.date])
        
        return record_tuple

    @property
    def branch_name(self):
        return self.__branch_name
    @property
    def start_time(self):
        return self.__start_time
    @property
    def date(self):
        return self.__date
    @property
    def duration(self):
        return self.__duration

