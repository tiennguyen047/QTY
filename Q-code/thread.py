from PyQt5 import QtCore
import time

class ThreadClass(QtCore.QThread):
    """Thread that running every 2 second to check
    current working branche
    """
    any_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None,index=0):
        super(ThreadClass, self).__init__(parent)
        self.index=index
        self.is_running = True
    def run(self):
        # print('Starting thread...',self.index)
        cnt=0
        while (True):
            cnt+=1
            if cnt==99: cnt=0
            time.sleep(2)
            self.any_signal.emit(cnt)
    def stop(self):
        self.is_running = False
        # print('Stopping thread...',self.index)
        self.terminate()

    def is_alive(self):
        return self.is_running

# Create a worker class for long running task
class HardWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)
    parent 	 = None
    task_name = str()

    def run(self):
        """Long-running task."""
        exec("self.parent_object." + self.task_name)
        #Long-running task finish, emit finished signal
        self.finished.emit()
        # print("Long-running task %s finished" %self.task_name )
    
    def get_task(self, parent_object, task_name: str) -> None:
        self.parent_object = parent_object
        self.task_name = task_name
